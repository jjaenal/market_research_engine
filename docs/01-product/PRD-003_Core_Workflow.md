---
title: Core Workflow
document_id: PRD-003
version: 1.1.1
status: Approved
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

referenced_by:
  - PRD-004
  - PRD-006
  - ARC-001

purpose: Define the core research workflow of MRE — every major step with its input, processing, output, and failure conditions
---

# Core Workflow

> Measure the Market. Discover the Edge.

---

# 1. Purpose

PRD-003 mendefinisikan **core research workflow** dari Market Research Engine (MRE) pada level produk.

Dokumen ini menjawab TODO-005 — Define Core Research Workflow (FND-008).

Setiap major step pada workflow harus memiliki:

- input;
- processing;
- output;
- failure conditions.

---

# 2. Scope

Scope PRD-003:

- workflow utama MRE dari data hingga evidence;
- spesifikasi setiap step (input, processing, output, failure);
- prinsip yang mengatur alur data.

Di luar scope PRD-003:

- functional requirements (PRD-004);
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

Agar sebuah experiment dapat direproduksi, alur dari data hingga evidence harus didefinisikan secara eksplisit.

Workflow ini adalah jembatan antara product vision (PRD-001) dan implementasi (Fase M4 — Engine).

PRD-001 mendefinisikan alur penelitian:

```text
Research Question → Hypothesis → Experiment → Event → Signal → Metrics → Evidence → Conclusion
```

PRD-003 menurunkan alur tersebut menjadi pipeline operasional yang dapat dieksekusi.

---

# 5. Definitions

Terminologi mengikuti **FND-009 — Project Glossary** (One Concept, One Name).

Istilah kunci:

| Term            | Definition                                |
| --------------- | ----------------------------------------- |
| Event           | Fakta atomik yang dihasilkan detektor     |
| Signal          | Kombinasi beberapa Event                  |
| Dataset         | Himpunan data historis yang immutable     |
| Experiment      | Prosedur terkontrol untuk menguji hypothesis |
| Backtest        | Metode; bukan bukti (Backtest ≠ Proof)    |

Apabila terjadi konflik terminologi, FND-009 lebih diutamakan.

---

# 6. Core Workflow

```text
Import Dataset
      ↓
Validate Dataset
      ↓
Configure Experiment
      ↓
Execute Strategy
      ↓
Generate Signals
      ↓
Simulate Trades
      ↓
Calculate Statistics
      ↓
Generate Report
      ↓
Evaluate Evidence
```

---

# 7. Step Specification

## 7.1 Import Dataset

- **Input:** file data historis (CSV), metadata (symbol, timeframe).
- **Processing:** membaca file, memetakan kolom ke OHLCV, membangun Candle domain objects.
- **Output:** Dataset yang immutable beserta metadata-nya.
- **Failure conditions:** file tidak ditemukan; format CSV tidak valid; kolom wajib hilang; format timestamp tidak dikenal.

## 7.2 Validate Dataset

- **Input:** Dataset dari step 7.1.
- **Processing:** memeriksa kelengkapan, urutan waktu, duplikasi, missing data, dan nilai di luar rentang wajar.
- **Output:** Dataset yang tervalidasi dan validation report.
- **Failure conditions:** timestamp duplikat; candle tidak urut; missing data melebihi ambang; harga tidak wajar (≤ 0, dsb).

## 7.3 Configure Experiment

- **Input:** Experiment Configuration (YAML), pilihan dataset.
- **Processing:** membaca dan mengikat konfigurasi, mencatat assumptions, membuat Experiment ID.
- **Output:** definisi Experiment yang terkunci (frozen).
- **Failure conditions:** YAML tidak valid; symbol/timeframe tidak dikenal; parameter wajib tidak ada; parameter saling bertentangan.

## 7.4 Execute Strategy

- **Input:** Dataset tervalidasi + Experiment configuration.
- **Processing:** menjalankan detektor/indikator sebagai pure functions; detektor menghasilkan Event.
- **Output:** timeline Event.
- **Failure conditions:** aturan strategi tidak terdefinisi; detektor gagal; data tidak cukup (warm-up).

## 7.5 Generate Signals

- **Input:** timeline Event dari step 7.4.
- **Processing:** mengombinasikan Event menjadi Signal sesuai definisi Signal.
- **Output:** stream Signal.
- **Failure conditions:** definisi Signal tidak ada; kombinasi Event ambigu.

## 7.6 Simulate Trades

- **Input:** Signal dari step 7.5.
- **Processing:** mengevaluasi behavior Signal menjadi simulated trades dengan execution rules (position sizing, transaction cost, slippage).
- **Output:** Trade ledger (log Trade hasil simulasi).
- **Failure conditions:** semantik Signal tidak valid; execution rules tidak ada.

