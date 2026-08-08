---
title: Experiment Specification
document_id: RSH-002
version: 1.0.0
status: Draft
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
  - PRD-005
  - RSH-001

referenced_by:
  - FND-006
  - FND-008
  - EXP-001

purpose: Define the experiment specification — what every experiment captures, metrics, and record lifecycle
---

# Experiment Specification

> Measure the Market. Discover the Edge.

---

# 1. Purpose

RSH-002 mendefinisikan **experiment specification** dari Market Research Engine (MRE).

Dokumen ini menjawab TODO-014 — Define Experiment Specification (FND-008).

RSH-002 menetapkan:

- field wajib yang dicatat setiap experiment;
- konvensi Experiment ID;
- metrik minimum;
- siklus hidup record experiment.

---

# 2. Scope

Scope RSH-002:

- format/field spesifikasi experiment;
- konvensi identitas experiment;
- metrik minimum (FND-008 §25).

Di luar scope RSH-002:

- metodologi penelitian umum (RSH-001);
- validasi detail (RSH-003);
- statistik detail (RSH-004);
- experiment spesifik (EXP-001).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- peneliti;
- quant analyst;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per FND-005, Research Evidence adalah sumber prioritas keputusan.

Setiap experiment harus dapat diulang dan direkam
dengan lengkap agar evidence dapat diverifikasi (FR-010, NFR-001).

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term            | Definition                                        |
| --------------- | ------------------------------------------------- |
| Experiment      | Unit penelitian terikat konfigurasi              |
| Experiment ID   | Identitas unik experiment                         |
| Code Version    | Versi kode/engine yang menjalankan experiment    |
| Result          | Output terukur (metrics) dari experiment         |
| Conclusion      | Interpretasi evidence (RSH-001 §13)              |

---

# 6. Experiment Specification Fields

Setiap experiment wajib mencatat (TODO-014):

| Field                   | Deskripsi                                  |
| ----------------------- | ------------------------------------------ |
| Experiment ID           | Identitas unik experiment (RSH-002 §7)     |
| Strategy                | Strategi/plugin yang diuji                 |
| Dataset                 | Dataset yang digunakan (ARC-004 metadata)  |
| Date Range              | Rentang data (start, end)                  |
| Timeframe               | Timeframe candle (H1, H4, …)               |
| Parameters              | Konfigurasi parameter (control + independent, RSH-001 §8) |
| Execution Assumptions   | Asumsi eksekusi (entry/exit, sizing)       |
| Cost Assumptions        | Biaya transaksi, slippage                  |
| Code Version            | Versi kode/engine (git)                    |
| Result                  | Metrics output                             |
| Conclusion              | Kesimpulan dari evidence                   |

---

# 7. Experiment ID Convention

Format:

```text
EXP-<NNN>
```

Contoh: `EXP-001` (RSI Trendline Breakout Baseline).

- nomor 3-digit, sekuensial (FND-003);
- immutable, tidak pernah dipakai ulang;
- terdaftar di FND-004 registry.

---

# 8. Minimum Metrics

Per FND-008 §25:

```text
Trade Count
Win Rate
Loss Rate
Average Win
Average Loss
Risk/Reward
Expectancy
Profit Factor
Gross Profit
Gross Loss
Net P&L
Maximum Drawdown
Winning Streak
Losing Streak
```

Additional metrics dapat ditambahkan
setelah baseline engine stabil (FND-008 §25).

---

# 9. Reproducibility

Per FR-010 dan RSH-001 §7.2:

- konfigurasi terkunci (frozen) sebelum experiment dijalankan (PRD-003 §7.3);
- Code Version dicatat (versi engine + git commit);
- dataset immutable (Article 13, ARC-004);
- run yang sama → output yang sama (NFR-001).

---

# 10. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)
    ↓
Run (eksperimen dijalankan)
    ↓
Result (metrics dicatat)
    ↓
Conclusion (interpretasi evidence)
    ↓
Reviewed (validasi, RSH-003)
```

Setiap record experiment disimpan
sebagai dokumen EXP (FND-003).

---

# 11. Traceability

| Item              | Requirement / TODO           |
| ----------------- | ---------------------------- |
| Spec fields       | TODO-014                     |
| Metrics minimum   | FND-008 §25, FR-007          |
| Experiment ID     | FND-003, FR-010              |
| Reproducibility   | FR-010, NFR-001              |
| Conclusion        | FR-011, RSH-001 §13          |

---

# 12. Compliance

| Document / Rule       | Experiment requirement       |
| --------------------- | ---------------------------- |
| FND-003               | ID immutable, sekuensial     |
| FND-005 §37           | Research Evidence priority   |
| FND-009               | Backtest ≠ Proof             |
| PRD-004 FR-010        | Reproducibility experiment   |
| PRD-004 FR-011        | Evaluate Evidence            |
| Article 13            | Dataset immutable            |

---

# 13. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-004_Data_Architecture.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-005_Non_Functional_Requirements.md`
- `docs/05-research/RSH-001_Research_Methodology.md`

---

# 14. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial experiment specification |

---

**Document Status:** Draft

**Document ID:** RSH-002

**Version:** 1.0.0

**End of Document**
