# AGENTS.md

Market Research Engine (MRE): a documentation-driven, event-driven framework for testing trading hypotheses (Sprint 1 = "Project Skeleton").

## Current state (verify before assuming)
- **No code or tests exist.** `src/` and `tests/` are empty scaffolds — loaders, models, engines, etc. are not written yet. Do not go looking for implementations.
- `src/` already has the intended package layout from the PRD (`core`, `models`, `loaders`, `indicators`, `detectors`, `engines`, `reports`, `utils`, `strategies`). Put new modules there; don't reorganize.
- `requirements.txt` is intentionally empty; there is **no `pyproject.toml`, no test runner, no linter configured**. Nothing can be installed or tested yet. Do not invent commands like `pytest`/`ruff` and expect them to work. `pytest`, `ruff`, and `black` are the *planned* standards (per PROJECT_CONTEXT), not installed.
- `.venv` exists (Python 3.13, no packages installed). Use `.venv/bin/python` rather than the system interpreter. `.venv/` is gitignored.
- `datasets/` is where CSV inputs go (per YAML config, e.g. `datasets/XAUUSD_H1.csv`); `experiments/` and `reports/` are for run output. All three are empty.

## Documentation-Driven Development
- `docs/` is the source of truth. Per `docs/README.md`: when docs and code conflict, **docs take precedence** until officially updated.
- `docs/context/PROJECT_CONTEXT.md` declares the current phase (Sprint 1, documentation only) and an AI-rule: **do not implement Python code until its requirements are documented**. Read it before proposing architecture/code.
- Docs are written in **Indonesian**; follow that language and the `NN_Document_Name.md` naming convention for new docs.
- New docs go in the numbered category folders under `docs/` (`00-foundation`, `01-product`, `02-architecture`, `03-engine`, `04-development`, `05-research`); ADRs go in `docs/adr/`.
- Every document has metadata (title, project, version, status, owner, last_updated) and required sections (Purpose, Scope, Dependencies, References, Changelog).
- Major architectural decisions must be recorded in `docs/adr/` before implementation.

## Architecture (per docs/Market_Research_Engine_PRD_Sprint1.md)
- Data flow: CSV → Data Loader → Validator → Domain Models → Detector Layer → Event Engine → Probability Engine → Trading Engine (future) → Reports.
- Core principles: event-driven; pure functions (deterministic); reproducible experiments; config over hardcode (YAML); unit-test first; strategies as plugins.
- Domain models: Candle, Swing, Trendline, IndicatorSeries, Event, Signal, Trade.

## Coding standards (for when code is added)
- Type hints; dataclasses when appropriate; pure functions; **no `print` in business logic** (use a logger with INFO/WARNING/ERROR levels); docstring for every public class/function.
- Sprint 1 excludes buy/sell entries, TP/SL, optimization, and ML.
