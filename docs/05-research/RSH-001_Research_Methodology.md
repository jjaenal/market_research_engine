---
title: Research Methodology
document_id: RSH-001
version: 1.2.0
status: Approved
category: Research
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-11

depends_on:
  - FND-001
  - FND-005
  - FND-009
  - FND-010
  - ARC-001
  - ARC-002
  - ARC-007
  - PRD-001
  - PRD-003
  - PRD-004
  - PRD-005
  - PRD-006

referenced_by:
  - FND-006
  - FND-008
  - RSH-002
  - RSH-003

purpose: Define the research methodology for MRE — hypothesis, variables, metrics, sample, validation, and interpretation
---

# Research Methodology

> Measure the Market. Discover the Edge.

---

# 1. Purpose

RSH-001 mendefinisikan **research methodology** dari Market Research Engine (MRE).

Dokumen ini menjawab TODO-013 — Define Research Methodology (FND-008).

Pertanyaan utama (FND-007 §8):

> **Bagaimana kita memastikan experiment
> menghasilkan evidence yang meaningful?**

RSH-001 menetapkan:

- definisi hipotesis;
- baseline;
- variabel (control, independent, dependent);
- metrik;
- persyaratan sampel;
- validasi;
- interpretasi.

---

# 2. Scope

Scope RSH-001:

- metodologi penelitian (M3);
- kerangka untuk semua experiment MRE.

Di luar scope RSH-001:

- spesifikasi experiment spesifik (RSH-002, EXP-001);
- validasi detail (RSH-003);
- statistik detail (RSH-004);
- implementasi engine (M4).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- peneliti;
- quant analyst;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

MRE menguji hipotesis trading secara ilmiah (PRD-001 §7).

Initial research tidak mengejar `Maximum Profit`,
tetapi **Reliable Evidence** (FND-007 §11).

Keputusan evidence mengikuti prioritas (FND-005 §37):

> Research Evidence > Implementation Preference.

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term            | Definition                                        |
| --------------- | ------------------------------------------------- |
| Hypothesis      | Pernyataan yang diuji (edge yang dihipotesiskan) |
| Baseline        | Titik pembanding tanpa strategi                  |
| Evidence        | Fakta terukur dari experiment (FND-009)          |
| Experiment      | Unit penelitian terikat konfigurasi              |
| Signal          | Kombinasi Event (FND-009 §13)                    |
| Metrics         | Ukuran kuantitatif hasil eksperimen              |

---

# 6. Research Lifecycle

Per FND-007 §9:

```text
Question
   ↓
Hypothesis
   ↓
Dataset
   ↓
Configuration
   ↓
Experiment
   ↓
Observation
   ↓
Measurement
   ↓
Validation
   ↓
Conclusion
```

---

# 7. Hypothesis Definition

## 7.1 Form

Hipotesis dinyatakan dalam bentuk:

> Kondisi **X** (deteksi/Event) menghasilkan
> edge pada **Symbol** (Y) timeframe (**Z**).

Contoh:

> Break of Structure pada XAUUSD H1
> menghasilkan expectancy positif
> setelah biaya transaksi.

## 7.2 Kriteria

- dapat diuji (falsifiable);
- terikat dataset dan konfigurasi spesifik;
- dinyatakan sebelum experiment dijalankan (pre-registration).

---

# 8. Variables

## 8.1 Control Variables

Faktor yang ditetapkan tetap dalam experiment:

- dataset (symbol, timeframe, rentang);
- execution rules (biaya transaksi, slippage, sizing);
- validasi/konfigurasi lain yang bukan objek uji.

## 8.2 Independent Variables

Faktor yang divariasikan untuk menguji hipotesis:

- parameter strategi/detektor;
- parameter indikator.

## 8.3 Dependent Variables

Output yang diukur:

- metrics (FND-007 §11).

---

# 9. Baseline

Setiap experiment wajib memiliki baseline pembanding:

