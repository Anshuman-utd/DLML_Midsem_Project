# Phase 2 source register and synthesis

Reviewed during owner/AI-assisted preparation on November12 2026. This records inspected source material, not independent reading by every member or replication of the papers' experiments. No published score is treated as a local result.

| Source | Material inspected | Design connection | Important limit |
| --- | --- | --- | --- |
| Cho et al. (2014), Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation | Abstract and sections2.2/2.3 on encoding, reset/update gates and hidden state | Shared GRU summarizes recent speed history | Original application is machine translation. Our fixed-horizon regression head is different, and uses PyTorch's GRU implementation |
| Veličković et al. (2018), Graph Attention Networks | Abstract and architecture section2.1: transformed features, masked neighbours, softmax and aggregation | Original-style additive attention over permitted road-network senders | Original evaluation concerns graph tasks, not a guarantee on METR-LA. Attention weights do not establish physical causality |
| Li et al. (2018), Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting | Abstract and methodology2.1–2.3: graph forecasting, directed diffusion and recurrent temporal dynamics | Traffic-specific rationale for jointly considering space and time; benchmark provenance | Our GRU+GAT is not DCGRU or a scheduled-sampling encoder–decoder. Splits/masks differ, so paper scores are not directly ranked against ours |
| Richards (1956), Shock Waves on the Highway | Publisher bibliographic record and abstract | Macroscopic density/speed relationship and traffic waves motivate the LWR theory discussion | Full paper was not independently replicated. Speed-only METR-LA cannot establish calibrated density/flow physics or signal-control benefit |
| Official PyTorch2.7 documentation | GRU/module behaviour and installation compatibility; gate equations reconfirmed from the installed torch 2.7.1 GRU docstring on November13 (the versioned web page was unavailable on this check) | Implement a tested GRU and explicit dropout/checkpoint workflow | A single-layer GRU's inter-layer dropout argument alone does not supply dropout; runtime versions and platform still matter |

## Synthesis

Temporal sequence learning and graph aggregation answer distinct questions. We first need a temporal baseline, then a controlled neighbour-access comparison. Comparing graph DL only against differently engineered trees cannot isolate the graph contribution. Self-loop and uniform-neighbour controls therefore accompany the main model. Published traffic success motivates the experiment, rather than predetermining its conclusion.

## Primary links

- Cho: https://arxiv.org/abs/1406.1078 ; method PDF https://arxiv.org/pdf/1406.1078
- GAT: https://arxiv.org/abs/1710.10903 ; architecture PDF https://arxiv.org/pdf/1710.10903
- DCRNN: https://arxiv.org/abs/1707.01926 ; methodology PDF https://arxiv.org/pdf/1707.01926
- Richards: https://doi.org/10.1287/opre.4.1.42
- PyTorch GRU: https://docs.pytorch.org/docs/2.7/generated/torch.nn.GRU.html

The original master attachment also proposes CityFlow reading. That simulator is not implemented here; it must not be listed as an implemented component. The standalone faculty Project 4 brief remains unlocated, so this source register does not resolve separate mandatory LWR/control scope.


## LWR/control sources inspected November16

- California PATH, UC Berkeley, Technical Overview of the Cell Transmission Model (2015), pages1–4: triangular fundamental diagram, Godunov sending/receiving update, CFL, nodes and red/green gating. https://connected-corridors.berkeley.edu/sites/default/files/ctm_technical_overview.pdf
- Lioris and Varaiya, Variants of max pressure control for a network of signalized intersections, pages1–2: adjacent-queue observations, fixed-time comparator and pressure-based local choice. https://connected-corridors.berkeley.edu/sites/default/files/Variants%20of%20Max%20Pressure%20Control%20for%20Signalized%20Intersections.pdf
- Daganzo (1994), Berkeley ITS bibliographic/abstract records for CTM and network extension. Full original paper download was unavailable on this check; the Berkeley technical overview supplied the implemented discretization. https://its.berkeley.edu/publications/cell-transmission-model-network-traffic

Our signal rule uses cell-occupancy pressure and min/max-green/clearance constraints, not the paper’s full queueing model or stability proof. Parameters are synthetic. No optimality/stability guarantee or calibrated prediction-to-action pipeline is transferred from these sources.
