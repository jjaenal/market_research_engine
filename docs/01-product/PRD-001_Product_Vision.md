---
title: Product Vision
document_id: PRD-001
version: 1.1.0
status: Approved
category: Product
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-005
  - FND-010

referenced_by:
  - PRD-002
  - PRD-003
  - PRD-004
  - PRD-005
  - PRD-006
  - PRD-007
  - ARC-001

purpose: Translate the MRE project vision into a product-level statement that answers who uses MRE, what problem it solves, why it is useful, and what the primary workflow is
---

# Product Vision

> **Measure the Market. Discover the Edge.**

---

# 1. Purpose

PRD-001 mendefinisikan **product vision** dari Market Research Engine (MRE) pada level produk.

Dokumen ini menjawab pertanyaan mendasar:

- Siapa yang menggunakan MRE?
- Masalah apa yang dipecahkan MRE?
- Apa yang membuat MRE berguna?
- Bagaimana workflow utama MRE?
- Apa yang secara eksplisit di luar scope?

PRD-001 adalah bagian pertama dari Product Phase (M1) sesuai dengan TODO-004 pada FND-008.

---

# 2. Scope

Scope PRD-001:

- product vision statement;
- target user;
- problem statement;
- value proposition;
- primary workflow;
- batas produk (in-scope dan out-of-scope).

Di luar scope PRD-001:

- user personas (PRD-002);
- core workflow (PRD-003);
- functional requirements (PRD-004);
- non-functional requirements (PRD-005);
- MVP definition (PRD-006);
- feature specification (PRD-007);
- detail arsitektur (Fase M2 — Architecture).

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

Dokumen ini juga menjadi acuan bagi AI assistant yang bekerja pada repository ini.

---

# 4. Background

Sebagian besar trader mengembangkan strategi dengan mencari indikator baru, menggabungkan sinyal, kemudian mengoptimasi parameter.

Pendekatan tersebut sering menghasilkan strategi yang terlihat baik di masa lalu tetapi gagal secara ilmiah ketika diuji.

Masalah inti:

- tidak ada evidence yang dapat direproduksi;
- backtest disalahartikan sebagai bukti;
- hasil sulit dibandingkan antar strategi;
- keputusan didasarkan pada opini, bukan data.

MRE dibangun untuk menjawab masalah tersebut.

---

# 5. Definitions

Terminologi mengikuti **FND-009 — Project Glossary** (One Concept, One Name).

Istilah kunci:

| Term               | Definition                                   |
| ------------------ | -------------------------------------------- |
| Research           | Proses sistematis untuk menghasilkan evidence terhadap hypothesis |
| Hypothesis         | Pernyataan yang dapat diuji menggunakan evidence |
| Experiment         | Prosedur terkontrol untuk menguji hypothesis |
| Signal             | Kombinasi beberapa Event                     |
| Backtest           | Metode; bukan bukti (Backtest ≠ Proof)       |

Apabila terjadi konflik terminologi, FND-009 lebih diutamakan.

---

# 6. Product Vision

> **Market Research Engine (MRE) adalah framework open-source untuk menguji hipotesis trading secara ilmiah menggunakan pendekatan event-driven dan analisis statistik.**

MRE bukan sekadar backtester. Backtest hanyalah salah satu output dari proses riset.

Prinsip utama:

> Jangan percaya strategi. Percaya data.

---

# 7. Problem Statement

Trader dan peneliti tidak memiliki cara yang dapat direproduksi untuk menguji apakah sebuah strategi trading memiliki statistical edge.

Akibatnya:

- strategi dievaluasi secara subjektif;
- hasil eksperimen tidak dapat diulang;
- keputusan pengembangan tidak didasarkan pada evidence;
- knowledge tidak terdokumentasi.

---

# 8. Value Proposition

MRE berguna karena:

- **Reproducible** — experiment yang sama menghasilkan hasil yang sama;
- **Event-driven** — deteksi berbasis fakta (Event), bukan rekomendasi;
- **Statistical** — menghasilkan metrik yang dapat dipercaya;
- **Modular** — memisahkan market research dari trade simulation;
- **Transparan** — setiap keputusan dapat ditelusuri dari data sampai kesimpulan;
- **Configurable** — configuration over hardcode.

---

# 9. Primary Workflow

Workflow utama MRE:

```text
Research Question
        ↓
Hypothesis
        ↓
Experiment (dataset + configuration)
        ↓
Event Detection
        ↓
Signal
        ↓
Statistical Metrics
        ↓
Evidence
        ↓
Conclusion
```

Posisi produk: MRE menyediakan alat untuk menjalankan alur tersebut secara terkontrol dan dapat diulang.

---

# 10. Target Users

| User                 | Needs                                        |
| -------------------- | -------------------------------------------- |
| Quantitative Researcher | Menguji hypothesis secara statistik        |
| Algorithmic Trader   | Mengevaluasi strategi sebelum eksekusi       |
| Software Engineer    | Mengembangkan framework modular              |
| Data Scientist       | Menganalisis market data                     |
| Akademisi            | Melakukan penelitian trading yang dapat diulang |
| Komunitas open-source | Menggunakan dan memperluas framework        |

---

# 11. Explicitly Out of Scope

Pada fase M1 dan Sprint 1 (implementation), MRE secara eksplisit **tidak** mencakup:

- entry BUY/SELL;
- TP/SL;
- optimasi;
- machine learning;
- live trading / order execution;
- rekomendasi sinyal trading;
- penggantian keputusan manusia.

---

# 12. Success Direction

MRE sukses apabila:

- satu experiment dapat dijalankan dari CSV hingga report secara reproducible;
- hypothesis dapat diuji dan menghasilkan conclusion yang dapat diulang;
- knowledge dari setiap eksperimen terdokumentasi;
- tidak ada bias sistematis dalam proses evaluasi.

---

# 13. Alignment with Foundation

PRD-001 konsisten dengan:

- **FND-001** — Project Charter (vision dan mission);
- **FND-005** — Project Context (current phase dan research principles);
- **FND-010** — Foundation Review (transition gate M1);
- **FND-009** — Project Glossary (terminologi).

---

# 14. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/Market_Research_Engine_PRD_Sprint1.md`

---

# 15. Revision History

| Version | Date       | Changes                                                    |
| ------- | ---------- | ---------------------------------------------------------- |
| 1.1.0    | 2026-08-08 | Approved via M1 Product Definition Review (PRD-008) |
| 1.0.1   | 2026-08-08 | Align PRD series with FND-007 (User Personas, Core Workflow, Functional/NFR, MVP, Feature Spec) |
| 1.0.0   | 2026-08-08 | Initial product vision                                     |

---

**Document Status:** Approved

**Document ID:** PRD-001

**Version:** 1.1.0

**End of Document**
