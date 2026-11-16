# Phase 2 integration/review — Rudraksh Sharma

- Package: 01-rudraksh-control
- Assigned review scope: Synthetic LWR/CTM physics and two local signal agents
- Prepared package date: 2026-11-16 (not a student-work date)
- Status: **integrated and agent-reviewed on 2026-11-16; member understanding and reproduction pending**

The source, experiments and academic materials were prepared under Kavya Katal's coordination with substantial AI assistance, building on the teammate prototype and preserved Phase 1 work. This log records integration and review of that prepared work. It records no completed independent student implementation or understanding.

## Agent integration and review (2026-11-16, about 17:25–17:40 IST, Asia/Kolkata)

Performed by a Claude Code agent (Claude Fable 5.2) run by Rudraksh Sharma under the Git identity `rxdrxksh01`. Everything in this section is what the agent did. It is not evidence that Rudraksh personally reproduced or understands the module.

### Repository, base and branch

- Local clone: remote `origin` is the canonical repository `KatalKavya96/DLML_Midsem_Project`; remote `fork` is `rxdrxksh01/DLML_Midsem_Project`. The account has read-only access to canonical, so the branch was pushed to the fork.
- Base: canonical `origin/main` at `fbb71d1`, fetched on 2026-11-16. This is the same commit as the package's recorded preparation base.
- Branch: `codex/rudraksh-phase2-control`, created from that base. The working tree was clean beforehand. The existing local branch `codex/rudraksh-phase1-report` was left as it was.

### Verification and import

- `python3 -I VERIFY_PACKAGE.py`, run in the extracted package before any edit: "Verified 17 assigned payload files and all supplied baseline bytes."
- `BASELINE.json` lists all 17 paths as new (`base_sha256: null`). None of them existed on `origin/main`, on the previous local branch or in the working tree, so every file was a plain import with nothing to compare or reconcile.
- After copying, all 17 files in the repository root matched the `MANIFEST.json` SHA-256 values and byte counts.
- Imported unchanged (16 files): the four files in `src/trafficml/simulation/`, `configs/control.yaml`, `scripts/run_control.py`, `tests/test_control.py`, the three `docs/PHASE2_CONTROL_*.md` files and the six files in `verification/phase2-final-20261116/control/`.
- Changed (1 file): this review log, completed from the prepared template.
- Genuine corrections to code, configuration, protocol or evidence: none. The review found no evidence-backed defect.
- Not copied: the package README, HANDOFF, MANIFEST, BASELINE, verifier, common prompt and `repo-context/`. No other member's file and no shared coordinator file was touched. The delivery ZIP is ignored by `.gitignore` and was not staged.

### What the module does (agent's description)

Purpose: a small traffic simulation that shows vehicle conservation, queue spillback and two signals that affect each other. It is separate from the METR-LA forecasting study.

- `src/trafficml/simulation/lwr.py` holds the physics. The road is eight cells of 0.25 km: main cells 0→1→2→3→4→5→exit, with side cell 6 joining before cell 2 and side cell 7 joining before cell 4. Each cell has a sending limit (what it can release) and a receiving limit (the room it has left), both from a triangular flow–density relation with free speed 60 km/h, wave speed 20 km/h and jam density 150 veh/km. That gives a capacity of 2250 veh/h and a storage of 37.5 vehicles per cell. The flow between two cells is the smaller of the sender's and the receiver's limit. `advance()` computes all flows from the old state, applies them together, and then raises an error if a cell leaves its physical bounds, a limit is exceeded or the vehicle count does not balance.
- CFL: the 5-second step is rejected unless the fastest speed covers at most one cell per step (60 km/h × 5 s = 83 m, less than 250 m).
- Red gating: signal A lets either cell 1 or cell 6 enter cell 2; signal B lets either cell 3 or cell 7 enter cell 4. During all-red neither moves.
- Source queues: arrivals for cells 0, 6 and 7 wait in an external queue and enter only as fast as the cell can receive them. Nothing is dropped.
- `src/trafficml/simulation/agents.py` holds the two policies. `FixedSignal` repeats 40 s main, 5 s all-red, 40 s side, 5 s all-red; agent B is offset by 45 s. `ResponsiveSignal` sees only its own main, side and downstream cell counts. It keeps a green for at least 20 s, switches when the other approach's pressure (upstream count minus downstream count, floored at zero) is more than 2 vehicles higher, switches when its own approach is empty and the other is not, and is forced to switch after 60 s. Every switch has 5 s all-red.
- `src/trafficml/simulation/experiment.py` builds the four demand scenarios (balanced, arterial peak, side peak, downstream restriction), each with 60 minutes of demand and 20 minutes of drain, and runs one policy over one arrival sequence.
- `scripts/run_control.py` reads `configs/control.yaml`, samples Poisson arrivals once per scenario and seed, runs both policies on the same arrivals, and writes a manifest, per-run metrics, a summary, a paired table, trajectory files and their hashes.