- **Buy & Hold** — reference sederhana;
- **No Trade** — reference tanpa aktivitas;
- perbandingan diukur pada rentang data yang sama.

Baseline didefinisikan di RSH-002 (Experiment Specification).

---

# 10. Metrics

Per FND-007 §11, metrik utama:

| Metric             | Definisi                                   |
| ------------------ | ------------------------------------------ |
| Win Rate           | Proporsi Trade menang                       |
| Loss Rate          | Proporsi Trade kalah                        |
| Risk/Reward        | Rasio expected loss vs gain                 |
| Expectancy         | Expected value per Trade                    |
| Profit Factor      | Gross profit / gross loss                   |
| Max Drawdown       | Penurunan terbesar equity                   |
| Sample Size        | Jumlah Trade                                |
| Return Distribution| Distribusi return Trade                     |
| Robustness         | Stabilitas hasil atas parameter/data       |

Detail statistik: RSH-004 (Statistical Methodology).

---

# 11. Sample Requirements

- jumlah Trade minimum untuk inferensi yang valid
  (ditetapkan pada RSH-004);
- sampel tidak cukup → evidence ditandai tidak cukup
  (PRD-004 FR-011);
- tidak ada alokasi sampel retroaktif setelah melihat hasil.

---

# 12. Validation

Per FND-007 §10:

- train/test separation — out-of-sample (TODO-025);
- walk-forward testing;
- sensitivity analysis (TODO-024);
- robustness analysis (TODO-026);
- Monte Carlo analysis jika relevan.

Jenis validasi dan urutan eksekusi:
RSH-003 (Validation Methodology).

---

# 13. Interpretation

- kesimpulan diturunkan dari evidence, bukan rekomendasi (PRD-003 §7.9);
- evidence tidak cukup ditandai secara eksplisit (FR-011);
- decision priority: Research Evidence (FND-005 §37);
- backtest adalah evidence, bukan bukti (FND-009);
- kriteria keputusan menggunakan **set standar** (RSH-004 §8.1);
- setiap experiment wajib mencantumkan **catatan multiple-testing**
  (RSH-004 §8.2) sehingga verdict antar experiment sebanding (E-8).

---

# 14. Execution Assumptions

Per FND-007 §10:

- entry/exit rules;
- position sizing;
- transaction costs;
- slippage;
- execution assumptions (simulasi, bukan live).

Assumption dicatat pada setiap eksperimen
dan dilaporkan (PRD-003 §7.8).

---

# 15. Traceability

| Item               | Requirement / TODO           |
| ------------------ | ---------------------------- |
| Hypothesis         | TODO-013                     |
| Metrics            | FND-007 §11, FR-007          |
| Validation         | TODO-024..026, RSH-003       |
| Interpretation     | FR-011, PRD-003 §7.9         |
| Evidence priority  | FND-005 §37                  |

---

# 16. Compliance

| Document / Rule       | Research requirement         |
| --------------------- | ---------------------------- |
| FND-001 Article 5     | Keputusan dapat dijelaskan   |
| FND-007 §11           | Reliable Evidence, bukan max profit |
| FND-009               | Backtest ≠ Proof             |
| PRD-004 FR-010        | Reproducibility experiment   |
| PRD-004 FR-011        | Evaluate Evidence            |

---

# 17. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/01-product/PRD-001_Product_Vision.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-005_Non_Functional_Requirements.md`
- `docs/01-product/PRD-006_MVP_Definition.md`

---

# 18. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.2.0   | 2026-08-11 | E-8: §13 now mandates the standardized decision criteria (RSH-004 §8.1) and the multiple-testing note (RSH-004 §8.2) |
| 1.1.0   | 2026-08-08 | Approved via M3 Research Review (RSH-006) |
| 1.0.0   | 2026-08-08 | Initial research methodology     |

---

**Document Status:** Approved

**Document ID:** RSH-001

**Version:** 1.2.0

**End of Document**
