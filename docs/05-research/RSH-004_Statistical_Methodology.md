---
title: Statistical Methodology
document_id: RSH-004
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
  - ARC-007
  - PRD-004
  - PRD-005
  - RSH-001
  - RSH-002
  - RSH-003

referenced_by:
  - FND-006
  - FND-008
  - RSH-001
  - RSH-002
  - RSH-003

purpose: Define the statistical methodology for MRE — metric formulas, sample size, significance, and evidence thresholds
---

# Statistical Methodology

> Measure the Market. Discover the Edge.

---

# 1. Purpose

RSH-004 mendefinisikan **statistical methodology** dari Market Research Engine (MRE).

Dokumen ini menurunkan metrik dari RSH-001 §10
dan persyaratan sampel dari RSH-001 §11
menjadi formula dan threshold yang dapat dieksekusi.

RSH-004 menetapkan:

- formula metrik;
- persyaratan ukuran sampel;
- threshold evidence;
- interpretasi statistik.

---

# 2. Scope

Scope RSH-004:

- formula metrik (RSH-001 §10, FND-008 §25);
- persyaratan sampel minimum;
- threshold evidence;
- prosedur penilaian evidence.

Di luar scope RSH-004:

- metodologi umum (RSH-001);
- spesifikasi experiment (RSH-002);
- validasi (RSH-003).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- peneliti;
- quant analyst;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per RSH-001 §10, metrik utama MRE:

```text
Win Rate, Loss Rate, Risk/Reward, Expectancy,
Profit Factor, Max Drawdown, Sample Size,
Return Distribution, Robustness
```

Metrik dihitung dari Trade ledger (PRD-003 §7.7).

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term      | Definition                                        |
| --------- | ------------------------------------------------- |
| Trade     | Hasil eksekusi simulasi (FND-009 §15)            |
| Expectancy| Expected value per Trade                         |
| Sample    | Kumpulan Trade hasil eksperimen                  |
| Evidence  | Fakta terukur dari experiment                    |

---

# 6. Metric Formulas

## 6.1 Win Rate

```text
Win Rate = jumlah Trade menang / jumlah Trade total
```

## 6.2 Loss Rate

```text
Loss Rate = jumlah Trade kalah / jumlah Trade total
```

## 6.3 Average Win / Average Loss

```text
Average Win  = total profit Trade menang / jumlah Trade menang
Average Loss = total loss Trade kalah  / jumlah Trade kalah
```

## 6.4 Risk/Reward

```text
Risk/Reward = Average Win / Average Loss
```

## 6.5 Expectancy

```text
Expectancy = (Win Rate × Average Win) − (Loss Rate × Average Loss)
```

## 6.6 Profit Factor

```text
Profit Factor = Gross Profit / Gross Loss
```

## 6.7 Net P&L

```text
Net P&L = Gross Profit − Gross Loss
```

## 6.8 Maximum Drawdown

```text
Max Drawdown = penurunan maksimum equity dari peak ke trough
```

## 6.9 Streaks

```text
Winning Streak = deret Trade menang terpanjang
Losing Streak  = deret Trade kalah terpanjang
```

---

# 7. Sample Requirements

- jumlah Trade minimum untuk inferensi valid
  ditetapkan per experiment (RSH-002) dengan batas bawah default:
  - minimum 30 Trade untuk perhitungan statistik dasar;
  - sampel lebih besar diperlukan untuk edge tipis.
- sampel tidak cukup → evidence ditandai tidak cukup
  (PRD-004 FR-011).

---

# 8. Evidence Thresholds

| Ukuran              | Threshold default                       |
| ------------------- | --------------------------------------- |
| Trade count         | ≥ 30 (dasar), lebih besar untuk edge tipis |
| Expectancy          | > 0 setelah biaya transaksi (net)       |
| Profit Factor       | > 1 setelah biaya transaksi             |
| Robustness          | hasil stabil pada parameter/data beragam|

Threshold dapat dikonfigurasi per experiment (RSH-002).

## 8.1 Standardized Decision Criteria (E-8)

