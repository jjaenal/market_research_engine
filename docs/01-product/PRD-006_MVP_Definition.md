---
title: MVP Definition
document_id: PRD-006
version: 1.1.0
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
  - PRD-003
  - PRD-004

referenced_by:
  - PRD-007
  - ARC-001

purpose: Define the MVP scope of MRE — one complete research workflow from CSV to report
---

# MVP Definition

> Measure the Market. Discover the Edge.

---

# 1. Purpose

PRD-006 mendefinisikan **Minimum Viable Product (MVP)** dari Market Research Engine (MRE).

Dokumen ini menjawab TODO-007 — Define MVP (FND-008).

---

# 2. Scope

Scope PRD-006:

- prinsip MVP;
- batas MVP (in-scope);
- batas bukan-MVP (out-of-scope);
- success criteria MVP.

Di luar scope PRD-006:

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

Per FND-007 roadmap, MVP adalah:

> Satu experiment yang reproducible dari CSV hingga report.

MVP harus membuktikan bahwa seluruh pipeline dapat berjalan, bukan membangun banyak fitur.

---

# 5. Definitions

Terminologi mengikuti **FND-009 — Project Glossary** (One Concept, One Name).

Istilah kunci:

| Term       | Definition                                |
| ---------- | ----------------------------------------- |
| Event      | Fakta atomik yang dihasilkan detektor     |
| Signal     | Kombinasi beberapa Event                  |
| Experiment | Prosedur terkontrol untuk menguji hypothesis |
| Backtest   | Metode; bukan bukti (Backtest ≠ Proof)    |

Apabila terjadi konflik terminologi, FND-009 lebih diutamakan.

---

# 6. MVP Principle

MVP:

> Satu complete research workflow.

Bukan:

> Banyak fitur.

MVP berhasil apabila membuktikan alur lengkap
dari data hingga report secara reproducible.

---

# 7. MVP Boundary

```text
CSV
 ↓
Validation
 ↓
Strategy
 ↓
Signal
 ↓
Simulation
 ↓
Statistics
 ↓
Report
```

---

# 8. In-Scope (MVP)

## 8.1 CSV

- Satu format input: file CSV dengan kolom timestamp + OHLCV (misal `XAUUSD_H1.csv`).
- Mapping kolom ke Candle domain objects.

## 8.2 Validation

- Validasi inti: urutan waktu, duplikasi, missing data, dan nilai tidak wajar.

## 8.3 Strategy

- Paling sedikit satu strategi contoh yang berjalan (strategy sebagai plugin).
- Menjalankan detektor/indikator dan menghasilkan Event.

## 8.4 Signal

- Mengombinasikan Event menjadi Signal berdasarkan definisi Signal.

## 8.5 Simulation

- Simulasi Trade dari Signal menggunakan execution rules dasar (position sizing, transaction cost, slippage).

## 8.6 Statistics

- Metrik inti: win rate, expectancy, drawdown, dan metrik pendukung.

## 8.7 Report

- Report terstruktur dan reproducible dengan Experiment ID.

---

# 9. Out of MVP

Pada MVP, hal berikut **tidak** termasuk:

- banyak sumber data (satu format CSV saja);
- validasi lanjutan;
- banyak strategi/indikator;
- optimasi;
- machine learning;
- entry BUY/SELL;
- TP/SL;
- live trading / order execution;
- Evaluate Evidence otomatis (7.9 pada PRD-003) — conclusion ditentukan secara manual oleh peneliti;
- UI/dashboard (MVP berupa CLI).

---

# 10. Success Criteria

MVP dinyatakan berhasil apabila:

- satu experiment dapat dijalankan dari CSV hingga report;
- hasil reproducible — input yang sama menghasilkan output yang sama;
- report memuat metrik yang dapat dievaluasi terhadap hypothesis;
- experiment dijalankan dengan konfigurasi (config over hardcode);
- seluruh langkah terverifikasi (unit-test).

---

# 11. Relationship to Roadmap

- M1 — Product Definition: mendefinisikan scope MVP (dokumen ini).
- M4 — Engine Implementation: membangun MVP.
- M5 — Baseline Experiment: menjalankan experiment baseline pertama (EXP-001).

---

# 12. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-007_Roadmap.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/01-product/PRD-001_Product_Vision.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`

---

# 13. Revision History

| Version | Date       | Changes               |
| ------- | ---------- | --------------------- |
| 1.1.0    | 2026-08-08 | Approved via M1 Product Definition Review (PRD-008) |
| 1.0.0   | 2026-08-08 | Initial MVP definition |

---

**Document Status:** Approved

**Document ID:** PRD-006

**Version:** 1.1.0

**End of Document**
