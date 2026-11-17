# Final local Phase 2 verification — 2026-11-16

The owner requested finishing remaining work, checking LWR/multi-agent requirements first, keeping viva simple and performing no pushes. The original technical brief is still unlocated in accessible sources; see ../../docs/PHASE2_REQUIREMENTS_FINAL_AUDIT.md. Generic rubric requirements are mapped there. The synthetic extension is an owner-authorized conservative completion choice, not a fabricated faculty requirement.

## Two separate evidence streams

- Forecasting: the November 13 GRU/GAT/control-variant/checkpoint study is unchanged. Small evidence remains in ../phase2-20261112/. XGBoost still has better MAE than these compact DL models; the validation blend chooses pure XGBoost. No test-driven retuning/clipping occurred.
- LWR/control: control/ contains the predeclared model/config/source identity, all 40 per-run metric rows, five-seed summaries, paired comparisons, trajectory checksums and invariant verification. Full trajectories remain local/ignored. Eight cells and two local rule-based signal agents form a separate synthetic experiment, not calibrated METR-LA, MARL or GAT-driven control.

## Fresh checks

76 tests passed in 2.40 seconds (latest final run) with real data available and no skips. Ruff lint/format passed for 51 Python files. Seven added tests cover CFL/invalid physics, red gating, downstream blockage, retained source arrivals, closed-system conservation/bounds, green/clearance/starvation timing and deterministic/zero-demand execution. Every one of the 40 simulations also enforces physical invariants on every time step. No stability theorem, control optimality or real-world safety certification is claimed.

The wheel rebuilt with simulation modules and imported neural/control modules outside the checkout; one physical update passed. A saved graph checkpoint forecast an actual observed-history CSV again. See package_check.json and checks.json. No claim of a fresh full neural refit is made; its unchanged source/checkpoint/data hashes are verified instead.

Both current academic artifacts were compiled/rendered and every page/slide reviewed. PPTX structural/native table/chart/font/import validation passed; this is not a native PowerPoint opening test. The report uses an assumed triangular fundamental diagram and clearly separates vehicle-time/boundary waiting from mean completed-trip delay. Original November 13 artifacts/source are privately archived; dated historical records are preserved.

## Interpretation

The responsive agents reduced system vehicle-time against an equal-green baseline under the four selected synthetic scenarios. The fixed policy is not demand-optimized. Parameters, topology and arrivals are illustrative, not measured LA traffic. Keep all per-run results, seed variability, physical constraints and final residuals visible. This does not establish general superiority or that neural forecasts improve control.

## Reproduce and review

Use ../../docs/PHASE2_RUNBOOK.md and ../../docs/PHASE2_CONTROL_NOTES.md. The simulator needs only the pinned base dependencies and no raw METR-LA, neural checkpoints, SUMO or CityFlow installation. Source fingerprints, latest artifact sizes/hashes and actual check scope are in source_snapshot.json, submission_artifacts.json and artifact_checks.json.

Nothing was staged/committed/pushed, no PR was created/merged, no form was submitted and this verification pass created no member ZIP. Five local handoffs are subsequently prepared under the owner's separate request; see ../../docs/handoffs/phase2/. The current GitHub main therefore does not yet publish this Phase 2 extension. Owner review, any original project-specific brief requirements, genuine member understanding/rehearsal, later handoffs/publication and university-email submission by Nov 19 12:55 IST remain owner-managed actions. No final faculty acceptance is certified.