Catatan: pada Sprint 1, entry BUY/SELL, TP/SL, optimasi, dan ML berada di luar scope (lihat PRD-001 §11). Step ini adalah simulasi riset, bukan eksekusi live.

## 7.7 Calculate Statistics

- **Input:** Trade ledger, timeline Event/Signal, konfigurasi.
- **Processing:** menghitung metrik statistik (win rate, expectancy, drawdown, dsb).
- **Output:** hasil statistik yang terukur.
- **Failure conditions:** jumlah Trade tidak cukup; formula metrik tidak terdefinisi.

## 7.8 Generate Report

- **Input:** statistik + konfigurasi + metadata dataset.
- **Processing:** menyusun laporan terstruktur dan reproducible.
- **Output:** report dengan Experiment ID.
- **Failure conditions:** metrik hilang; error rendering report.

## 7.9 Evaluate Evidence

- **Input:** report dari step 7.8.
- **Processing:** membandingkan hasil terhadap hypothesis; menerapkan kriteria statistik.
- **Output:** evidence dan conclusion (bukan rekomendasi).
- **Failure conditions:** evidence tidak cukup; hasil ambigu.

---

# 8. Step Matrix

| Step                  | Input                | Output              | Main Failure                |
| --------------------- | -------------------- | ------------------- | --------------------------- |
| Import Dataset        | CSV + metadata       | Dataset             | file/format tidak valid     |
| Validate Dataset      | Dataset              | Dataset + report    | duplikasi/missing data      |
| Configure Experiment  | YAML config          | Experiment terkunci | konfigurasi tidak valid     |
| Execute Strategy      | Dataset + config     | Timeline Event      | aturan tidak terdefinisi    |
| Generate Signals      | Timeline Event       | Stream Signal       | definisi Signal tidak ada   |
| Simulate Trades       | Signal               | Trade ledger        | execution rules tidak ada   |
| Calculate Statistics  | Trade ledger         | Statistics          | Trade tidak cukup           |
| Generate Report       | Statistics           | Report              | metrik hilang               |
| Evaluate Evidence     | Report               | Evidence            | evidence tidak cukup        |

---

# 9. Guiding Principles

Workflow tunduk pada prinsip berikut:

- **Event adalah unit atomik** — Signal mengagregasi Event (FND-001);
- **Detector menghasilkan fakta, bukan rekomendasi** — Detector memancarkan Event;
- **Indicator tidak pernah menghasilkan Trade**;
- **Data bersifat immutable**;
- **Configuration over hardcode** — Experiment Configuration dari YAML;
- **Pure functions** — setiap step deterministik dan dapat direproduksi;
- **Backtest ≠ proof** — report adalah evidence, bukan keputusan.

## 9.1 Event Semantics

Terdapat dua makna "Event" yang berbeda dan tidak boleh dicampur:

- **Event arsitektur** (mekanisme): fakta atomik yang dihasilkan detektor
  pada step 7.4. Ini adalah unit dasar dari pipeline MRE.
- **"Event Detection"** (capability produk): kemampuan calon masa depan
  yang tercantum pada FND-010 §32 (Portfolio Scanner, Market Regime, dsb).

Kandidat capability tersebut tidak otomatis menjadi MVP feature
(lihat PRD-006 §9 dan PRD-008 §7).

---

# 10. Explicitly Out of Scope

Pada fase M1 dan Sprint 1, workflow ini **tidak** mencakup:

- entry BUY/SELL;
- TP/SL;
- optimasi;
- machine learning;
- live trading / order execution;
- rekomendasi sinyal trading.

---

# 11. Relationship to PRD-001

PRD-001 mendefinisikan alur penelitian level konsep:

```text
Research Question → Hypothesis → Experiment → Event → Signal → Metrics → Evidence → Conclusion
```

PRD-003 mendefinisikan pipeline operasional yang menjalankan alur tersebut dari data hingga evidence.

---

# 12. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/01-product/PRD-001_Product_Vision.md`

---

# 13. Revision History

| Version | Date       | Changes                   |
| ------- | ---------- | ------------------------- |
| 1.1.1   | 2026-08-08 | Clarify Event semantics (PRD-ACT-003)                   |
| 1.1.0   | 2026-08-08 | Approved via M1 Product Definition Review (PRD-008)     |
| 1.0.0   | 2026-08-08 | Initial core workflow     |

---

**Document Status:** Approved

**Document ID:** PRD-003

**Version:** 1.1.1

**End of Document**
