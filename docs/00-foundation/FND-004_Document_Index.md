---
title: Document Index
document_id: FND-004
version: 1.1.15
status: Active
category: Foundation
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-002
  - FND-003

purpose: Official registry of all Market Research Engine documentation
---

# Document Index

> **One project. One knowledge base. One source of truth.**

---

# 1. Purpose

Document Index merupakan registry resmi seluruh dokumentasi
Market Research Engine (MRE).

Dokumen ini digunakan untuk:

- mengetahui seluruh dokumen yang tersedia;
- mengetahui status setiap dokumen;
- mengetahui versi setiap dokumen;
- menemukan dokumen dengan cepat;
- memahami hubungan antar dokumen;
- mencegah duplikasi dokumentasi;
- membantu onboarding contributor;
- membantu AI assistant memahami knowledge base;
- menjaga dokumentasi tetap terstruktur.

`FND-004` merupakan **single source of truth**
untuk identitas dan status dokumentasi MRE.

---

# 2. Registry Rules

Seluruh dokumen resmi MRE wajib terdaftar di sini.

Setiap entry minimal memiliki:

- Document ID
- Title
- Category
- Path
- Version
- Status

Document ID mengikuti aturan pada:

`FND-003 — Document ID Standard`

---

# 3. Status Definitions

Status dokumen menggunakan nilai berikut.

| Status       | Meaning                                     |
| ------------ | ------------------------------------------- |
| `Planned`    | Dokumen direncanakan tetapi belum dibuat    |
| `Draft`      | Dokumen sedang dikembangkan                 |
| `Review`     | Dokumen sedang direview                     |
| `Approved`   | Dokumen telah disetujui                     |
| `Active`     | Dokumen aktif dan menjadi referensi         |
| `Deprecated` | Dokumen tidak lagi direkomendasikan         |
| `Archived`   | Dokumen disimpan untuk historical reference |

---

# 4. Foundation Documents

| ID      | Document               | Path                                                   | Version | Status   |
| ------- | ---------------------- | ------------------------------------------------------ | ------- | -------- |
| FND-001 | Project Charter        | `docs/00-foundation/FND-001_Project_Charter.md`        | 1.0.1   | Draft    |
| FND-002 | Documentation Standard | `docs/00-foundation/FND-002_Documentation_Standard.md` | 1.0.2   | Approved |
| FND-003 | Document ID Standard   | `docs/00-foundation/FND-003_Document_ID_Standard.md`   | 1.0.2   | Approved |
| FND-004 | Document Index         | `docs/00-foundation/FND-004_Document_Index.md`         | 1.0.3   | Active   |
| FND-005 | Project Context        | `docs/00-foundation/FND-005_Project_Context.md`        | 1.0.1   | Active   |
| FND-006 | Project Status      | `docs/00-foundation/FND-006_Project_Status.md`      | 1.3.1   | Active   |
| FND-007 | Roadmap             | `docs/00-foundation/FND-007_Roadmap.md`             | 1.1.0   | Active   |
| FND-008 | TODO                   | `docs/00-foundation/FND-008_TODO.md`                   | 1.3.2   | Active   |
| FND-009 | Glossary               | `docs/00-foundation/FND-009_Project_Glossary.md`        | 1.0.0   | Active   |
| FND-010 | Foundation Review      | `docs/00-foundation/FND-010_Foundation_Review.md`       | 1.0.0   | Approved |

---

# 5. Product Documents

Directory:

```text
docs/01-product/
```

