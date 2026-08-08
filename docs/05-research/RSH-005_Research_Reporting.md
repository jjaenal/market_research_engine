---
title: Research Reporting
document_id: RSH-005
version: 1.1.0
status: Approved
category: Research
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-005
  - FND-009
  - FND-010
  - ARC-002
  - ARC-004
  - ARC-007
  - PRD-003
  - PRD-004
  - PRD-007
  - RSH-001
  - RSH-002
  - RSH-004

referenced_by:
  - FND-006
  - FND-008
  - ENG-007
  - EXP-001

purpose: Define the research reporting requirements for MRE to satisfy the M3 exit criterion "research reporting requirements tersedia"
---

# Research Reporting

> Measure the Market. Discover the Edge.

---

# 1. Purpose

RSH-005 mendefinisikan **research reporting requirements** dari Market Research Engine (MRE).

Dokumen ini menjawab kriteria exit M3
"research reporting requirements tersedia" (FND-007 §12).

RSH-005 menetapkan:

- struktur report;
- isi setiap section report;
- format dan reproducibility report;
- pelaporan evidence dan conclusion.

Dokumen ini menjadi acuan FEAT-008 (Report Generator)
dan ENG-007 (Reporting Engine) pada M4.

---

# 2. Scope

Scope RSH-005:

- struktur dan isi report;
- format output;
- reproducible reporting.

Di luar scope RSH-005:

- statistik detail (RSH-004);
- spesifikasi experiment (RSH-002);
- implementasi ReportingEngine (ENG-007, M4).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- peneliti;
- quant analyst;
- implementor ReportingEngine;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per PRD-003 §7.8, report harus
**terstruktur dan reproducible**, terikat Experiment ID.

Per PRD-007 FEAT-008, report memuat:
**konfigurasi, metadata dataset, metrik, dan area conclusion.**

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term            | Definition                                        |
| --------------- | ------------------------------------------------- |
| Report          | Output terstruktur dari experiment (FEAT-008)     |
| Experiment ID   | Identitas unik experiment (RSH-002 §7)            |
| Evidence        | Fakta terukur dari experiment (FND-009)           |
| Conclusion      | Interpretasi evidence (RSH-001 §13)               |

---

# 6. Report Structure

Report terdiri atas section berikut:

| Section                   | Isi                                         |
| ------------------------- | ------------------------------------------- |
| Header                    | Experiment ID, judul, tanggal, code version |
| Hypothesis                | Hipotesis yang diuji (RSH-001 §7)           |
| Dataset                   | Metadata dataset (ARC-004), date range, timeframe |
| Configuration             | Parameter (control + independent)           |
| Assumptions               | Execution & cost assumptions (RSH-001 §14)  |
| Metrics                   | Metrik minimum (RSH-002 §8, RSH-004)        |
| Evidence & Conclusion     | Evidence assessment dan conclusion (FR-011) |
| Reproducibility           | Code version, konfigurasi frozen, dataset immutable |

---

# 7. Section Detail

## 7.1 Header

```text
Experiment ID: EXP-001
Title: RSI Trendline Breakout Baseline
Date: YYYY-MM-DD
Code Version: <git commit>
```

## 7.2 Hypothesis

- pernyataan hipotesis (RSH-001 §7.1);
- baseline pembanding (RSH-001 §9).

## 7.3 Dataset

- symbol, timeframe, date range;
- dataset_version (ARC-004);
- integrity status (ARC-004).

## 7.4 Configuration

- seluruh parameter terkunci (frozen, PRD-003 §7.3);
- control dan independent variables (RSH-001 §8).

## 7.5 Assumptions

- execution assumptions (entry/exit, sizing);
- cost assumptions (biaya transaksi, slippage).

## 7.6 Metrics

- metrik minimum (RSH-002 §8):
  Trade Count, Win/Loss Rate, Average Win/Loss,
  Risk/Reward, Expectancy, Profit Factor,
  Gross Profit/Loss, Net P&L, Max Drawdown, streaks;
- dibandingkan dengan baseline.

## 7.7 Evidence & Conclusion

- evidence cukup / tidak cukup (RSH-004 §9, FR-011);
- conclusion diturunkan dari evidence, bukan rekomendasi (PRD-003 §7.9);
- evidence tidak cukup ditandai eksplisit.

## 7.8 Reproducibility

- code version (engine + git commit);
- konfigurasi frozen;
- dataset immutable (Article 13);
- input yang sama → output yang sama (NFR-001, FEAT-009).

---

# 8. Output Format

- report dalam format terstruktur yang dapat di-parse
  (Markdown + blok data terstruktur);
- output reproducible dan deterministic (FR-010);
- report disimpan terikat Experiment ID;
- tidak ada komponen interaktif/mutasi setelah render (Article 13).

---

# 9. Reporting Lifecycle

```text
Statistik + konfigurasi + metadata dataset (PRD-003 §7.7)
    ↓
Susun report terstruktur (FEAT-008)
    ↓
Report terikat Experiment ID
    ↓
Evaluate evidence (PRD-003 §7.9)
```

---

# 10. Traceability

| Item              | Requirement / Feature     |
| ----------------- | ------------------------- |
| Report structure  | FR-009, FEAT-008          |
| Reproducibility   | FR-010, NFR-001, FEAT-009 |
| Evidence          | FR-011, PRD-003 §7.9      |
| Exit criterion    | FND-007 §12               |

---

# 11. Compliance

| Document / Rule       | Reporting requirement     |
| --------------------- | ------------------------- |
| FND-009               | Backtest ≠ Proof          |
| PRD-003 §7.8          | Report terstruktur, reproducible |
| PRD-003 §7.9          | Conclusion, bukan rekomendasi |
| PRD-004 FR-011        | Evaluate Evidence         |
| PRD-007 FEAT-008      | Report memuat config, metadata, metrik, conclusion |
| Article 13            | Report immutable setelah render |

---

# 12. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-004_Data_Architecture.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-007_Feature_Specification.md`
- `docs/05-research/RSH-001_Research_Methodology.md`
- `docs/05-research/RSH-002_Experiment_Specification.md`
- `docs/05-research/RSH-004_Statistical_Methodology.md`

---

# 13. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.1.0   | 2026-08-08 | Approved via M3 Research Review (RSH-006) |
| 1.0.0   | 2026-08-08 | Initial research reporting       |

---

**Document Status:** Approved

**Document ID:** RSH-005

**Version:** 1.1.0

**End of Document**
