---
title: Non-Functional Requirements
document_id: PRD-005
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
  - PRD-004

referenced_by:
  - PRD-007
  - ARC-001

purpose: Define the non-functional requirements of MRE — determinism, reproducibility, correctness, performance, testability, extensibility, observability, maintainability
---

# Non-Functional Requirements

> Measure the Market. Discover the Edge.

---

# 1. Purpose

PRD-005 mendefinisikan **non-functional requirements (NFR)** dari Market Research Engine (MRE).

Dokumen ini menjawab TODO-008 — Define Non-Functional Requirements (FND-008).

NFR bersifat cross-cutting dan mengatur bagaimana sistem berperilaku, bukan apa yang dilakukan sistem.

---

# 2. Scope

Scope PRD-005:

- determinism;
- reproducibility;
- correctness;
- performance;
- testability;
- extensibility;
- observability;
- maintainability.

Di luar scope PRD-005:

- functional requirements (PRD-004);
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

Functional requirements (PRD-004) mendefinisikan apa yang harus dilakukan sistem.

Agar research dapat dipercaya, sistem juga harus:

- deterministic dan reproducible;
- benar secara kalkulasi;
- dapat diuji;
- dapat diperluas;
- mudah dipahami dan dipelihara.

NFR memastikan hal tersebut.

---

# 5. Definitions

Terminologi mengikuti **FND-009 — Project Glossary** (One Concept, One Name).

Istilah kunci:

| Term       | Definition                                |
| ---------- | ----------------------------------------- |
| Experiment | Prosedur terkontrol untuk menguji hypothesis |
| Evidence   | Output research yang dapat direproduksi   |
| Backtest   | Metode; bukan bukti (Backtest ≠ Proof)    |

Apabila terjadi konflik terminologi, FND-009 lebih diutamakan.

---

# 6. Non-Functional Requirements

## NFR-001 — Determinism

Sistem harus menghasilkan output yang sama untuk input yang sama.

- **Rationale:** hasil eksperimen tidak boleh bergantung pada urutan eksekusi, waktu, atau randomness.
- **Verification:** menjalankan step yang sama dua kali menghasilkan output yang identik; tidak ada source of randomness pada pipeline inti (kecuali dikontrol seed).

## NFR-002 — Reproducibility

Experiment harus dapat direproduksi dari dataset dan konfigurasi yang sama.

- **Rationale:** research hanya valid apabila dapat diulang oleh pihak lain.
- **Verification:** Experiment ID stabil untuk konfigurasi yang sama; report menyimpan konfigurasi, metadata dataset, dan version.

## NFR-003 — Correctness

Kalkulasi metrik dan validasi data harus benar dan tidak pernah salah diam-diam.

- **Rationale:** metrik yang salah merusak kesimpulan.
- **Verification:** formula metrik terdefinisi eksplisit (PRD-004 FR-007); kegagalan dipermukaan melalui failure conditions (PRD-003); tidak ada silent error.

## NFR-004 — Performance

Sistem harus memproses dataset target (misal `XAUUSD_H1`) dalam waktu yang dapat diterima.

- **Rationale:** iterasi eksperimen harus praktis.
- **Verification:** pipeline inti dapat menjalankan satu experiment penuh pada dataset target dalam batas waktu yang ditetapkan.

## NFR-005 — Testability

Sistem harus dapat diuji secara unit-test first.

- **Rationale:** pure functions memudahkan pengujian; core pipeline harus terverifikasi.
- **Verification:** setiap modul inti memiliki unit test; pipeline end-to-end dapat diuji.

## NFR-006 — Extensibility

Strategi dan detektor harus dapat ditambahkan sebagai plugin tanpa mengubah engine.

- **Rationale:** MRE adalah framework riset yang modular (FND-001).
- **Verification:** strategi baru dapat ditambahkan melalui konfigurasi/plugin; indicator tidak pernah menghasilkan Trade.

## NFR-007 — Observability

Sistem harus menyediakan logging terstruktur dengan level INFO/WARNING/ERROR.

- **Rationale:** setiap langkah experiment harus dapat ditelusuri.
- **Verification:** tidak ada `print` pada business logic; log mencatat langkah, konfigurasi, dan kegagalan.

## NFR-008 — Maintainability

Kode harus mengikuti standar engineering: type hints, dataclasses, docstring, modular layout.

- **Rationale:** framework jangka panjang harus mudah dipelihara.
- **Verification:** modul pada `src/` mengikuti layout yang ditetapkan; public class/function memiliki docstring.

---

# 7. NFR Matrix

| NFR                    | Source                                 |
| ---------------------- | -------------------------------------- |
| NFR-001 Determinism    | FND-005 (pure functions)               |
| NFR-002 Reproducibility | FND-005 / PRD-004 FR-010              |
| NFR-003 Correctness    | PRD-003 (failure conditions)           |
| NFR-004 Performance    | scope MVP (PRD-006)                    |
| NFR-005 Testability    | FND-005 (unit-test first)              |
| NFR-006 Extensibility  | FND-001 (strategies as plugins)        |
| NFR-007 Observability  | coding standard (logger)               |
| NFR-008 Maintainability | coding standard (type hints, docstring) |

---

# 8. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/01-product/PRD-001_Product_Vision.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-006_MVP_Definition.md`

---

# 9. Revision History

| Version | Date       | Changes                         |
| ------- | ---------- | ------------------------------- |
| 1.0.0   | 2026-08-08 | Initial non-functional requirements |

---

**Document Status:** Draft

**Document ID:** PRD-005

**Version:** 1.0.0

**End of Document**
