---
title: System Architecture
document_id: ARC-001
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
  - PRD-001
  - PRD-003
  - PRD-004
  - PRD-005
  - PRD-006
  - PRD-007
  - PRD-008

referenced_by:
  - ARC-002
  - ARC-003
  - ARC-004
  - ARC-005
  - ARC-006

purpose: Define the major system boundaries of MRE and how modules relate, honoring the Architecture Constitution (FND-001)
---

# System Architecture

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ARC-001 mendefinisikan **system architecture** dari Market Research Engine (MRE).

Dokumen ini menjawab TODO-009 — Define System Architecture (FND-008).

ARC-001 menetapkan:

- batas major sistem (module boundaries);
- hubungan dan arah dependensi antar modul;
- kesesuaian dengan Architecture Constitution (FND-001 §14).

---

# 2. Scope

Scope ARC-001:

- system context dan pipeline utama;
- module boundaries;
- dependency direction;
- compliance terhadap konstitusi.

Di luar scope ARC-001:

- domain model detail (ARC-002);
- event architecture (ARC-003);
- data architecture (ARC-004);
- plugin architecture (ARC-005);
- module/physical layout (ARC-006);
- implementasi teknis.

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- arsitek;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Product phase (M1) menghasilkan pipeline yang disetujui (PRD-003):

```text
Import → Validate → Configure → Execute → Signals → Simulate → Statistics → Report → Evaluate
```

ARC-001 menurunkan pipeline tersebut menjadi
batas sistem yang terpisah dan testable,
sesuai Architecture Constitution (FND-001 §14).

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name)
dan Architecture Constitution (FND-001 §14).

Istilah kunci:

| Term       | Definition                                |
| ---------- | ----------------------------------------- |
| Event      | Fakta atomik yang dihasilkan detektor     |
| Signal     | Kombinasi beberapa Event                  |
| Module     | Batas sistem dengan satu tanggung jawab   |
| Engine     | Modul yang memproses aliran data          |

---

# 6. Architectural Principles

Arsitektur MRE tunduk pada prinsip berikut (FND-001 §14, FND-005):

1. Event adalah unit atomik (Article 1).
2. Detector independen satu sama lain (Article 2).
3. Detector menghasilkan fakta, bukan rekomendasi (Article 3).
4. Signal adalah agregasi evidence (Article 4).
5. Keputusan harus dapat dijelaskan (Article 5).
6. Business logic stateless (Article 6).
7. Processing deterministik (Article 7).
8. Indicator tidak pernah mengeksekusi Trade (Article 8).
9. Report Engine read-only (Article 9).
10. Probability Engine independen (Article 10).
11. Plugin First (Article 11).
12. Configuration over hardcoding (Article 12).
13. Data immutable (Article 13).
14. Satu module satu tanggung jawab (Article 14).
15. Keputusan besar wajib ADR (Article 15).

---

# 7. System Context

```text
CSV
 │
 ▼
┌──────────────┐     ┌───────────────────┐
│ DATA         │     │ EXPERIMENT        │
│ Load         │     │ Configure + ID    │
│ Validate     │     │ Reproduce         │
└──────┬───────┘     └─────────┬─────────┘
       ▼                       │
┌──────────────┐               │
│ INDICATOR    │               │ config
└──────┬───────┘               │
       ▼                       │
┌──────────────┐               │
│ DETECTOR     │───────────────┘
└──────┬───────┘
       ▼
┌──────────────┐
│ EVENT        │
└──────┬───────┘
       ▼
┌──────────────┐
│ SIGNAL       │
└──────┬───────┘
       ▼
┌──────────────┐
│ SIMULATION   │
└──────┬───────┘
       ▼
┌──────────────┐
│ STATISTICS   │
└──────┬───────┘
       ▼
┌──────────────┐
│ REPORTING    │
└──────┬───────┘
       ▼
┌──────────────┐
│ EVALUATE     │  (di luar MVP)
└──────────────┘
```

---

# 8. Module Boundaries

## 8.1 EXPERIMENT

- **Responsibility:** konfigurasi, orchestration, dan reproducibility experiment.
- **Workflow source:** PRD-003 §7.3 (Configure Experiment).
- **Requirements/features:** FR-003, FR-010, FR-012; FEAT-003, FEAT-009.
- **Constitutional constraint:** Configuration over hardcoding (Article 12); determinism (Article 7).

## 8.2 DATA

- **Responsibility:** memuat dan memvalidasi dataset; menyediakan Candle domain objects.
- **Workflow source:** PRD-003 §7.1, §7.2.
- **Requirements/features:** FR-001, FR-002; FEAT-001, FEAT-002.
- **Constitutional constraint:** Data immutable (Article 13).

## 8.3 INDICATOR

- **Responsibility:** menghitung series indikator dari data.
- **Workflow source:** PRD-003 §7.4 (input).
- **Requirements/features:** FR-004; FEAT-004.
- **Constitutional constraint:** Indicator tidak pernah mengeksekusi Trade (Article 8).

## 8.4 DETECTOR

- **Responsibility:** menghasilkan Event dari data dan indicator series.
- **Workflow source:** PRD-003 §7.4.
- **Requirements/features:** FR-004; FEAT-004.
- **Constitutional constraint:** menghasilkan fakta, bukan rekomendasi (Article 3); independen satu sama lain (Article 2).

## 8.5 EVENT

- **Responsibility:** mengelola timeline Event sebagai unit atomik.
- **Workflow source:** PRD-003 §7.4 output.
- **Constitutional constraint:** Event adalah unit atomik (Article 1).