Inputs: `configs/control.yaml` only. No METR-LA data, model checkpoint or network access.
Outputs: `manifest.json`, `metrics.csv`, `summary.csv`, `paired_system_time.csv`, `artifacts.json` and 40 `.npz` trajectories in the chosen run directory.
Dependencies: numpy (2.x, for `np.trapezoid`), pandas and PyYAML. It does not import any other project module.

One update traced with the real code: cell 1 holds 10 vehicles (40 veh/km) and can send 2250 veh/h; cell 2 holds 30 vehicles (120 veh/km) and can receive only 20 × (150 − 120) = 600 veh/h. With signal A green for the main road, 600 veh/h flows, which is 0.8333 vehicles in 5 s. Cell 1 goes from 10 to 9.1667. Cell 2 gains that 0.8333 and sends 3.125 vehicles on to the empty cell 3, ending at 27.7083. The total stays at 40 vehicles.

### Checks run

Environment: macOS (Darwin 27.2.0), CPython 3.12.6. The repository has no `.venv`, so a throwaway environment was built outside the repository with `uv venv --python 3.12` and `uv pip install -r requirements.txt` (numpy 2.3.5, pandas 2.2.3, PyYAML 6.0.3, pytest 8.4.2, ruff 0.14.2). All commands ran from the repository root on this branch, which holds canonical `main` plus this package only.

| Command | Outcome |
|---|---|
| `PYTHONPATH=src pytest -q -ra tests/test_control.py` | Passed: 7 passed, no skips |
| `PYTHONPATH=src python scripts/run_control.py --help` | Passed: usage printed |
| `python scripts/run_control.py --help` (as written in the handoff, no `PYTHONPATH`) | Failed: `ModuleNotFoundError: No module named 'trafficml'`. Expected, because the package was not installed in this environment |
| `ruff check src/trafficml/simulation scripts/run_control.py tests/test_control.py` | Passed |
| `ruff format --check` on the same paths | Passed: 6 files already formatted |
| `ruff check .` and `ruff format --check .` | Passed: 43 files already formatted |
| `uv pip check` | Passed: 51 installed packages compatible |
| `python -m pip check` | Not run: the uv environment has no pip module |
| `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 pytest -q -ra` | Passed: 63 passed, no skips (56 existing tests plus the 7 control tests; the ignored local `data/raw` files were present) |
| `PYTHONPATH=src python scripts/run_control.py --run-dir <scratch directory outside the repository>` | Completed: 40 matched runs in about 2 seconds |

The 63-test result belongs to this branch only. The 76-test result in the prepared evidence needs all five Phase 2 packages and was not run here. No GitHub Actions result is claimed in this log.

Comparison of the fresh run with the frozen evidence in `verification/phase2-final-20261116/control/` (done with temporary scripts kept outside the repository):

- `metrics.csv`, `summary.csv` and `paired_system_time.csv` are byte-identical to the frozen files.
- All 40 trajectory hashes equal the ones in the frozen `artifacts.json`.
- The fresh manifest has the same source hashes and settings as the frozen one. Only the Python patch version differs (3.12.6 here, 3.12.13 in the frozen run).
- The 7 source hashes in the frozen `manifest.json` match the imported files.
- The rows in `results.json` and the table in `docs/PHASE2_CONTROL_RESULTS.md` equal means recomputed from `metrics.csv` (largest difference 9e-13). The stated maximum mass residual (3.04e-12 vehicles) and maximum density (143.6 veh/km, below the 150 jam density) also match.
- Pairing: each of the 20 scenario/seed pairs has one arrival hash and the same arrived-vehicle count for both policies.