| ID      | Document                      | Path                                               | Version | Status  |
| ------- | ----------------------------- | -------------------------------------------------- | ------- | ------- |
| PRD-001 | Product Vision                | `docs/01-product/PRD-001_Product_Vision.md`        | 1.1.0   | Approved |
| PRD-002 | User Personas                 | `docs/01-product/PRD-002_User_Personas.md`         | 1.1.0   | Approved |
| PRD-003 | Core Workflow                 | `docs/01-product/PRD-003_Core_Workflow.md`         | 1.1.1   | Approved |
| PRD-004 | Functional Requirements       | `docs/01-product/PRD-004_Functional_Requirements.md` | 1.1.0   | Approved |
| PRD-005 | Non-Functional Requirements   | `docs/01-product/PRD-005_Non_Functional_Requirements.md` | 1.1.0   | Approved |
| PRD-006 | MVP Definition                | `docs/01-product/PRD-006_MVP_Definition.md`        | 1.1.0   | Approved |
| PRD-007 | Feature Specification         | `docs/01-product/PRD-007_Feature_Specification.md` | 1.1.0   | Approved |
| PRD-008 | Product Definition Review     | `docs/01-product/PRD-008_Product_Definition_Review.md` | 1.1.0 | Approved |

---

# 6. Architecture Documents

Directory:

```text
docs/02-architecture/
```

| ID      | Document            | Path                                                  | Version | Status  |
| ------- | ------------------- | ----------------------------------------------------- | ------- | ------- |
| ARC-001 | System Architecture | `docs/02-architecture/ARC-001_System_Architecture.md` | 1.0.0   | Draft   |
| ARC-002 | Domain Model        | `docs/02-architecture/ARC-002_Domain_Model.md`        | 1.0.0   | Draft   |
| ARC-003 | Event Architecture  | `docs/02-architecture/ARC-003_Event_Architecture.md`  | —       | Planned |
| ARC-004 | Data Architecture   | `docs/02-architecture/ARC-004_Data_Architecture.md`   | 1.0.0   | Draft   |
| ARC-005 | Plugin Architecture | `docs/02-architecture/ARC-005_Plugin_Architecture.md` | —       | Planned |
| ARC-006 | Module Architecture | `docs/02-architecture/ARC-006_Module_Architecture.md` | 1.0.0   | Draft |

---

# 7. Engine Documents

Directory:

```text
docs/03-engine/
```

| ID      | Document           | Path                                           | Version | Status  |
| ------- | ------------------ | ---------------------------------------------- | ------- | ------- |
| ENG-001 | Data Engine        | `docs/03-engine/ENG-001_Data_Engine.md`        | —       | Planned |
| ENG-002 | Event Engine       | `docs/03-engine/ENG-002_Event_Engine.md`       | —       | Planned |
| ENG-003 | Signal Engine      | `docs/03-engine/ENG-003_Signal_Engine.md`      | —       | Planned |
| ENG-004 | Probability Engine | `docs/03-engine/ENG-004_Probability_Engine.md` | —       | Planned |
| ENG-005 | Simulation Engine  | `docs/03-engine/ENG-005_Simulation_Engine.md`  | —       | Planned |
| ENG-006 | Statistics Engine  | `docs/03-engine/ENG-006_Statistics_Engine.md`  | —       | Planned |
| ENG-007 | Reporting Engine   | `docs/03-engine/ENG-007_Reporting_Engine.md`   | —       | Planned |

---

# 8. Development Documents

Directory:

```text
docs/04-development/
```

| ID      | Document          | Path                                               | Version | Status  |
| ------- | ----------------- | -------------------------------------------------- | ------- | ------- |
| DEV-001 | Coding Standard   | `docs/04-development/DEV-001_Coding_Standard.md`   | —       | Planned |
| DEV-002 | Testing Strategy  | `docs/04-development/DEV-002_Testing_Strategy.md`  | —       | Planned |
| DEV-003 | Git Workflow      | `docs/04-development/DEV-003_Git_Workflow.md`      | —       | Planned |
| DEV-004 | Development Guide | `docs/04-development/DEV-004_Development_Guide.md` | —       | Planned |
| DEV-005 | Release Process   | `docs/04-development/DEV-005_Release_Process.md`   | —       | Planned |

---

# 9. Research Documents

Directory:

