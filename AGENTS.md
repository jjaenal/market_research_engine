# AGENTS.md

Market Research Engine (MRE): a documentation-driven, event-driven framework for testing trading hypotheses. The Foundation phase is **APPROVED and LOCKED** (per FND-010); the next phase is **M1 — Product Definition** (TODO-004…008 in FND-008), then the implementation sprint. **No code or tests exist yet.**

## Current state (verify before assuming)
- **No code or tests exist.** `src/` and `tests/` are empty scaffolds — loaders, models, engines, etc. are not written. Do not go looking for implementations.
- `src/` already has the intended package layout (`core`, `models`, `loaders`, `indicators`, `detectors`, `engines`, `reports`, `utils`, `strategies`). Put new modules there; don't reorganize.
- `requirements.txt` is intentionally empty; there is **no `pyproject.toml`, no test runner, no linter configured**. Nothing can be installed or tested. Do not invent commands like `pytest`/`ruff` and expect them to work; `pytest`, `ruff`, and `black` are planned, not installed.
- `.venv` exists (Python 3.13, no packages). Use `.venv/bin/python` rather than the system interpreter. `.venv/` is gitignored.
- `datasets/` (CSV inputs, e.g. `datasets/XAUUSD_H1.csv`), `experiments/`, and `reports/` (run output) are all empty **and gitignored** — don't commit data.
- **Foundation cleanup pending:** FND-010 approved the Foundation with 4 outstanding P1 actions (FND-ACT-001…004). FND-ACT-004 (sync the doc index) is still open: **FND-010 is missing from the FND-004 index**, and `docs/README.md` still uses the stale `NN_Name.md` naming and `docs/adr/` layout.
- Changes land via short-lived branches + PRs (see git history).

## Documentation-Driven Development
- `docs/` is the source of truth: when docs and code conflict, **docs take precedence**. Decision priority (per FND-005 §37): Project Charter > Architecture Constitution > Approved ADR > Product Requirements > Research Evidence > Implementation Preference.
- **Read `docs/00-foundation/FND-001_Project_Charter.md` before proposing architecture/code.** It defines the Architecture Constitution and Ubiquitous Language; code must change, never the constitution. Key rules: Event is the atomic unit (Signal aggregates Events); Detectors emit facts (Events), never recommendations; Indicators never produce trades; data is immutable; configuration over hardcode; new terms/architecture require an ADR.
- `docs/00-foundation/FND-005_Project_Context.md` (Active) is the authoritative project context: **do not implement Python code until its requirements are documented**. Suggested reading order (FND-005 §48): README → FND-005 → FND-001 → FND-004 → relevant PRD/ARC/DEV. (`docs/context/PROJECT_CONTEXT.md` is the pre-FND-004 version, superseded by FND-005.)
- `docs/00-foundation/FND-010_Foundation_Review.md` (v1.0.0, Approved) is the formal gate: Foundation = **APPROVED / LOCKED** (0 blockers, 95% readiness, "PASS WITH ACTIONS"). **Foundation docs are locked — material changes require a Change Request → Impact Analysis, not casual edits.**
- `docs/00-foundation/FND-006_Project_Status.md` (Active) is authoritative for phase/sprint/milestone/next steps — **but it and FND-008 trail FND-010**: they still say Foundation / Sprint 0 / IN_PROGRESS and list TODO-003 (Foundation Review) as PLANNED, though the review is done and approved. Treat FND-010 as the gate authority.
- `docs/00-foundation/FND-007_Roadmap.md` (Active) defines the phased roadmap (M0 Foundation → M1 Product → M2 Architecture → M3 Research → M4 Engine → M5 Baseline Experiment → M6 Validation → M7 Iteration → M8 Expansion). MVP = one reproducible experiment from CSV to report.
- `docs/00-foundation/FND-008_TODO.md` (Active) is the execution backlog (statuses PLANNED/READY/IN_PROGRESS/BLOCKED/REVIEW/DONE/DEFERRED/CANCELLED, priorities P0–P3). Next work is M1 Product Definition (TODO-004 Define Product Vision → TODO-008).
- `docs/00-foundation/FND-009_Project_Glossary.md` (Active) is the controlled vocabulary (One Concept, One Name; e.g. Order ≠ Trade ≠ Position, Signal ≠ Trade). Use its terms, don't invent synonyms.
- `docs/00-foundation/FND-002_Documentation_Standard.md` (Approved) governs doc structure: front-matter (title, document_id, version, status, category, owner, created, last_updated, depends_on, referenced_by); structure (Purpose, Scope, Audience, Background, Definitions, Main Content, Examples, References, Revision History). Docs are written in **Indonesian**.
- `docs/00-foundation/FND-003_Document_ID_Standard.md` (Approved) governs document IDs: format `<PREFIX>-<NNN>` with prefixes FND/PRD/ARC/ENG/DEV/RSH/ADR/EXP/TMP/REF. Numbers are 3-digit, sequential per category, **immutable and never reused**. File names are `<PREFIX>-<NNN>_<PascalCase>.md`; the front-matter `document_id` is the identity, the filename may change. Cross-reference other docs by ID (e.g. "See FND-003").
- `docs/00-foundation/FND-004_Document_Index.md` (Active) is the official registry of all doc IDs, paths, versions, and statuses. **Check it before creating a doc** (duplicate prevention); a doc not listed there is not official. Workflow: assign ID → create doc → update FND-004, and keep it synced on every version/status change (FND-004 §25). Known gap: FND-010 hasn't been added yet.
- New docs go in the numbered category folders under `docs/`: `00-foundation` … `05-research`, plus `06-decisions` (ADRs), `07-experiments`, `08-templates`, `09-reference`. Per FND-004, ADRs go in `docs/06-decisions/`, not the legacy empty `docs/adr/`. (`docs/README.md` is stale: outdated naming example and `docs/adr/` layout.)
- Major architectural decisions must be recorded as an ADR in `docs/06-decisions/` before implementation.

## Architecture (per docs/Market_Research_Engine_PRD_Sprint1.md)
- Data flow: CSV → Data Loader → Validator → Domain Models → Detector Layer → Event Engine → Probability Engine → Trading Engine (future) → Reports.
- Core principles: event-driven; pure functions (deterministic); reproducible experiments; config over hardcode (YAML); unit-test first; strategies as plugins.
- Domain models: Candle, Swing, Trendline, IndicatorSeries, Event, Signal, Trade.

## Coding standards (for when code is added)
- Type hints; dataclasses when appropriate; pure functions; **no `print` in business logic** (use a logger with INFO/WARNING/ERROR levels); docstring for every public class/function.
- Sprint 1 (implementation) excludes buy/sell entries, TP/SL, optimization, and ML.