Audit menemukan kriteria keputusan **drift** antar experiment: EXP-002
di-declare SUPPORTED tanpa kriteria stasionaritas yang kemudian menolak
EXP-007/008, sehingga verdict tidak saling sebanding (R-005). Mulai
eksperimen berikutnya, set kriteria **standar** (dapat ditambah dengan
justifikasi eksplisit, tidak boleh dikurangi tanpa justifikasi):

```text
SUPPORTED hanya jika SEMUA terpenuhi:
  1. expectancy > 0 pada skenario representative (biaya venue aktual,
     1.0 bps/side) dengan n >= min_sample (30);
  2. biaya breakeven/side >= biaya venue aktual (>= 1.0 bps);
  3. OOS test expectancy > 0 (edge bertahan out-of-sample);
  4. OOS train expectancy > 0 (stasionaritas temporal).

REJECTED jika salah satu tidak terpenuhi.
```

- Set deviasi dari set standar **harus** didokumentasikan di §13
  experiment beserta alasannya (mis. threshold breakeven dinaikkan
  mengikuti kontrol experiment sebelumnya — EXP-003/004).
- Setiap experiment wajib mencantumkan seluruh kriteria di §13
  secara eksplisit; tidak boleh mereferensikan experiment lain.

## 8.2 Multiple-Testing / Data-Snooping Control (E-8)

Audit menemukan **tidak ada kontrol multiple-testing** formal; grid
robustness yang degenerate memperparahnya (R-005/R-006). Setiap
experiment wajib mencantumkan **catatan multiple-testing** di §13:

```text
- jumlah kriteria keputusan yang diuji:  <N>;
- jumlah kombinasi parameter (combo grid): <N>;
- jumlah slice temporal / split point:     <N>;
- jumlah dimensi robustness:               <N>;
- koreksi / penalty yang diterapkan:       <none | Bonferroni | pre-registered
                                           rule, sebutkan eksplisit>.
```

Prinsip:

- tidak ada koreksi → pernyataan risiko data-snooping eksplisit;
- jika koreksi diterapkan, threshold expectancy/kriteria disesuaikan
  sebelum run (pre-registered), bukan sesudahnya;
- hasil yang bertahan setelah kontrol dianggap lebih kuat evidence;
- grid yang memvariasikan parameter yang tidak dikonsumsi strategi
  **dilarang** (robustness harus bermakna — RSH-003 §10, E-7).

---

# 9. Evidence Assessment

Per RSH-001 §13 dan FR-011:

- evidence cukup jika sampel terpenuhi dan threshold tercapai;
- evidence tidak cukup ditandai eksplisit;
- kesimpulan diturunkan dari evidence, bukan rekomendasi.

---

# 10. Distribution Analysis

- Return Distribution dihitung dari return Trade;
- menilai skewness dan ekor distribusi;
- digunakan untuk menilai risiko (drawdown, tail).

---

# 11. Traceability

| Item              | Requirement / TODO           |
| ----------------- | ---------------------------- |
| Metric formulas   | FND-008 §25, FR-007          |
| Sample size       | RSH-001 §11                  |
| Evidence thresholds | RSH-001 §10, FR-011        |
| Distribution      | FND-007 §11                  |

---

# 12. Compliance

| Document / Rule       | Statistical requirement      |
| --------------------- | ---------------------------- |
| FND-009               | Backtest ≠ Proof            |
| PRD-004 FR-007        | Calculate Metrics           |
| PRD-004 FR-011        | Evaluate Evidence           |
| RSH-001 §10, §11      | Metrics dan sampel          |

---

# 13. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-005_Non_Functional_Requirements.md`
- `docs/05-research/RSH-001_Research_Methodology.md`
- `docs/05-research/RSH-002_Experiment_Specification.md`
- `docs/05-research/RSH-003_Validation_Methodology.md`

---

# 14. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.2.0   | 2026-08-11 | E-8: standardized decision criteria set (§8.1) + mandatory multiple-testing/data-snooping note (§8.2); fixes audit findings R-005 (criteria drift) and R-006 (no multiple-testing control) |
| 1.1.0   | 2026-08-08 | Approved via M3 Research Review (RSH-006) |
| 1.0.0   | 2026-08-08 | Initial statistical methodology  |

---

**Document Status:** Approved

**Document ID:** RSH-004

**Version:** 1.2.0

**End of Document**
