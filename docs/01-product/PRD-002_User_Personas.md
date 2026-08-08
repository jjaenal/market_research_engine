---
title: User Personas
document_id: PRD-002
version: 1.0.0
status: Draft
category: Product
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

referenced_by:
  - PRD-007
  - ARC-001

purpose: Define the user personas of MRE — who uses MRE, their goals, pain points, and needs
---

# User Personas

> Measure the Market. Discover the Edge.

---

# 1. Purpose

PRD-002 mendefinisikan **user personas** dari Market Research Engine (MRE).

Dokumen ini menurunkan target users (PRD-001 §10) menjadi persona yang konkret:
profil, goals, pain points, dan kebutuhan terhadap MRE.

---

# 2. Scope

Scope PRD-002:

- persona per segmen pengguna;
- goals dan pain points;
- kebutuhan terhadap MRE;
- keterkaitan persona dengan core workflow (PRD-003).

Di luar scope PRD-002:

- functional requirements (PRD-004);
- non-functional requirements (PRD-005);
- MVP definition (PRD-006);
- feature specification (PRD-007).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- quantitative researcher;
- algorithmic trader;
- software engineer;
- data scientist;
- akademisi;
- komunitas open-source.

---

# 4. Background

MRE dibangun untuk menguji hipotesis trading secara ilmiah.

Untuk memastikan produk memenuhi kebutuhan nyata,
target users (PRD-001 §10) diuraikan menjadi persona.

Persona bukan data individual, melainkan representasi segmen pengguna.

---

# 5. Definitions

Terminologi mengikuti **FND-009 — Project Glossary** (One Concept, One Name).

Istilah kunci:

| Term       | Definition                                |
| ---------- | ----------------------------------------- |
| Experiment | Prosedur terkontrol untuk menguji hypothesis |
| Signal     | Kombinasi beberapa Event                  |
| Evidence   | Output research yang dapat direproduksi   |

Apabila terjadi konflik terminologi, FND-009 lebih diutamakan.

---

# 6. Personas

## 6.1 Raka — Quantitative Researcher

- **Profil:** peneliti kuantitatif, fokus pada pengujian strategi trading secara statistik.
- **Goals:** menguji hypothesis dengan evidence yang dapat direproduksi; membandingkan strategi secara objektif.
- **Pain points:** backtest tidak reproducible; keputusan didasarkan pada opini, bukan data.
- **Kebutuhan MRE:** reproducible experiments, metrik statistik, configuration-driven, evidence yang dapat dipercaya.
- **Workflow touchpoints:** PRD-003 §7.3, §7.7, §7.9 (Configure, Statistics, Evaluate).

## 6.2 Dina — Algorithmic Trader

- **Profil:** trader algoritmik yang mengevaluasi strategi sebelum eksekusi.
- **Goals:** memastikan strategi memiliki statistical edge; memisahkan signal dari noise.
- **Pain points:** overfitting; sulit membedakan signal vs noise; backtest disalahartikan sebagai bukti.
- **Kebutuhan MRE:** signal generation yang jelas, trade simulation, metrik risiko (drawdown), evaluasi objektif.
- **Workflow touchpoints:** PRD-003 §7.5, §7.6, §7.7 (Signals, Simulate, Statistics).

## 6.3 Bayu — Software Engineer

- **Profil:** engineer yang mengembangkan dan memperluas framework MRE.
- **Goals:** membangun modul modular dan testable; menambahkan detektor/indikator tanpa mengubah engine.
- **Pain points:** kode tidak testable; tidak ada standar engineering; konfigurasi tersebar di kode.
- **Kebutuhan MRE:** arsitektur modular (strategies as plugins), pure functions, unit-test first, dokumentasi yang jelas.
- **Workflow touchpoints:** seluruh pipeline (PRD-003); FR-012 (config over hardcode).

## 6.4 Sari — Data Scientist

- **Profil:** data scientist yang menganalisis market data.
- **Goals:** menganalisis data secara akurat; menghitung metrik dengan benar.
- **Pain points:** data tidak tervalidasi; metrik tidak konsisten antar eksperimen.
- **Kebutuhan MRE:** data validation, metrik terdefinisi eksplisit, reproducibility.
- **Workflow touchpoints:** PRD-003 §7.1, §7.2, §7.7 (Import, Validate, Statistics).

## 6.5 Prof. Wijaya — Akademisi

- **Profil:** akademisi yang meneliti trading dan keuangan.
- **Goals:** melakukan penelitian yang dapat diulang dan dipublikasikan.
- **Pain points:** hasil tidak dapat direproduksi; tidak ada dokumentasi eksperimen.
- **Kebutuhan MRE:** Experiment ID, dokumentasi, evidence yang dapat diaudit.
- **Workflow touchpoints:** PRD-003 §7.3, §7.8, §7.9 (Configure, Report, Evaluate).

## 6.6 Komunitas Open Source

- **Profil:** kontributor dan pengguna framework open-source.
- **Goals:** menggunakan dan memperluas framework; berbagi strategi.
- **Pain points:** onboarding sulit; ekstensi tidak didukung.
- **Kebutuhan MRE:** lisensi open-source, dokumentasi yang baik, ekstensibilitas (plugin).
- **Workflow touchpoints:** seluruh pipeline; dokumentasi (FND-002).

---

# 7. Persona Matrix

| Persona                | Primary Workflow Steps        | Primary Requirements      |
| ---------------------- | ----------------------------- | ------------------------- |
| Raka (Researcher)      | Configure, Statistics, Evaluate | FR-003, FR-007, FR-011  |
| Dina (Trader)          | Signals, Simulate, Statistics | FR-005, FR-006, FR-007    |
| Bayu (Engineer)        | Seluruh pipeline              | FR-012, NFR-005, NFR-006  |
| Sari (Data Scientist)  | Import, Validate, Statistics  | FR-001, FR-002, FR-007    |
| Prof. Wijaya (Akademisi) | Configure, Report, Evaluate | FR-003, FR-009, FR-011    |
| Komunitas Open Source  | Seluruh pipeline              | NFR-006, NFR-008          |

---

# 8. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/01-product/PRD-001_Product_Vision.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`

---

# 9. Revision History

| Version | Date       | Changes                  |
| ------- | ---------- | ------------------------ |
| 1.0.0   | 2026-08-08 | Initial user personas    |

---

**Document Status:** Draft

**Document ID:** PRD-002

**Version:** 1.0.0

**End of Document**
