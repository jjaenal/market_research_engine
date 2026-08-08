---
title: Testing Strategy
document_id: DEV-002
version: 1.0.0
status: Draft
category: Development
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-005
  - FND-009
  - FND-010
  - ARC-001
  - ARC-002
  - ARC-003
  - ARC-004
  - ARC-005
  - ARC-006
  - ARC-007
  - PRD-004
  - PRD-005
  - DEV-001

referenced_by:
  - ARC-007
  - FND-006
  - FND-008

purpose: Define the testing strategy for MRE to satisfy the M2 exit criterion "testing strategy jelas" (ARC-ACT-001)
---

# Testing Strategy

> Measure the Market. Discover the Edge.

---

# 1. Purpose

DEV-002 mendefinisikan **testing strategy** dari Market Research Engine (MRE).

Dokumen ini menjawab **ARC-ACT-001** (ARC-007)
dan kriteria exit M2 "testing strategy jelas" (FND-007 §7).

DEV-002 menetapkan:

- level testing;
- framework dan tooling;
- strategi test per module;
- data test;
- determinisme dan reproducibility;
- kontribusi dari strategi (pytest, ruff, black).

---

# 2. Scope

Scope DEV-002:

- level testing (unit, integration, acceptance);
- strategi test per module (ARC-006 layout);
- data test dan fixture;
- reproducibility testing.

Di luar scope DEV-002:

- proses development (DEV-003 Git Workflow);
- release process (DEV-005);
- detail implementasi engine (M4).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- QA;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

MRE dibangun dengan prinsip:

- **unit-test first** (FND-001, FND-010);
- pure functions dan determinism (Article 6, Article 7);
- config over hardcode (Article 12);
- reproducibility experiment (PRD-004 FR-010, NFR-001).

Testing adalah bagian dari Gate 3 — Architecture (FND-001 §14.16):
tidak boleh melanggar Architecture Constitution.

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term          | Definition                                        |
| ------------- | ------------------------------------------------- |
| Unit test     | Test fungsi tunggal (pure function)               |
| Integration   | Test interaksi antar module (ARC-006)             |
| Golden test   | Test terhadap output yang sudah diverifikasi      |
| Fixture       | Data test yang deterministik dan dapat diulang    |
| Reproducibility | Test bahwa run yang sama menghasilkan output sama |

---

# 6. Testing Levels

| Level           | Scope                      | Tools (planned)          |
| --------------- | -------------------------- | ------------------------ |
| Unit            | Pure function per module   | pytest                   |
| Integration     | Kontrak antar engine       | pytest                   |
| Acceptance      | Pipeline CSV → Report      | pytest + golden file     |
| Reproducibility | Run berulang deterministic | pytest (determinism check) |

---

# 7. Unit Test Strategy

Per module (ARC-006):

| Module         | Unit test coverage                       |
| -------------- | ---------------------------------------- |
| `loaders/`     | parsing CSV, validasi, integrity rules (ARC-004) |
| `indicators/`  | output indikator terhadap referensi      |
| `detectors/`   | Event yang dipancarkan (ARC-003)         |
| `engines/`     | kontrak interface (ARC-006 §7)           |
| `strategies/`  | kombinasi Event → Signal                 |
| `utils/`       | logging, helpers                         |

Prinsip unit test:

- fungsi murni → test murni (tanpa I/O, tanpa network);
- satu test satu perilaku;
- test deterministik — tanpa random/tanggal dinamis;
- test cepat (< ms per test).

---

# 8. Integration Test Strategy

- test kontrak antar engine (ARC-006 §7): input/output sesuai spesifikasi;
- test pipeline mini: Dataset → Event → Signal (tanpa simulasi);
- test plugin loading dan validasi konfigurasi (ARC-005 §10);
- test kegagalan: warm-up tidak cukup, konfigurasi tidak valid (PRD-003 §7.4).

---

# 9. Acceptance / Golden Test

- satu pipeline end-to-end: CSV → Report (MVP boundary, PRD-006);
- output dibandingkan dengan **golden file** yang telah diverifikasi manual;
- perubahan perilaku terdeteksi melalui diff golden.

---

# 10. Reproducibility Testing

Per NFR-001 dan Article 7:

- run yang sama (dataset + config sama) → output identik;
- test memastikan tidak ada state global (Article 6);
- tidak ada sumber nondeterminisme (waktu, random, konfigurasi tersembunyi).

---

# 11. Test Data

- fixture dataset sintetis yang kecil dan deterministik;
- dataset nyata tidak dimasukkan ke repository (gitignore `datasets/`);
- golden file di-maintain bersama kode;
- setiap fixture memiliki metadata (symbol, timeframe, ekspektasi).

---

# 12. Tooling (Planned)

- **pytest** — runner dan assertion;
- **coverage** (pytest-cov) — metrik coverage module;
- **ruff** — linting;
- **black** — formatting.

Tooling diaktifkan pada M4 — Engine Implementation
(TODO-015 Build Data Engine dan seterusnya).

---

# 13. Traceability

| Item                  | Requirement / Feature     |
| --------------------- | ------------------------- |
| Unit tests            | NFR-001, NFR-002          |
| Determinism tests     | NFR-001, Article 7        |
| Acceptance golden     | PRD-006 MVP boundary      |
| Integration contracts | ARC-006 §7, FR-004..FR-011|

---

# 14. Compliance

| Constitution Article | Testing requirement                |
| -------------------- | ---------------------------------- |
| Article 6            | Test memastikan tanpa state global |
| Article 7            | Test deterministik                 |
| Article 13           | Data test immutable                |
| Gate 3               | Tidak melanggar Architecture Constitution |

---

# 15. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-003_Event_Architecture.md`
- `docs/02-architecture/ARC-004_Data_Architecture.md`
- `docs/02-architecture/ARC-005_Plugin_Architecture.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-005_Non_Functional_Requirements.md`
- `docs/04-development/DEV-001_Coding_Standard.md`

---

# 16. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial testing strategy (ARC-ACT-001) |

---

**Document Status:** Draft

**Document ID:** DEV-002

**Version:** 1.0.0

**End of Document**