The frozen evidence files were not regenerated or replaced.

Further probes (not added to the repository):

- All 40 saved trajectories stay within 0 to 37.5 vehicles per cell with non-negative queues. Greens always alternate. Completed responsive greens last 4 to 12 steps (20 to 60 s), fixed greens 8 steps, and every all-red lasts 1 step.
- 50,000 steps of `advance()` with random states, phases, arrivals and exit limits raised no invariant error; the worst cumulative mass residual was 5.2e-10 vehicles.

### Observations and remaining issues

- Why the fixed baseline does badly (the agent's reading, from the code and arithmetic): each approach gets 8 green steps in an 18-step cycle, so it can pass at most 2250 × 8/18 = 1000 veh/h. The arterial peak sends 1100 veh/h down the main road, so the fixed plan cannot keep up and queues grow. This is why the comparison shows a large gap, and why the protocol calls the baseline "not demand-optimized".
- The agents' "pressure" uses cell occupancy, which counts moving vehicles as well as stopped ones. It is not a measured queue length.
- How often each responsive rule fired, counted from the 20 responsive trajectories of the fresh run: 4274 switches in total, of which 1681 came at the 60 s maximum green and 379 happened while the agent's current approach was empty. The remaining switches came from the pressure comparison before the maximum. An uncongested cell releases one third of its vehicles each step (60 km/h × 5 s over 250 m), so a cell that has held traffic empties only gradually.
- `run_control.py` stops with a `ValueError` when `--config` points to a file outside the repository, because the manifest stores repository-relative paths. Confirmed by running it. The default configuration is not affected. Not changed: editing the runner would alter a source hash recorded in the frozen manifest. Left for the coordinator to decide.
- Several numbers in the three docs are missing a space (for example "speed60 km/h"). Not changed: the protocol's hash is part of the frozen run identity.
- Cross-package dependencies: `results.json` and the report figures are produced by `scripts/build_control_report.py` (package 03-anshuman-artifacts), so `results.json` could be checked but not regenerated here. The docs also refer to notes and a runbook that arrive with packages 03 and 05.
- `AGENTS.md` and `PROJECT_STATE.md` on canonical `main` still describe Phase 2 as deferred. The owner's Phase 2 and handoff authorization is in the updated coordinator files of package 05-kavya-integration. Those files were not edited here.

Limits that still apply: the simulation uses assumed parameters and invented demand and is not calibrated to Los Angeles traffic. The two agents are hand-written rules, not MARL, and no GAT forecast is used for control. The responsive rule is better than an equal-green baseline in four chosen scenarios only; no real-world delay saving is claimed. The forecasting results remain exploratory and are not changed by this package. No more specific faculty brief is available.

## Actual activity

- Actual date/time and reviewer/agent: 2026-11-16, about 17:25–17:40 IST; Claude Code agent (Claude Fable 5.2) run by Rudraksh Sharma.
- Repository, verified remotes, base and personal branch: canonical `origin`, personal `fork`; base `origin/main` at `fbb71d1`; branch `codex/rudraksh-phase2-control`.
- SHA-256 verification and current/base/prepared comparison: verifier passed; all 17 paths were new; all match the manifest after copying.
- Files imported, already identical, preserved or genuinely corrected: 16 imported unchanged; this log completed; none already present; none corrected.
- Purpose/inputs/outputs/dependencies explained: by the agent, in the section above. Not yet explained by the member.
- Exact commands with passed/failed/skipped outcomes and evidence: see "Checks run".
- Assistance used and limitations/missing dependencies: prepared owner/AI-assisted source reused unchanged; integration, checks and this log done with Claude Code. Combined-tree checks, `build_control_report.py` and `pip check` were not available.
- Human explanation/reproduction demonstrated: **not established**. Rudraksh has not yet explained the module in their own words, traced an update by hand or rerun the checks personally.
- Commit IDs and PR link: `f45d5b2` (simulation, configuration, runner), `7df55b4` (tests), `47deda7` (protocol, notes, frozen evidence), followed by the commit that adds this log. PR: https://github.com/KatalKavya96/DLML_Midsem_Project/pull/9
- Coordinator combined verification/faculty acceptance: **not established by this handoff**.
