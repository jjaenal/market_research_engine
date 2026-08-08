---
title: Reporting Engine
document_id: ENG-007
version: 1.0.0
status: Draft
category: Engine
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
  - ARC-006
  - ARC-007
  - PRD-003
  - PRD-007
  - DEV-002
  - RSH-002
  - RSH-005
  - RSH-006

referenced_by:
  - FND-006
  - FND-008
  - RSH-005

purpose: Define the Reporting Engine implementation spec — report sections, output format, and reproducibility (TODO-021, FEAT-008)
---

# Reporting Engine

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ENG-007 mendefinisikan **Reporting Engine** — spesifikasi implementasi
untuk TODO-021 (Build Reporting Engine) dan FEAT-008 (Report Generator).

Dokumen ini menurunkan requirements penelitian (RSH-005)
dan feature (FEAT-008) menjadi spesifikasi engine yang dapat dibangun.

---

# 2. Scope

Scope ENG-007:

- kontrak interface ReportingEngine (ARC-006 §7.7);
- komponen penyusun report;
- format output;
- reproducibility report.

Di luar scope ENG-007:

- research reporting requirements (RSH-005);
- metrik (RSH-004);
- engine lain (ENG-001..ENG-006).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per ARC-006 §7.7:

```text
ReportingEngine: render(result, config) → Report
```

Report harus **terstruktur dan reproducible** (PRD-003 §7.8),
memuat konfigurasi, metadata dataset, metrik, dan conclusion (FEAT-008).

Per RSH-005 §6, report tersusun dari section:
Header, Hypothesis, Dataset, Configuration, Assumptions,
Metrics, Evidence & Conclusion, Reproducibility.

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term        | Definition                                        |
| ----------- | ------------------------------------------------- |
| Report      | Output terstruktur dari experiment (FEAT-008)     |
| Section     | Bagian terstruktur report (RSH-005 §6)            |
| Experiment ID | Identitas unik experiment (RSH-002 §7)          |
| Conclusion  | Interpretasi evidence (RSH-005 §7.7)              |

---

# 6. Interface

Per ARC-006 §7.7:

```text
render(result, config) → Report
```

- `result`: output StatisticsEngine (metrik, trade ledger, equity curve);
- `config`: konfigurasi experiment terkunci (PRD-003 §7.3);
- `Report`: objek report immutable (Article 13).

---

# 7. Report Sections

ENG-007 memproduksi section berikut (TODO-021, FND-007 §21, RSH-005 §6):

| Section             | Sumber                              |
| ------------------- | ----------------------------------- |
| Header              | Experiment ID, tanggal, code version|
| Hypothesis          | RSH-001 §7                          |
| Dataset             | Metadata dataset (ARC-004)          |
| Configuration       | Konfigurasi frozen (PRD-003 §7.3)   |
| Assumptions         | Execution & cost assumptions        |
| Summary             | Ringkasan hasil (metrics)           |
| Trade Log           | Log Trade simulasi                  |
| Statistics          | Metrik minimum (RSH-002 §8)         |
| Equity Curve        | Perubahan equity (chart/data)       |
| Experiment Metadata | Reproducibility (code version)      |
| Evidence & Conclusion | Evidence assessment + conclusion (FR-011) |

---

# 8. Components

| Component             | Responsibility                      |
| --------------------- | ----------------------------------- |
| Summary Builder       | Menyusun ringkasan metrics          |
| Trade Log Renderer    | Merender log Trade                  |
| Statistics Renderer   | Menyusun tabel metrik (RSH-004)     |
| Equity Curve Renderer | Menyusun data equity curve          |
| Config Exporter       | Menyusun konfigurasi frozen         |
| Metadata Exporter     | Menyusun experiment metadata        |
| Conclusion Builder    | Area conclusion dari evidence       |

---

# 9. Output Format

- format terstruktur yang dapat di-parse (Markdown + blok data);
- deterministic dan reproducible (FR-010, FEAT-009);
- output immutable setelah render (Article 13);
- disimpan terikat Experiment ID (RSH-002 §7).

---

# 10. Failure Conditions

Per PRD-003 §7.8:

- metrik hilang → report gagal;
- error rendering → report gagal;
- evidence tidak cukup → conclusion menandai tidak cukup (FR-011).

---

# 11. Testing (DEV-002)

- golden test: output report dibandingkan dengan golden file
  yang telah diverifikasi (DEV-002 §9);
- test determinism: run yang sama → report identik;
- test failure: metrik hilang, error rendering.

---

# 12. Traceability

| Item              | Requirement / Feature          |
| ----------------- | ------------------------------ |
| Interface         | ARC-006 §7.7, FR-009           |
| Report sections   | TODO-021, FND-007 §21, RSH-005 |
| Reproducibility   | FR-010, NFR-001, FEAT-009      |
| Evidence          | FR-011, PRD-003 §7.9           |

---

# 13. Compliance

| Document / Rule       | Engine requirement         |
| --------------------- | -------------------------- |
| Article 6             | Stateless renderer         |
| Article 7             | Deterministic              |
| Article 13            | Report immutable           |
| PRD-003 §7.8          | Report terstruktur, reproducible |
| DEV-002               | Golden test                |

---

# 14. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-004_Data_Architecture.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-007_Feature_Specification.md`
- `docs/04-development/DEV-002_Testing_Strategy.md`
- `docs/05-research/RSH-002_Experiment_Specification.md`
- `docs/05-research/RSH-005_Research_Reporting.md`
- `docs/05-research/RSH-006_Research_Review.md`

---

# 15. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial reporting engine spec    |

---

**Document Status:** Draft

**Document ID:** ENG-007

**Version:** 1.0.0

**End of Document**