## 8.6 SIGNAL

- **Responsibility:** mengombinasikan Event menjadi Signal; integrasi antar detektor.
- **Workflow source:** PRD-003 §7.5.
- **Requirements/features:** FR-005; FEAT-005.
- **Constitutional constraint:** Signal adalah agregasi evidence (Article 4); keputusan dapat dijelaskan (Article 5).

## 8.7 SIMULATION

- **Responsibility:** mensimulasikan Trade dari Signal menggunakan execution rules.
- **Workflow source:** PRD-003 §7.6.
- **Requirements/features:** FR-006, FR-008; FEAT-006.
- **Constitutional constraint:** single responsibility (Article 14); bukan eksekusi live.

## 8.8 STATISTICS

- **Responsibility:** menghitung metrik statistik dari Trade ledger.
- **Workflow source:** PRD-003 §7.7.
- **Requirements/features:** FR-007; FEAT-007.

## 8.9 REPORTING

- **Responsibility:** menyusun report terstruktur dan reproducible.
- **Workflow source:** PRD-003 §7.8.
- **Requirements/features:** FR-009; FEAT-008.
- **Constitutional constraint:** read-only (Article 9).

## 8.10 EVALUATE

- **Responsibility:** membandingkan hasil terhadap hypothesis; menghasilkan conclusion.
- **Workflow source:** PRD-003 §7.9.
- **Requirements/features:** FR-011; FEAT-010.
- **Status:** di luar MVP (PRD-006 §9).

---

# 9. Dependency Direction

```text
DATA → INDICATOR → DETECTOR → EVENT → SIGNAL → SIMULATION → STATISTICS → REPORTING → EVALUATE

EXPERIMENT (config) → seluruh modul (input konfigurasi, bukan dependensi eksekusi)
```

Aturan:

- arah dependensi satu arah (tidak ada backward dependency);
- config mengalir dari EXPERIMENT ke setiap modul;
- tidak ada modul yang membaca state global (Article 6).

---

# 10. Config Flow

```text
YAML config
   ↓
EXPERIMENT (frozen)
   ↓
DATA bounds (symbol/timeframe/date range)
INDICATOR parameters (window)
DETECTOR thresholds
SIGNAL rules
SIMULATION execution rules
STATISTICS metric selection
REPORTING format
```

Tidak ada parameter hardcode (Article 12).

---

# 11. Compliance with Architecture Constitution

| Article | Requirement                        | Compliance          |
| ------- | ---------------------------------- | ------------------- |
| 1       | Event unit atomik                  | Modul EVENT         |
| 2       | Detector independen                | Modul DETECTOR      |
| 3       | Detector fakta, bukan rekomendasi  | Modul DETECTOR      |
| 4       | Signal agregasi evidence           | Modul SIGNAL        |
| 5       | Keputusan explainable              | Modul SIGNAL        |
| 6       | Business logic stateless           | Seluruh modul       |
| 7       | Deterministic                      | Seluruh modul       |
| 8       | Indicator tidak execute trade      | Modul INDICATOR     |
| 9       | Report read-only                   | Modul REPORTING     |
| 10      | Probability Engine independen      | Masa depan (ADR)    |
| 11      | Plugin First                       | Modul DETECTOR/SIGNAL (ARC-005) |
| 12      | Config over hardcode               | Modul EXPERIMENT    |
| 13      | Data immutable                     | Modul DATA          |
| 14      | Satu module satu tanggung jawab    | Seluruh modul       |
| 15      | Keputusan besar wajib ADR          | ADR yang diperlukan |

---

# 12. Future Boundaries

Tidak termasuk MVP (PRD-006), tetapi sudah ditetapkan batasannya:

- **Probability Engine** — independent, hanya menerima Event (Article 10); wajib ADR saat dibangun.
- **Trading Engine** — eksekusi live; di luar scope (PRD-001 §11).
- **ML Research Layer** — deferred (FND-008 TODO-031).

---

# 13. Traceability to Product

| Module     | Workflow Step (PRD-003) | Feature (PRD-007) |
| ---------- | ----------------------- | ----------------- |
| EXPERIMENT | 7.3                     | FEAT-003, FEAT-009 |
| DATA       | 7.1, 7.2                | FEAT-001, FEAT-002 |
| INDICATOR  | 7.4                     | FEAT-004           |
| DETECTOR   | 7.4                     | FEAT-004           |
| EVENT      | 7.4                     | FEAT-004           |
| SIGNAL     | 7.5                     | FEAT-005           |
| SIMULATION | 7.6                     | FEAT-006           |
| STATISTICS | 7.7                     | FEAT-007           |
| REPORTING  | 7.8                     | FEAT-008           |
| EVALUATE   | 7.9                     | FEAT-010 (non-MVP) |

---

# 14. Required ADRs

Per Article 15, keputusan berikut wajib memiliki ADR
(dicatat di `docs/06-decisions/`):

- event-driven architecture;
- plugin architecture;
- swing algorithm;
- trendline algorithm;
- probability model (saat dibangun).

---

# 15. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/01-product/PRD-001_Product_Vision.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-005_Non_Functional_Requirements.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `docs/01-product/PRD-007_Feature_Specification.md`
- `docs/01-product/PRD-008_Product_Definition_Review.md`

---

# 16. Revision History

| Version | Date       | Changes                     |
| ------- | ---------- | --------------------------- |
| 1.0.0   | 2026-08-08 | Initial system architecture |

---

**Document Status:** Draft

**Document ID:** ARC-001

**Version:** 1.0.0

**End of Document**