```text
docs/05-research/
```

| ID      | Document                | Path                                                  | Version | Status  |
| ------- | ----------------------- | ----------------------------------------------------- | ------- | ------- |
| RSH-001 | Research Methodology    | `docs/05-research/RSH-001_Research_Methodology.md`    | —       | Planned |
| RSH-002 | Backtest Protocol       | `docs/05-research/RSH-002_Backtest_Protocol.md`       | —       | Planned |
| RSH-003 | Validation Methodology  | `docs/05-research/RSH-003_Validation_Methodology.md`  | —       | Planned |
| RSH-004 | Statistical Methodology | `docs/05-research/RSH-004_Statistical_Methodology.md` | —       | Planned |

---

# 10. Architecture Decision Records

Directory:

```text
docs/06-decisions/
```

| ID      | Document | Path                             | Version | Status  |
| ------- | -------- | -------------------------------- | ------- | ------- |
| ADR-001 | —        | `docs/06-decisions/ADR-001_*.md` | —       | Planned |

> ADR numbering is sequential and chronological.

ADR entries will be added when architecture decisions
requiring formal records are made.

---

# 11. Experiment Documents

Directory:

```text
docs/07-experiments/
```

| ID      | Document                        | Path                               | Version | Status  |
| ------- | ------------------------------- | ---------------------------------- | ------- | ------- |
| EXP-001 | RSI Trendline Breakout Baseline | `docs/07-experiments/EXP-001_*.md` | —       | Planned |

Experiment documents will be added as research
experiments are conducted.

---

# 12. Templates

Directory:

```text
docs/08-templates/
```

| ID      | Document                      | Path                                                | Version | Status  |
| ------- | ----------------------------- | --------------------------------------------------- | ------- | ------- |
| TMP-001 | Standard Document Template    | `docs/08-templates/TMP-001_Standard_Document.md`    | —       | Planned |
| TMP-002 | ADR Template                  | `docs/08-templates/TMP-002_ADR_Template.md`         | —       | Planned |
| TMP-003 | Experiment Report Template    | `docs/08-templates/TMP-003_Experiment_Report.md`    | —       | Planned |
| TMP-004 | Design Specification Template | `docs/08-templates/TMP-004_Design_Specification.md` | —       | Planned |

---

# 13. Reference Documents

Directory:

```text
docs/09-reference/
```

| ID      | Document                | Path                                                   | Version | Status  |
| ------- | ----------------------- | ------------------------------------------------------ | ------- | ------- |
| REF-001 | Market Data Format      | `docs/09-reference/REF-001_Market_Data_Format.md`      | —       | Planned |
| REF-002 | Statistical Terminology | `docs/09-reference/REF-002_Statistical_Terminology.md` | —       | Planned |
| REF-003 | Python Environment      | `docs/09-reference/REF-003_Python_Environment.md`      | —       | Planned |

---

# 14. Document Dependency Map

High-level documentation dependency:

```text
                    FND-001
                Project Charter
                       │
                       ▼
              FND-002 / FND-003
             Documentation Rules
                       │
                       ▼
                  FND-004
               Document Index
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Product    Architecture   Research
          │            │            │
          ▼            ▼            │
        PRD-*        ARC-*          │
                       │            │
                       ▼            ▼
                    ENG-*        RSH-*
                       │            │
                       └─────┬──────┘
                             ▼
                           EXP-*
```

---

# 15. Core Dependency Chain

The primary documentation flow is:

```text
Project Charter
      ↓
Product Definition
      ↓
Architecture
      ↓
Engine Specification
      ↓
Development Standards
      ↓
Research Methodology
      ↓
Experiment
      ↓
Knowledge
```

Each layer should respect the constraints
defined by the layer above it.

---

# 16. Current Documentation Status

As of version `1.0.0`:

