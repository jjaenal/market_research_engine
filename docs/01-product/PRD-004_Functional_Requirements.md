---
title: Functional Requirements
document_id: PRD-004
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
  - PRD-006
  - PRD-007
  - ARC-001

purpose: Define the functional requirements of MRE — what the system must be able to do
---

# Functional Requirements

> Measure the Market. Discover the Edge.

---

# 1. Purpose

PRD-004 mendefinisikan **functional requirements** dari Market Research Engine (MRE).

Dokumen ini menjawab TODO-006 — Define Functional Requirements (FND-008).

Setiap requirement diturunkan dari core workflow (PRD-003) dan harus dapat diverifikasi.

---

# 2. Scope

Scope PRD-004:

- kemampuan fungsional yang harus dimiliki MRE;
- acceptance criteria per requirement;
- matriks requirement terhadap workflow (PRD-003).

Di luar scope PRD-004:

- non-functional requirements (PRD-005);
- MVP definition (PRD-006);
- feature specification (PRD-007);
- detail implementasi (Fase M2 — Architecture).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- quantitative researcher;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

PRD-003 mendefinisikan pipeline 9 langkah:

```text
Import → Validate → Configure → Execute → Signals → Simulate → Statistics → Report → Evaluate
```

PRD-004 menurunkan pipeline tersebut menjadi daftar kemampuan yang dapat diuji dan diterima.

---

# 5. Definitions

Terminologi mengikuti **FND-009 — Project Glossary** (One Concept, One Name).

Istilah kunci:

| Term       | Definition                                |
| ---------- | ----------------------------------------- |
| Event      | Fakta atomik yang dihasilkan detektor     |
| Signal     | Kombinasi beberapa Event                  |
| Dataset    | Himpunan data historis yang immutable     |
| Experiment | Prosedur terkontrol untuk menguji hypothesis |

Apabila terjadi konflik terminologi, FND-009 lebih diutamakan.

---

# 6. Functional Requirements

## FR-001 — Load Historical Data

Sistem harus dapat memuat data historis dari file CSV menjadi Dataset.

- **Workflow source:** PRD-003 §7.1 (Import Dataset).
- **Acceptance criteria:**
  - menerima file CSV dengan kolom timestamp + OHLCV;
  - membangun Dataset immutable dari Candle;
  - menolak file dengan pesan error yang jelas apabila file/kolom/format tidak valid.

## FR-002 — Validate Data

Sistem harus dapat memvalidasi Dataset sebelum diproses lebih lanjut.

- **Workflow source:** PRD-003 §7.2 (Validate Dataset).
- **Acceptance criteria:**
  - mendeteksi timestamp duplikat, candle tidak urut, missing data, dan harga tidak wajar;
  - menghasilkan validation report;
  - menolak Dataset yang gagal validasi.

## FR-003 — Configure Experiment

Sistem harus dapat mengonfigurasi Experiment melalui konfigurasi YAML.

- **Workflow source:** PRD-003 §7.3 (Configure Experiment).
- **Acceptance criteria:**
  - mengikat symbol, timeframe, date range, dan strategy parameters;
  - mencatat assumptions;
  - membuat Experiment ID;
  - menolak konfigurasi tidak valid dengan pesan yang jelas.

## FR-004 — Execute Strategy

Sistem harus dapat menjalankan strategi sebagai pure functions dan menghasilkan Event.

- **Workflow source:** PRD-003 §7.4 (Execute Strategy).
- **Acceptance criteria:**
  - deterministic untuk input yang sama;
  - detektor menghasilkan Event, bukan rekomendasi;
  - menangani warm-up / data tidak cukup secara eksplisit.

## FR-005 — Generate Signals

Sistem harus dapat mengombinasikan Event menjadi Signal sesuai definisi Signal.

- **Workflow source:** PRD-003 §7.5 (Generate Signals).
- **Acceptance criteria:**
  - Signal dibangun dari Event berdasarkan aturan yang terdefinisi;
  - kombinasi ambigu ditandai atau ditolak.

## FR-006 — Simulate Trades

Sistem harus dapat mensimulasikan Trade dari Signal menggunakan execution rules.

