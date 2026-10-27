# Rudraksh Sharma - module review register

Package prepared: 2026-10-27. Role: Dataset provenance, loading and graph integrity.
Status: **integrated and agent-reviewed; member understanding/reproduction pending**. No individual implementation or completion is claimed.

Existing module provenance: teammate prototype and integrated owner-prepared extension with substantial AI assistance. Redistribution does not change authorship.

## Required review

Confirm dataset shape/frequency/sensor ordering and speed-only scope; record real loader checks and unresolved metadata.

## Agent integration and review (2026-10-27, Asia/Kolkata)

Performed by a Claude Code agent (Claude Opus 5.5) run by Rudraksh Sharma under the Git identity `rxdrxksh01`. This records what the agent did; it is not evidence that Rudraksh personally reproduced or understands the module.

### Integration

- Base: canonical `origin/main` at `5576750` (coordination fix). Branch: `codex/rudraksh-data`.
- All 13 payload files were verified against the package `MANIFEST.json` SHA-256 values, both in the extracted package and after copying into the repository root. All matched; no extra, missing or symlinked files. `COMMIT_PATHS.txt` matches the manifest and `docs/handoffs/FILE_OWNERSHIP.json`.
- None of the 13 paths existed on `main`, so there were no conflicts. Shared coordinator files were not touched. `data/.gitkeep` is explicitly allowed by `.gitignore`.
- No code changes: the review found no evidence-backed defect. Files are byte-identical to the package, apart from this completed log.

### Module summary (agent's description)

- `src/trafficml/data/load.py`: reads `metr-la.h5` directly with PyTables (the pandas 0.15 / Python 2 file is not readable by current `pd.read_hdf`) into a time x sensor DataFrame. It rejects mismatched sensor order, empty data, NaT timestamps, duplicate sensors, infinite or negative speeds, and non-5-minute steps. 0 mph is left in place; masking it as missing belongs to package 02 (`masking.py`). It also loads sensor ids, road distances (metres), locations, and DCRNN's `adj_mx.pkl` through an unpickler that only allows numpy array reconstruction.
- `src/trafficml/data/graph.py`: builds the directed N x N road-distance matrix restricted to the listed sensors (inf where no distance), then the DCRNN Gaussian kernel `exp(-(d/sigma)^2)`. sigma is the std of finite entries of that filtered matrix; weights below `normalized_k` (0.1) are zeroed; the diagonal is 1. `without_self_loops` gives a zero-diagonal copy for neighbour features.
- `configs/data.yaml`: raw-file paths, 5-minute frequency, 0 mph null value, 12-step history/horizon, report horizons 3/6/12, provisional split fractions, kappa 0.1.
- `scripts/check_data.py`: rebuilds the adjacency and compares it with DCRNN's, then prints series range, shape, missing rate and split dates. `scripts/download_data.sh`: fetches the DCRNN graph files with curl and the speed files with gdown.
- Inputs: DCRNN `data/sensor_graph/*` files and `metr-la.h5` under `data/raw/` (not in Git). Outputs: in-memory arrays/DataFrames used by features, splits and models.
- Dependencies: numpy, pandas, PyTables, PyYAML; `check_data.py` also needs `trafficml.data.masking` and `trafficml.data.splits` (package 02-vridhi-features); the download script needs curl and gdown.

### Checks run

Environment: macOS (Darwin 25.0.0), existing Anaconda base Python 3.12.2 with numpy 1.26.4, pandas 2.3.3, tables 3.9.2, pytest 7.4.4. Nothing was installed. Run from the repository root with only this package present.

| Command | Outcome |
|---|---|
| `PYTHONPATH=src python -m pytest -q -ra -p no:cacheprovider` | 5 passed, 2 skipped (`test_real_speed_shape_frequency_and_sensor_order`, `test_adjacency_matches_dcrnn_pickle`: `data/raw` not downloaded) |
| `PYTHONPATH=src python scripts/check_data.py` | Failed: `ModuleNotFoundError: No module named 'trafficml.data.masking'` (package 02 not yet merged) |
| `python -m pyflakes src tests scripts` | No findings |
| `bash -n scripts/download_data.sh` | Syntax OK; script not run (no download authorized) |
| `ruff check .` / `ruff format --check .` | Not run: ruff not installed in available environments |

The data-dependent claims (shape 34,272 x 207, 2012-03-01 00:00 to 2012-06-27 23:55, sensor order and adjacency matching DCRNN) were **not** re-verified here because no raw data is present. The historical 56-test result is not a new run.

### Observations and open questions

- Timezone/DST of the naive timestamps, speed units (mph per the benchmark description) and raw-data redistribution terms remain unresolved, as stated in `docs/DATASET_CARD.md`.
- Speed-only scope: the loader reads a single speed matrix; no flow/occupancy channels exist. Faculty sign-off on that scope is still pending.
- `distance_matrix` silently keeps the last value if a (from, to) pair repeats in the CSV. No such check was possible without the data; not changed.
- `scripts/download_data.sh` is committed without the executable bit; run it as `bash scripts/download_data.sh`.

## Actual member activity (complete only after performing it)

- Performed on: pending (agent integration/review above on 2026-10-27)
- Registered on: 2026-10-27
- Files studied and explanation in your own words: pending
- Actual reproduction/check commands and environment: pending (agent checks recorded above)
- Actual outcomes, skips and failures: pending (agent results recorded above)
- Genuine fixes/tests/analysis/documentation added: none to code; this review log
- Assistance and existing work reused: prepared owner/AI-assisted source reused unchanged; integration, checks and this log written with Claude Code assistance
- Evidence paths or commit IDs: d084acd, 5c9888c, 7c20c56 on `codex/rudraksh-data`
- Reviewer and review date: pending human review
- Remaining limitations/questions: real-data checks, `check_data.py` after package 02, ruff, and combined verification are pending; see observations above
