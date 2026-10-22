# ADR-001: Repository-native documentation and persistent agent context

## Status

Proposed — scaffold draft only; not an accepted architecture decision.

## Date

2026-10-22.

## Context and problem

Future sessions and five student contributors need recoverable project context beyond chat history.

## Considered options

Chat-only context; repository-resident instructions, state, logs, and decision records.

## Evaluation criteria

Discoverability, traceability, low maintenance, and clear evidence status.

## Proposed decision and rationale

Use AGENTS.md for instructions, PROJECT_STATE.md for current state, journals for history, and ADRs for significant choices. This makes context reviewable alongside the project.

## Consequences, risks, and tradeoffs

Documents need maintenance and can drift or duplicate each other. Keep current state separate from historical records.

## Evidence

Owner supplied the requested structure and authorized its scaffold. This does not accept all future methodological choices.

## Revisit conditions

Owner review or evidence that the structure is confusing or burdensome.

## Related decisions

None.
