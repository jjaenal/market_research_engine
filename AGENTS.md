# AGENTS.md

Market Research Engine (MRE): a documentation-driven, event-driven framework for testing trading hypotheses. Current sprint is **Sprint 0 — Foundation** (documentation phase, per FND-006); the PRD's "Sprint 1" names the future implementation sprint that builds the skeleton.

## Current state (verify before assuming)
- **No code or tests exist.** `src/` and `tests/` are empty scaffolds — loaders, models, engines, etc. are not written yet. Do not go looking for implementations.
- `src/` already has the intended package layout from the PRD (`core`, `models`, `loaders`, `indicators`, `detectors`, `engines`, `reports`, `utils`, `strategies`). Put new modules there; don't reorganize.
- `requirements.txt` is intentionally empty; there is **no `pyproject.toml`, no test runner, no linter configured**. Nothing can be installed or tested yet. Do not invent commands like `pytest`/`ruff` and expect them to work. `pytest`, `ruff`, and `black` are the *planned* standards (per PROJECT_CONTEXT), not installed.
- `.venv` exists (Python 3.13, no packages installed). Use `.venv/bin/python` rather than the system interpreter. `.venv/` is gitignored.
- `datasets/` is where CSV inputs go (per YAML config, e.g. `datasets/XAUUSD_H1.csv`); `experiments/` and `reports/` are for run output. All three are empty.

## Documentation-Driven Development
- `docs/` is the source of truth: when docs and code conflict, **docs take precedence**. Decision priority (per FND-005 §37): Project Charter > Architecture Constitution > Approved ADR > Product Requirements > Research Evidence > Implementation Preference.
- **Read `docs/00-foundation/FND-001_Project_Charter.md` before proposing architecture/code.** It defines the Architecture Constitution and Ubiquitous Language; code must change, never the constitution. Key rules: Event is the atomic unit (Signal aggregates Events); Detectors emit facts (Events), never recommendations; Indicators never produce trades; data is immutable; configuration over hardcode; new terms/architecture require an ADR.
- `docs/00-foundation/FND-005_Project_Context.md` (Active) is the authoritative project context: current phase is Foundation (documentation only) — **do not implement Python code until its requirements are documented**. Suggested reading order (FND-005 §48): README → FND-005 → FND-001 → FND-004 → relevant PRD/ARC/DEV. (`docs/context/PROJECT_CONTEXT.md` is the pre-FND-004 version, superseded by FND-005.)
- `docs/00-foundation/FND-006_Project_Status.md` (Active) is authoritative for current phase/sprint/milestone/next steps. As of now: all 9 Foundation docs are complete; next is a Foundation Review, then Product Definition. Check it before deciding what to work on.
- `docs/00-foundation/FND-007_Roadmap.md` (Active) defines the phased roadmap (M0 Foundation → M1 Product → M2 Architecture → M3 Research → M4 Engine → M5 Baseline Experiment → M6 Validation → M7 Iteration → M8 Expansion). MVP = one reproducible experiment from CSV to report.
- `docs/00-foundation/FND-008_TODO.md` (Active) is the execution backlog (statuses PLANNED/READY/IN_PROGRESS/BLOCKED/REVIEW/DONE/DEFERRED/CANCELLED, priorities P0–P3). M1 Product Definition comes after the Foundation Review.
- `docs/00-foundation/FND-009_Project_Glossary.md` (Active) is the controlled vocabulary for docs, code, and experiments (One Concept, One Name; e.g. Order ≠ Trade ≠ Position, Signal ≠ Trade). Use its terms, don't invent synonyms.
- `docs/00-foundation/FND-002_Documentation_Standard.md` (Approved) governs doc structure: front-matter (title, document_id, version, status, category, owner, created, last_updated, depends_on, referenced_by); structure (Purpose, Scope, Audience, Background, Definitions, Main Content, Examples, References, Revision History). Docs are written in **Indonesian**.
- `docs/00-foundation/FND-003_Document_ID_Standard.md` (Approved) governs document IDs: format `<PREFIX>-<NNN>` with prefixes FND/PRD/ARC/ENG/DEV/RSH/ADR/EXP/TMP/REF. Numbers are 3-digit, sequential per category, **immutable and never reused**. File names are `<PREFIX>-<NNN>_<PascalCase>.md` (e.g. `FND-003_Document_ID_Standard.md`); the front-matter `document_id` is the identity, the filename may change. Cross-reference other docs by ID (e.g. "See FND-003").
- `docs/00-foundation/FND-004_Document_Index.md` (Active) is the official registry of all doc IDs, paths, versions, and statuses. **Check it before creating a doc** (duplicate prevention); a doc not listed there is not official. Every new doc must be added to FND-004 (workflow: assign ID → create doc → update FND-004). Note: FND-004 is currently out of sync — FND-005 through FND-009 exist (Active) but are still listed as `Planned`; update the index when it lags (FND-004 §25).
- New docs go in the numbered category folders under `docs/`: `00-foundation` … `05-research`, plus `06-decisions` (ADRs), `07-experiments`, `08-templates`, `09-reference`. Note: per FND-004, ADRs go in `docs/06-decisions/`, not the older empty `docs/adr/` (which only exists from the pre-FND-004 layout). (The `NN_Document_Name.md` example in `docs/README.md` is outdated.)
- Major architectural decisions must be recorded as an ADR in `docs/06-decisions/` before implementation.

## Architecture (per docs/Market_Research_Engine_PRD_Sprint1.md)
- Data flow: CSV → Data Loader → Validator → Domain Models → Detector Layer → Event Engine → Probability Engine → Trading Engine (future) → Reports.
- Core principles: event-driven; pure functions (deterministic); reproducible experiments; config over hardcode (YAML); unit-test first; strategies as plugins.
- Domain models: Candle, Swing, Trendline, IndicatorSeries, Event, Signal, Trade.

## Coding standards (for when code is added)
- Type hints; dataclasses when appropriate; pure functions; **no `print` in business logic** (use a logger with INFO/WARNING/ERROR levels); docstring for every public class/function.
- Sprint 1 excludes buy/sell entries, TP/SL, optimization, and ML.
