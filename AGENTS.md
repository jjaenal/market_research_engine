# AGENTS.md

Market Research Engine (MRE): a documentation-driven, event-driven framework for testing trading hypotheses (RSI Trendline Breakout baseline). **Phase M6 — Validation is in progress** (per git history + FND-008 §7); M0–M5 are done.

## Current state (trust git history + FND-008 §7 TODO table; FND-006 prose lags)
- **Code and tests exist.** Package is `src/mre/` (`core`, `detectors`, `engines`, `indicators`, `loaders`, `models`, `utils`). There is **no `strategies/` package yet** — the one strategy is `_exp001_signal_definition()` in `src/mre/core/experiment_runner.py`.
- Next work is **TODO-025 Out-of-Sample Testing** (PLANNED). WIP already exists on `main` but is **untracked**: `src/mre/core/out_of_sample.py` + `tests/test_out_of_sample.py` (module complete; the 400-candle fixture produces baseline trades; all tests pass).
- Foundation docs are **locked** (FND-010, approved). Docs are written in **Indonesian**; use FND-009 glossary terms (Event ≠ Signal ≠ Trade).
- **Docs drift is a known risk (R-005):** FND-006's status snapshot still says "M1 / Not Started" while its milestone table and FND-008 §7 say M6. When they conflict, trust git history and the FND-008 master TODO table.
- `datasets/`, `experiments/`, `reports/` are **gitignored but populated locally** (XAUUSD_H1.csv ~100k rows; EXP-001 report/sensitivity under `experiments/EXP-001/`). Never commit them. Tests use synthetic sine CSVs, never real data.

## Commands (exact)
- Run all tests: `.venv/bin/python -m pytest` (pyproject.toml sets `testpaths=["tests"]` and `pythonpath=["src"]`; pytest 9.1.1 installed in `.venv`).
- Run one file: `.venv/bin/python -m pytest tests/test_out_of_sample.py`
- Run a CLI module — **must** prepend `PYTHONPATH=src`; plain `python -m mre.core.*` raises `ModuleNotFoundError` because the package is not pip-installed (pyproject.toml has no `[project]` section):
  - `PYTHONPATH=src .venv/bin/python -m mre.core.experiment_runner` — EXP-001 baseline (M5, done)
  - `PYTHONPATH=src .venv/bin/python -m mre.core.sensitivity` — TODO-024 (done)
  - `PYTHONPATH=src .venv/bin/python -m mre.core.out_of_sample` — TODO-025 (in progress)
- **No linter/formatter is configured** (ruff/black are planned in DEV-002, not installed). Don't invent `ruff`/`black`/`mypy`/`flake8` commands.

## Architecture notes (not obvious from filenames)
- Pipeline: `normalize_raw_csv` → `load_dataset` → indicators (`rsi`) → `EventEngine.detect` → `signal_engine.combine` → `simulate` → `calculate` → `render` (markdown). Orchestrated in `compute_report()` (`src/mre/core/experiment_runner.py:63`).
- **Config is frozen dataclasses, not YAML** (`ExperimentConfig`, `EventEngineConfig`, `ExecutionConfig`, `StatisticsConfig`); parameters are hardcoded in `_exp001_signal_definition()` and CLI defaults. The docs' "config over hardcode (YAML)" is aspirational, not implemented.
- Engines implemented: event, signal, simulation, statistics, reporting. ENG-004 Probability Engine has no doc or impl (statistics engine covers it). Detectors: swing, price_confirmation, rsi_trendline. Indicators: rsi, ema, atr.
- Render (`reporting_engine.render`, `sensitivity.to_markdown`, `out_of_sample.to_markdown`) is pure string output; file writes happen only in `run_experiment()` and CLI `main()`s.

## Doc governance (when touching docs)
- New/updated docs need an ID from the FND-004 registry; creating or versioning a doc means syncing FND-004. ADRs go in `docs/06-decisions/`. Major architectural decisions require an ADR before implementation.
- Docs follow FND-002 front-matter/structure and are in **Indonesian**.
- Changes land via short-lived `feat/mN-*` branches merged to `main` through PRs (see git history).

## Coding standards (verified in the code)
- Type hints everywhere; frozen dataclasses for config; docstring on every public function/class; pure deterministic functions — no time/random sources, no future-candle lookahead (reproducibility is a hard requirement, Article 7).
- No `print` in business logic; `print` only in CLI `main()` entrypoints.
- One test file per module with `test_*` names and synthetic deterministic fixtures; correctness > performance.
