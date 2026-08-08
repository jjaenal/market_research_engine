---
title: Validation Methodology
document_id: RSH-003
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
  - ARC-007
  - PRD-004
  - PRD-005
  - RSH-001
  - RSH-002

referenced_by:
  - FND-006
  - FND-008
  - RSH-001
  - RSH-002
  - EXP-001

purpose: Define the validation methodology for MRE experiments — separation, out-of-sample, walk-forward, sensitivity, and robustness
---

# Validation Methodology

> Measure the Market. Discover the Edge.

---

# 1. Purpose

RSH-003 mendefinisikan **validation methodology** dari Market Research Engine (MRE).

Dokumen ini menurunkan validasi dari RSH-001 §12
menjadi prosedur yang dapat dieksekusi.

RSH-003 menetapkan:

- pemisahan train/test;
- out-of-sample testing (TODO-025);
- walk-forward testing;
- sensitivity analysis (TODO-024);
- robustness analysis (TODO-026).

---

# 2. Scope

Scope RSH-003:

- jenis validasi;
- urutan eksekusi validasi;
- aturan pemisahan data.

Di luar scope RSH-003:

- metodologi umum (RSH-001);
- spesifikasi experiment (RSH-002);
- statistik detail (RSH-004).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- peneliti;
- quant analyst;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per RSH-001 §12, validasi dilakukan agar evidence
tidak hanya in-sample (fit pada data lama)
tetapi out-of-sample (berlaku pada data baru).

Backtest adalah evidence, bukan bukti (FND-009).
Validasi mengurangi risiko overfitting.

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term             | Definition                                      |
| ---------------- | ----------------------------------------------- |
| In-sample        | Data yang digunakan untuk pengembangan          |
| Out-of-sample    | Data yang tidak dilihat saat pengembangan       |
| Walk-forward     | Validasi bergulir berbasis waktu                |
| Sensitivity      | Respons hasil terhadap perubahan parameter      |
| Robustness       | Stabilitas hasil atas parameter/data beragam    |
| Overfitting      | Fit berlebih pada in-sample, gagal out-of-sample|

---

# 6. Data Separation

- dataset dibagi menjadi **train** (pengembangan)
  dan **test** (validasi) berbasis waktu (chronological);
- tidak ada pengacakan silang yang membocorkan masa depan;
- separasi didefinisikan sebelum experiment dijalankan
  (RSH-001 §7.2, pre-registration);
- tidak ada alokasi retroaktif setelah melihat hasil.

---

# 7. Out-of-Sample Testing (TODO-025)

- strategi dioptimalkan/ditentukan pada train set;
- dijalankan tanpa perubahan pada test set (out-of-sample);
- hasil OOS dibandingkan dengan hasil in-sample;
- degradasi besar in-sample → OOS menandakan overfitting.

---

# 8. Walk-Forward Testing

- dataset dibagi menjadi window bergulir (training + validation);
- strategi ditentukan pada tiap window training;
- dievaluasi pada validation window berikutnya;
- hasil agregat menilai stabilitas temporal.

---

# 9. Sensitivity Analysis (TODO-024)

- variasi parameter strategi/indikator (independent variables, RSH-001 §8.2);
- satu parameter divariasikan, lainnya tetap (control);
- observasi perubahan metrik;
- parameter yang sangat sensitif menandakan fragile edge.

---

# 10. Robustness Analysis (TODO-026)

- kombinasi parameter/data beragam;
- hasil harus stabil di sekitar titik optimum;
- robustness dievaluasi terhadap perubahan
  rentang data, timeframe, dan biaya transaksi.

---

# 11. Validation Sequence

```text
Baseline run (in-sample)
    ↓
Out-of-sample testing
    ↓
Walk-forward testing
    ↓
Sensitivity analysis
    ↓
Robustness analysis
    ↓
Monte Carlo (jika relevan)
    ↓
Evidence assessment (RSH-004)
```

---

# 12. Thresholds

Threshold kuantitatif (mis. toleransi degradasi,
minimum trade count) ditetapkan pada RSH-004.

---

# 13. Traceability

| Item               | Requirement / TODO           |
| ------------------ | ---------------------------- |
| Data separation    | RSH-001 §8.1, FR-010         |
| Out-of-sample      | TODO-025                     |
| Sensitivity        | TODO-024                     |
| Robustness         | TODO-026                     |
| Walk-forward       | FND-007 §10                  |

---

# 14. Compliance

| Document / Rule       | Validation requirement      |
| --------------------- | --------------------------- |
| FND-009               | Backtest ≠ Proof            |
| PRD-004 FR-011        | Evaluate Evidence           |
| RSH-001 §7.2          | Pre-registration            |
| RSH-001 §12           | Validation                  |

---

# 15. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-005_Non_Functional_Requirements.md`
- `docs/05-research/RSH-001_Research_Methodology.md`
- `docs/05-research/RSH-002_Experiment_Specification.md`

---

# 16. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.1.0   | 2026-08-08 | Approved via M3 Research Review (RSH-006) |
| 1.0.0   | 2026-08-08 | Initial validation methodology   |

---

**Document Status:** Approved

**Document ID:** RSH-003

**Version:** 1.1.0

**End of Document**
