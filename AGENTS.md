# AGENTS.md

Market Research Engine (MRE): a documentation-driven, event-driven framework for testing trading hypotheses (RSI Trendline Breakout baseline). **Phase M7 — Iteration is in progress** (per git history + FND-008 §7); M0–M6 are done.

## Current state (trust git history + FND-008 §7 TODO table; FND-006 prose lags)
- **Code and tests exist.** Package is `src/mre/` (`core`, `strategies`, `detectors`, `engines`, `indicators`, `loaders`, `models`, `utils`). The strategy plugin `strategies/exp001.py` registers the RSI Trendline Breakout signal definition under `EXP001_STRATEGY_ID`; `ExperimentConfig.strategy_id` resolves it from the registry (ARC-ACT-010).
- Next work is **ARC-008 §14 next research question — re-run EXP-001 with cooldown (deduplication) at realistic costs + regime selection** (M7 iteration). ARC-ACT-010 (Extract Strategy Plugin Package — `src/mre/strategies/` registry + `exp001.py`), ARC-ACT-011 (Move Experiment Config to External File — `configs/EXP-001.yaml` + `load_experiment_config()` in `src/mre/core/experiment_runner.py`, `--config` CLI flag), ARC-ACT-012 (Signal Deduplication — `SignalRule.cooldown` in `src/mre/models/signal_rule.py`, implemented in `combine()` at `src/mre/engines/signal_engine.py`, ENG-003 §8.1), ARC-ACT-013 (Unify Segment Runner — `src/mre/core/segments.py`: `run_on_slice()`, `SegmentRun`, `ensure_normalized()`, shared by OOS + robustness), and ARC-ACT-014 (Unify Renderers & Config Builder — `src/mre/utils/markdown.py` `heading`/`table`, `exp001_config()` in `src/mre/core/experiment_runner.py`, `src/mre/cli.py`) are DONE. TODO-025..028 and the M7 architecture review (ARC-008 — **CORE HOLDS, PERIPHERY DRIFTS**) are complete; M6 validation done.
- Foundation docs are **locked** (FND-010, approved). Docs are written in **Indonesian**; use FND-009 glossary terms (Event ≠ Signal ≠ Trade).
- **Docs drift is a known risk (R-005):** FND-006's status snapshot still says "M1 / Not Started" while its milestone table and FND-008 §7 say M6. When they conflict, trust git history and the FND-008 master TODO table.
- `datasets/`, `experiments/`, `reports/` are **gitignored but populated locally** (XAUUSD_H1.csv ~100k rows; EXP-001 report/sensitivity under `experiments/EXP-001/`). Never commit them. Tests use synthetic sine CSVs, never real data.

## Commands (exact)
- Run all tests: `.venv/bin/python -m pytest` (pyproject.toml sets `testpaths=["tests"]` and `pythonpath=["src"]`; pytest 9.1.1 installed in `.venv`).
- Run one file: `.venv/bin/python -m pytest tests/test_out_of_sample.py`
- Run a CLI module — **must** prepend `PYTHONPATH=src`; plain `python -m mre.core.*` raises `ModuleNotFoundError` because the package is not pip-installed (pyproject.toml has no `[project]` section):
  - **Unified entrypoint (ARC-ACT-014):** `PYTHONPATH=src .venv/bin/python -m mre.cli <subcommand>` where `<subcommand>` ∈ `baseline|sensitivity|oos|robustness`. The old per-module entrypoints still work (they delegate to `mre.cli`):
  - `PYTHONPATH=src .venv/bin/python -m mre.core.experiment_runner` — EXP-001 baseline (M5, done)
  - `PYTHONPATH=src .venv/bin/python -m mre.core.sensitivity` — TODO-024 (done)
  - `PYTHONPATH=src .venv/bin/python -m mre.core.out_of_sample` — TODO-025 (done)
  - `PYTHONPATH=src .venv/bin/python -m mre.core.robustness` — TODO-026 (done; `--no-market` to skip XAGUSD)
- **No linter/formatter is configured** (ruff/black are planned in DEV-002, not installed). Don't invent `ruff`/`black`/`mypy`/`flake8` commands.

## Architecture notes (not obvious from filenames)
- Pipeline: `normalize_raw_csv` → `load_dataset` → indicators (`rsi`) → `EventEngine.detect` → `signal_engine.combine` → `simulate` → `calculate` → `render` (markdown). Orchestrated in `compute_report()` (`src/mre/core/experiment_runner.py:63`).
- **Config is frozen dataclasses built from an external YAML file** (`ExperimentConfig`, `EventEngineConfig`, `ExecutionConfig`, `StatisticsConfig`); frozen EXP-001 parameters live in `configs/EXP-001.yaml` (committed, single source of truth — FR-012), loaded by `load_experiment_config()` (`src/mre/core/experiment_runner.py`) and wrapped by `exp001_config()`, which every CLI subcommand builds from (`--config` flag, ARC-ACT-011/014).
- **Strategies are plugins** (ARC-005 §6, ARC-ACT-010): `src/mre/strategies/` (`registry.py` — `register`/`get`/`registered_ids`; `exp001.py` registers `EXP001_STRATEGY_ID`). `ExperimentConfig.strategy_id` resolves `signal_definition` from the registry; the Signal Engine interface (`combine(events, signal_definition)`) is unchanged — add a strategy by registering, never by editing the engine.
- Engines implemented: event, signal, simulation, statistics, reporting. ENG-004 Probability Engine has no doc or impl (statistics engine covers it). Detectors: swing, price_confirmation, rsi_trendline. Indicators: rsi, ema, atr.
- Renderers (`reporting_engine.render` → `report.to_markdown`, `sensitivity.to_markdown`, `out_of_sample.to_markdown`, `robustness.to_markdown`) are pure string output and share the markdown helpers `heading`/`table` in `src/mre/utils/markdown.py` (ARC-ACT-014); file writes happen only in `run_experiment()` and CLI `main()`s.
- `mre/core/segments.py` (`run_on_slice`, `SegmentRun`, `ensure_normalized`) is the shared segment runner — OOS train/test and robustness period splits both go through it. It uses `mre/utils/candle_csv.py` (`write_candle_csv`) as the compliant segment CSV writer — reuse `run_on_slice`/`write_candle_csv` instead of hand-writing segment CSVs.

## Doc governance (when touching docs)
- New/updated docs need an ID from the FND-004 registry; creating or versioning a doc means syncing FND-004. ADRs go in `docs/06-decisions/`. Major architectural decisions require an ADR before implementation.
- Docs follow FND-002 front-matter/structure and are in **Indonesian**.
- Changes land via short-lived `feat/mN-*` branches merged to `main` through PRs (see git history).

## Coding standards (verified in the code)
- Type hints everywhere; frozen dataclasses for config; docstring on every public function/class; pure deterministic functions — no time/random sources, no future-candle lookahead (reproducibility is a hard requirement, Article 7).
- No `print` in business logic; `print` only in CLI `main()` entrypoints.
- One test file per module with `test_*` names and synthetic deterministic fixtures; correctness > performance.