```text
Foundation
────────────────────────────
FND-001  Project Charter       Draft
FND-002  Documentation Std     Approved
FND-003  Document ID Std       Approved
FND-004  Document Index        Active

Product
────────────────────────────
PRD-*    Planned

Architecture
────────────────────────────
ARC-*    Planned

Engine
────────────────────────────
ENG-*    Planned

Development
────────────────────────────
DEV-*    Planned

Research
────────────────────────────
RSH-*    Planned

Decision
────────────────────────────
ADR-*    Planned

Experiment
────────────────────────────
EXP-*    Planned
```

---

# 17. Documentation Metrics

Document Index juga digunakan untuk
memantau perkembangan documentation coverage.

## Current Planned Documents

| Category     | Planned |
| ------------ | ------: |
| Foundation   |       9 |
| Product      |       5 |
| Architecture |       6 |
| Engine       |       7 |
| Development  |       5 |
| Research     |       4 |
| ADR          | Dynamic |
| Experiment   | Dynamic |
| Template     |       4 |
| Reference    |       3 |

Core planned documentation:

```text
9 + 5 + 6 + 7 + 5 + 4 + 4 + 3
= 43 documents
```

ADR dan Experiment bersifat dynamic
dan tidak memiliki batas jumlah.

---

# 18. Documentation Maturity

Documentation maturity akan diukur berdasarkan
status dokumen.

```text
Planned
   ↓
Draft
   ↓
Review
   ↓
Approved
   ↓
Active
```

Project tidak mengejar jumlah dokumen.

Project mengejar:

- completeness;
- consistency;
- accuracy;
- usefulness;
- maintainability.

---

# 19. Updating the Index

Setiap kali dokumen dibuat:

1. Assign Document ID.
2. Create document.
3. Add document ke FND-004.
4. Set initial status.
5. Set version.
6. Tambahkan dependency jika diperlukan.
7. Commit perubahan.

Flow:

```text
Create Document
      ↓
Assign ID
      ↓
Update FND-004
      ↓
Review
      ↓
Commit
```

---

# 20. When a Document Changes

Jika isi dokumen berubah:

```text
Update Content
      ↓
Update Version
      ↓
Update Last Updated
      ↓
Update FND-004
```

Document ID tetap sama.

---

# 21. When a Document Is Deprecated

Jika dokumen tidak lagi digunakan:

1. Ubah status menjadi `Deprecated`.
2. Catat penggantinya jika ada.
3. Update FND-004.
4. Jangan gunakan kembali Document ID.

Contoh:

```text
ARC-003
Status: Deprecated
Superseded By: ARC-008
```

---

# 22. When a Document Is Archived

Dokumen dapat dipindahkan menjadi `Archived`
apabila:

- tidak lagi relevan;
- hanya memiliki historical value;
- telah digantikan;
- tidak diperlukan untuk workflow aktif.

Document ID tetap dipertahankan.

---

# 23. Duplicate Prevention

Sebelum membuat dokumen baru,
developer harus melakukan:

```text
Search FND-004
      ↓
Search Repository
      ↓
Check Existing Concept
      ↓
Create or Extend
```

Jika dokumen dengan tujuan yang sama sudah ada,
dokumen baru tidak boleh dibuat
tanpa alasan yang jelas.

---

# 24. AI Assistant Integration

FND-004 merupakan dokumen penting
bagi AI assistant yang bekerja pada repository.

AI assistant harus menggunakan index ini untuk:

- menemukan dokumen;
- mengetahui status dokumen;
- mengetahui dependency;
- mengetahui struktur knowledge base;
- memilih dokumen yang tepat untuk diperbarui;
- menghindari pembuatan dokumen duplikat.

AI assistant tidak boleh menganggap
dokumen yang tidak terdaftar sebagai
official project documentation.

---

# 25. Consistency Rules

Document Index harus selalu konsisten dengan repository.

Minimal kondisi berikut harus benar:

```text
Every Registered Document
        ↓
Must Exist in Repository
```