- **Workflow source:** PRD-003 §7.6 (Simulate Trades).
- **Acceptance criteria:**
  - menerapkan position sizing, transaction cost, dan slippage;
  - menghasilkan Trade ledger per Experiment.

## FR-007 — Calculate Metrics

Sistem harus dapat menghitung metrik statistik dari Trade ledger.

- **Workflow source:** PRD-003 §7.7 (Calculate Statistics).
- **Acceptance criteria:**
  - metrik terdefinisi (win rate, expectancy, drawdown, dsb);
  - menangani jumlah Trade yang tidak cukup.

## FR-008 — Generate Trade Logs

Sistem harus dapat menghasilkan log Trade yang terstruktur.

- **Workflow source:** PRD-003 §7.6 output (Trade ledger).
- **Acceptance criteria:**
  - setiap Trade tercatat dengan timestamp dan konteks Signal;
  - log dapat dihubungkan ke satu Experiment ID.

## FR-009 — Generate Reports

Sistem harus dapat menghasilkan report yang terstruktur dan reproducible.

- **Workflow source:** PRD-003 §7.8 (Generate Report).
- **Acceptance criteria:**
  - report memuat konfigurasi, metadata dataset, metrik, dan area conclusion;
  - report terikat ke Experiment ID.

## FR-010 — Reproduce Experiments

Sistem harus dapat mereproduksi Experiment dengan hasil yang sama.

- **Workflow source:** lintas step.
- **Acceptance criteria:**
  - input yang sama (dataset + konfigurasi) menghasilkan output yang sama;
  - Experiment ID stabil untuk konfigurasi yang sama.

## FR-011 — Evaluate Evidence

Sistem harus dapat membandingkan hasil terhadap hypothesis dan menghasilkan conclusion.

- **Workflow source:** PRD-003 §7.9 (Evaluate Evidence).
- **Acceptance criteria:**
  - conclusion diturunkan dari evidence, bukan rekomendasi;
  - evidence tidak cukup ditandai secara eksplisit.

## FR-012 — Configuration over Hardcode

Sistem harus berperilaku berdasarkan konfigurasi, bukan nilai hardcode.

- **Workflow source:** FND-001 (Configuration over hardcode).
- **Acceptance criteria:**
  - strategy parameters dan execution rules berasal dari konfigurasi;
  - tidak ada parameter strategi yang di-hardcode di kode.

---

# 7. Requirement Matrix

| Requirement            | Workflow Step (PRD-003)   |
| ---------------------- | ------------------------- |
| FR-001 Load Data       | 7.1 Import Dataset        |
| FR-002 Validate Data   | 7.2 Validate Dataset      |
| FR-003 Configure       | 7.3 Configure Experiment  |
| FR-004 Execute Strategy | 7.4 Execute Strategy     |
| FR-005 Generate Signals | 7.5 Generate Signals     |
| FR-006 Simulate Trades | 7.6 Simulate Trades       |
| FR-008 Trade Logs      | 7.6 (output)              |
| FR-007 Calculate Metrics | 7.7 Calculate Statistics |
| FR-009 Generate Reports | 7.8 Generate Report      |
| FR-011 Evaluate Evidence | 7.9 Evaluate Evidence    |
| FR-010 Reproduce       | lintas step               |
| FR-012 Config over Hardcode | lintas step          |

---

# 8. Explicitly Not Required

Pada fase M1 dan Sprint 1, MRE **tidak** wajib mendukung:

- entry BUY/SELL;
- TP/SL;
- optimasi;
- machine learning;
- live trading / order execution;
- rekomendasi sinyal trading.

Kemampuan tersebut ditangani pada fase berikutnya.

---

# 9. Non-Functional Requirements

Non-functional requirements (performance, reproducibility, keamanan data, dsb) didefinisikan pada **PRD-005 — Non-Functional Requirements**.

---

# 10. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/01-product/PRD-001_Product_Vision.md`
- `docs/01-product/PRD-003_Core_Workflow.md`

---

# 11. Revision History

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 1.0.0   | 2026-08-08 | Initial functional requirements    |

---

**Document Status:** Draft

**Document ID:** PRD-004

**Version:** 1.0.0

**End of Document**
