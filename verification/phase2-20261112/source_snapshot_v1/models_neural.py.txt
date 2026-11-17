"""Small shared GRU with optional original-style additive graph attention.

Graph convention: mask[receiver, sender]. Stored distance[from,to] is
transposed to allow messages from `from` to `to`. This is an implementation
convention, not a verified physical upstream/downstream annotation.
"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


def masked_loss(prediction, target):
    valid = torch.isfinite(target)
    if not bool(valid.any()):
        return None
    return (prediction[valid] - target[valid]).abs().mean()


class GraphAttention(nn.Module):
    def __init__(self, hidden, heads, mask, uniform=False, dropout=0.1):
        super().__init__()
        if hidden % heads or mask.ndim != 2 or mask.shape[0] != mask.shape[1]:
            raise ValueError("incompatible attention dimensions")
        self.heads, self.channels, self.uniform = heads, hidden // heads, uniform
        self.projection = nn.Linear(hidden, hidden, bias=False)
        self.receiver = nn.Parameter(torch.empty(heads, self.channels))
        self.sender = nn.Parameter(torch.empty(heads, self.channels))
        nn.init.xavier_uniform_(self.receiver)
        nn.init.xavier_uniform_(self.sender)
        mask = torch.as_tensor(mask, dtype=torch.bool).clone()
        mask.fill_diagonal_(True)
        self.register_buffer("mask", mask)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, return_attention=False):
        b, n, _ = x.shape
        z = self.projection(x).reshape(b, n, self.heads, self.channels)
        left = (z * self.receiver).sum(-1).permute(0, 2, 1)
        right = (z * self.sender).sum(-1).permute(0, 2, 1)
        scores = F.leaky_relu(left.unsqueeze(-1) + right.unsqueeze(-2), 0.2)
        if self.uniform:
            scores = torch.zeros_like(scores)
        attention = scores.masked_fill(~self.mask, float("-inf")).softmax(-1)
        aggregate = torch.einsum("bhij,bjhc->bihc", self.dropout(attention), z)
        output = F.elu(aggregate.reshape(b, n, -1))
        return (output, attention) if return_attention else output


class TrafficGRU(nn.Module):
    def __init__(
        self, nodes, hidden=32, horizon=12, heads=2, mask=None, mode="temporal", dropout=0.1
    ):
        super().__init__()
        if mode not in {"temporal", "graph", "self", "uniform", "no_dropout"}:
            raise ValueError("unknown model mode")
        self.mode, self.nodes, self.horizon = mode, nodes, horizon
        self.gru = nn.GRU(2, hidden, batch_first=True)
        self.dropout = nn.Dropout(dropout)
        if mode != "temporal":
            if mask is None:
                raise ValueError("graph model needs a mask")
            if mode == "self":
                mask = torch.eye(nodes, dtype=torch.bool)
            self.graph = GraphAttention(hidden, heads, mask, mode == "uniform", dropout)
        self.head = nn.Linear(hidden * (1 if mode == "temporal" else 2) + 5, horizon)
        # Start from persistence; the network learns an additive correction.
        nn.init.zeros_(self.head.weight)
        nn.init.zeros_(self.head.bias)

    def forward(self, x, calendar):
        b, length, n, _ = x.shape
        if n != self.nodes:
            raise ValueError("sensor count differs from fitted graph")
        sequence = x.permute(0, 2, 1, 3).reshape(b * n, length, 2)
        _, hidden = self.gru(sequence)
        local = self.dropout(hidden[-1].reshape(b, n, -1))
        parts = [local]
        if self.mode != "temporal":
            parts.append(self.graph(local))
        parts.append(calendar[:, None].expand(-1, n, -1))
        correction = self.head(torch.cat(parts, -1)).permute(0, 2, 1)
        return x[:, -1, :, 0].unsqueeze(1) + correction