Dan:

```text
Every Official Document
        ↓
Must Exist in Index
```

Jika ditemukan ketidaksesuaian,
FND-004 harus diperbaiki.

---

# 26. Integrity Check

Secara berkala project dapat melakukan
documentation integrity check.

Pemeriksaan minimal:

- duplicate Document ID;
- missing Document ID;
- missing index entry;
- invalid path;
- invalid status;
- broken dependency;
- broken cross-reference;
- version mismatch.

Contoh:

```text
FND-004
   │
   ├── Check IDs
   ├── Check Paths
   ├── Check Status
   ├── Check Versions
   └── Check Dependencies
```

---

# 27. Future Automation

Di masa depan,
FND-004 dapat divalidasi secara otomatis
menggunakan tooling.

Contoh:

```text
documentation_lint
```

Tool dapat memeriksa:

```text
✓ ID exists
✓ ID unique
✓ File exists
✓ Metadata valid
✓ Path valid
✓ Version valid
✓ Dependency valid
✓ Cross-reference valid
```

Automation tidak mengubah governance.

Automation hanya membantu menegakkannya.

---

# 28. Definition of Done

FND-004 dianggap selesai apabila:

- [x] Seluruh kategori dokumentasi didefinisikan.
- [x] Foundation documents terdaftar.
- [x] Product documents terdaftar.
- [x] Architecture documents terdaftar.
- [x] Engine documents terdaftar.
- [x] Development documents terdaftar.
- [x] Research documents terdaftar.
- [x] ADR registry disiapkan.
- [x] Experiment registry disiapkan.
- [x] Template registry disiapkan.
- [x] Reference registry disiapkan.
- [x] Dependency map didefinisikan.
- [x] Lifecycle didefinisikan.
- [x] Update procedure didefinisikan.
- [x] Integrity rules didefinisikan.

---

# 29. Maintenance Policy

FND-004 harus diperbarui
setiap kali:

- dokumen baru dibuat;
- dokumen dihapus;
- dokumen deprecated;
- dokumen archived;
- document title berubah;
- document path berubah;
- document version berubah;
- dependency berubah.

FND-004 harus dianggap sebagai
living document.

---

# 30. Closing Statement

Document Index bukan sekadar daftar file.

Ia merupakan peta knowledge base
Market Research Engine.

Semakin besar project berkembang,
semakin penting kemampuan untuk menjawab:

> Apa yang kita ketahui?

> Di mana pengetahuan tersebut berada?

> Apa statusnya?

> Apa yang bergantung padanya?

> Apa yang menggantikannya?

FND-004 menyediakan jawaban tersebut
dalam satu lokasi terpusat.

> **If the project has knowledge, the knowledge must have an address.**

---

# Appendix A — Quick Reference

## Document ID Format

```text
<PREFIX>-<NUMBER>
```

## Prefix

```text
FND  Foundation
PRD  Product
ARC  Architecture
ENG  Engine
DEV  Development
RSH  Research
ADR  Architecture Decision
EXP  Experiment
TMP  Template
REF  Reference
```

## Status

```text
Planned
Draft
Review
Approved
Active
Deprecated
Archived
```

## Version

```text
MAJOR.MINOR.PATCH
```

## Registry

```text
FND-004
```

---

# Appendix B — Current Next Steps

Setelah FND-004 aktif,
urutan pengerjaan Foundation berikutnya:

```text
FND-005
Project Context
       ↓
FND-006
Project Status
       ↓
FND-007
Roadmap
       ↓
FND-008
TODO
       ↓
FND-009
Glossary
       ↓
Foundation Complete
```

Setelah Foundation selesai:

```text
01-product
      ↓
02-architecture
      ↓
03-engine
      ↓
04-development
      ↓
05-research
      ↓
Sprint 1
```

---

**Document Status:** Active

**Document ID:** FND-004

**Version:** 1.1.15

**End of Document**
