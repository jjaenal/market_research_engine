---
title: Module Architecture
document_id: ARC-006
version: 1.0.0
status: Draft
category: Architecture
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-005
  - FND-009
  - FND-010
  - ARC-001
  - ARC-002
  - ARC-004
  - PRD-003
  - PRD-004

referenced_by:
  - ARC-005

purpose: Define the module layout of MRE and the contracts (interfaces) between engines
---

# Module Architecture

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ARC-006 mendefinisikan **module architecture** dari Market Research Engine (MRE).

Dokumen ini menjawab TODO-012 — Define Engine Interfaces (FND-008).

ARC-006 menetapkan:

- layout module fisik (package `src/`);
- kontrak interface antar engine;
- aturan dependensi (strategy tidak bergantung pada infrastructure yang tidak terkait).

---

# 2. Scope

Scope ARC-006:

- layout `src/`;
- interface engine (contracts);
- dependency rules;
- plugin contract (ringkas).

Di luar scope ARC-006:

- detail plugin design (ARC-005);
- event model detail (ARC-003);
- schema data (ARC-004);
- domain model (ARC-002).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- arsitek;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

ARC-001 menetapkan batas sistem:

```text
DATA → INDICATOR → DETECTOR → EVENT → SIGNAL → SIMULATION → STATISTICS → REPORTING → EVALUATE
```

ARC-006 menurunkan batas tersebut menjadi
layout module dan kontrak interface yang dapat diimplementasi.

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term      | Definition                                |
| --------- | ----------------------------------------- |
| Module    | Batas sistem dengan satu tanggung jawab   |
| Engine    | Modul yang memproses aliran data          |
| Interface | Kontrak input/output antar modul          |
| Plugin    | Ekstensi yang dapat ditambahkan tanpa mengubah core |

---

# 6. Module Layout

```text
src/
├── core/          # aturan inti, konfigurasi, determinism
├── models/        # domain entities (ARC-002)
├── loaders/       # import + validasi data (DATA)
├── indicators/    # perhitungan indikator (INDICATOR)
├── detectors/     # detektor event (DETECTOR, plugin)
├── engines/       # event/signal/simulation/statistics/reporting/experiment
├── reports/       # rendering report (REPORTING)
├── strategies/    # strategi sebagai plugin (STRATEGY)
└── utils/         # logging, helpers
```

Mapping ke ARC-001 module:

| ARC-001 Module | Package        |
| -------------- | -------------- |
| EXPERIMENT     | `engines/`     |
| DATA           | `loaders/`     |
| INDICATOR      | `indicators/`  |
| DETECTOR       | `detectors/`   |
| EVENT          | `engines/`     |
| SIGNAL         | `engines/`     |
| SIMULATION     | `engines/`     |
| STATISTICS     | `engines/`     |
| REPORTING      | `reports/`     |
| EVALUATE       | `engines/`     |

---

# 7. Engine Interfaces

## 7.1 DataEngine

- **Kontrak:** `load_dataset(source, config) → Dataset`; `validate(dataset) → ValidationResult`.
- **Workflow:** PRD-003 §7.1, §7.2.
- **Feature:** FEAT-001, FEAT-002.

## 7.2 IndicatorEngine

- **Kontrak:** `compute(dataset, indicator_params) → IndicatorSeries`.
- **Workflow:** PRD-003 §7.4 (input).
- **Feature:** FEAT-004.

## 7.3 EventEngine

- **Kontrak:** `detect(dataset, indicator_series, detector_set) → Event timeline`.
- **Workflow:** PRD-003 §7.4.
- **Feature:** FEAT-004.

## 7.4 SignalEngine

- **Kontrak:** `combine(events, signal_definition) → Signal list`.
- **Workflow:** PRD-003 §7.5.
- **Feature:** FEAT-005.

## 7.5 SimulationEngine

- **Kontrak:** `simulate(signals, execution_rules) → Trade ledger`.
- **Workflow:** PRD-003 §7.6.
- **Feature:** FEAT-006.

## 7.6 StatisticsEngine

- **Kontrak:** `calculate(trades, metric_selection) → Result`.
- **Workflow:** PRD-003 §7.7.
- **Feature:** FEAT-007.

## 7.7 ReportingEngine

- **Kontrak:** `render(result, config) → Report`.
- **Workflow:** PRD-003 §7.8.
- **Feature:** FEAT-008.

## 7.8 ExperimentEngine

- **Kontrak:** `run(experiment_config, dataset) → Report` (orchestrasi pipeline).
- **Workflow:** PRD-003 §7.3 + seluruh pipeline.
- **Feature:** FEAT-003, FEAT-009.

---

# 8. Dependency Direction

```text
DataEngine → IndicatorEngine → EventEngine → SignalEngine
     → SimulationEngine → StatisticsEngine → ReportingEngine

ExperimentEngine → orchestrasi seluruh engine (config)
```

Aturan:

- arah dependensi satu arah;
- tidak ada backward dependency;
- interface didefinisikan pada `core/` atau modul konsumen;
- tidak ada engine yang membaca state global (Article 6).

---

# 9. Plugin Contract

Per Article 11 (Plugin First) dan TODO-012 critical requirement:

> Strategy implementation must not
> directly depend on unrelated infrastructure.

Konsekuensi:

- detector/strategy plugin bergantung hanya pada interface inti
  (Event, Signal, konfigurasi), bukan pada engine/infrastructure;
- plugin dijalankan melalui konfigurasi (Article 12);
- detail kontrak plugin: ARC-005.

---

# 10. Traceability

| Item                | Requirement / Feature     |
| ------------------- | ------------------------- |
| Engine interfaces   | FR-001..FR-011            |
| Module layout       | NFR-008 (maintainability) |
| Dependency rules    | NFR-006 (extensibility)   |
| Plugin contract     | FR-012, Article 11        |

---

# 11. Compliance

| Constitution Article | Module requirement                     |
| -------------------- | -------------------------------------- |
| Article 6            | Stateless, tidak ada state global      |
| Article 7            | Deterministic                          |
| Article 11           | Plugin First                          |
| Article 12           | Configuration over hardcode           |
| Article 14           | Satu module satu tanggung jawab       |

---

# 12. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-004_Data_Architecture.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`

---

# 13. Revision History

| Version | Date       | Changes                 |
| ------- | ---------- | ----------------------- |
| 1.0.0   | 2026-08-08 | Initial module architecture |

---

**Document Status:** Draft

**Document ID:** ARC-006

**Version:** 1.0.0

**End of Document**
