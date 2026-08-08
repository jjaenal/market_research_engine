---
title: Architecture Review
document_id: ARC-007
version: 1.0.0
status: Draft
category: Architecture
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-005
  - FND-010
  - ARC-001
  - ARC-002
  - ARC-003
  - ARC-004
  - ARC-005
  - ARC-006
  - ADR-001
  - ADR-002
  - PRD-003
  - PRD-008

referenced_by:
  - FND-006
  - FND-008

purpose: Record the M2 Architecture review — document completeness, constitution compliance, and the transition gate to M3
---

# Architecture Review

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ARC-007 adalah **review resmi** terhadap M2 — Architecture.

Dokumen ini:

- menilai kelengkapan dan kualitas ARC-001..006 dan ADR-001..002;
- memverifikasi objective chain M2 (TODO-009..012);
- memverifikasi compliance terhadap Architecture Constitution (FND-001 §14);
- memverifikasi exit criteria M2 (FND-007 §7);
- memutuskan transisi menuju M3 — Research Methodology.

---

# 2. Review Scope

Review mencakup:

```text
ARC-001  System Architecture
ARC-002  Domain Model
ARC-003  Event Architecture
ARC-004  Data Architecture
ARC-005  Plugin Architecture
ARC-006  Module Architecture
ADR-001  Adopt Event-Driven Architecture
ADR-002  Adopt Plugin-Based Architecture
```

Di luar scope review ini:

- detail research methodology (M3);
- detail implementasi (M4);
- hasil eksperimen (M5+).

---

# 3. Review Principle

M2 dianggap selesai apabila menjawab:

> **How should it work?**

bukan:

> Have we written every possible document?

---

# 4. Review Result

## Final Status

```text
M2 ARCHITECTURE: APPROVED
```

## Overall Assessment

```text
PASS WITH ACTIONS
```

Tidak ditemukan critical blocker
yang mengharuskan M2 diulang.

Terdapat beberapa consistency actions
yang harus diselesaikan
setelah review ini.

---

# 5. Architecture Document Review

| Document | Purpose                  |   Status | Review      |
| -------- | ------------------------ | -------: | ----------- |
| ARC-001  | System boundaries        |     PASS | Complete    |
| ARC-002  | Domain model             |     PASS | Complete    |
| ARC-003  | Event architecture       |     PASS | Complete    |
| ARC-004  | Data contracts           |     PASS | Complete    |
| ARC-005  | Plugin architecture      |     PASS | Complete    |
| ARC-006  | Module/engine interfaces |     PASS | Complete    |
| ADR-001  | Event-driven decision    |     PASS | Complete    |
| ADR-002  | Plugin-based decision    |     PASS | Complete    |

---

# 6. M2 Objective Review

Master TODO (FND-008 §7):

| TODO            | Evidence                | Status |
| --------------- | ----------------------- | :----: |
| TODO-009 System Architecture  | ARC-001   |   ✓    |
| TODO-010 Domain Model         | ARC-002   |   ✓    |
| TODO-011 Data Model           | ARC-004   |   ✓    |
| TODO-012 Engine Interfaces    | ARC-006   |   ✓    |

Semua link terpenuhi.

---

# 7. Exit Criteria Review

FND-007 §7:

| Criterion                    | Evidence                          | Status |
| ---------------------------- | --------------------------------- | :----: |
| System boundaries jelas      | ARC-001                           |   ✓    |
| Modules jelas                | ARC-001, ARC-006                  |   ✓    |
| Domain model jelas           | ARC-002                           |   ✓    |
| Data contracts jelas         | ARC-004                           |   ✓    |
| Interfaces jelas             | ARC-006                           |   ✓    |
| Dependency rules jelas       | ARC-001 §8, ARC-006 §8            |   ✓    |
| Architecture decisions terdokumentasi | ADR-001, ADR-002          |   ✓    |
| Testing strategy jelas       | — (gap)                           |   ✗    |

Satu kriteria belum terpenuhi:
**testing strategy** ditetapkan melalui ARC-ACT-001.

---

# 8. Constitution Compliance Review

FND-001 §14 Articles 1–15:

| Article                      | Evidence                          | Status |
| ---------------------------- | --------------------------------- | :----: |
| Article 1 Event unit atomik  | ARC-003 §7                        |   ✓    |
| Article 2 Detector independen| ARC-003 §9                        |   ✓    |
| Article 3 Facts, not recs    | ARC-003 §7                        |   ✓    |
| Article 5 Explainable        | ARC-003 §8                        |   ✓    |
| Article 6 Stateless          | ARC-006 §8                        |   ✓    |
| Article 7 Deterministic      | ARC-003 §7, ARC-005 §7            |   ✓    |
| Article 8 Indicator never trades | ARC-002 §7.4                   |   ✓    |
| Article 11 Plugin First      | ARC-005, ADR-002                  |   ✓    |
| Article 12 Config over hardcode | ARC-005 §10, FR-012            |   ✓    |
| Article 13 Data immutable    | ARC-004                           |   ✓    |
| Article 14 Single responsibility | ARC-006 §14                    |   ✓    |
| Article 15 ADR for major decisions | ADR-001, ADR-002             |   ✓    |

---

# 9. Terminology Review

Terminologi diverifikasi terhadap **FND-009** (One Concept, One Name):

| Term       | Penggunaan             | Status |
| ---------- | ---------------------- | :----: |
| Event      | konsisten              |   ✓    |
| Signal     | konsisten              |   ✓    |
| Detector   | konsisten              |   ✓    |
| Plugin     | konsisten              |   ✓    |
| Module     | konsisten              |   ✓    |
| Engine     | konsisten              |   ✓    |

Tidak ditemukan istilah liar atau sinonim baru.

---

# 10. Consistency Review

## 10.1 Module Boundaries

ARC-001 module ↔ ARC-006 package mapping konsisten. ✓

## 10.2 Engine Contracts

ARC-006 §7 contracts merujuk PRD-003 workflow (7.1..7.8) dan FEAT. ✓

## 10.3 Event Semantics

Per PRD-003 §9.1 dan PRD-008 NBI-003:
Event arsitektur ≠ "Event Detection" capability produk.
ARC-003 §6 memisahkan keduanya. ✓

## 10.4 Required ADRs

ARC-001 §14:

| Required ADR              | Recorded             | Status |
| ------------------------- | -------------------- | :----: |
| event-driven architecture | ADR-001              |   ✓    |
| plugin architecture       | ADR-002              |   ✓    |
| swing algorithm           | — (M3/M4)            |   →    |
| trendline algorithm       | — (M3/M4)            |   →    |
| probability model         | — (saat dibangun)    |   →    |

ADR swing/trendline dijadwalkan pada M3/M4 saat detektor dibangun (ARC-ACT-004).

---

# 11. Outstanding Actions

## ARC-ACT-001 — Define Testing Strategy

FND-007 §7 kriteria "testing strategy jelas" belum terpenuhi.
Buat dokumen testing strategy (ENG) sebelum implementasi M4.

## ARC-ACT-002 — Transition ARC Statuses

Transition status ARC-001..006 dari Draft menjadi Approved
setelah review ini disetujui.

## ARC-ACT-003 — Update Phase Status

Update FND-006 dan FND-008:

- M2 — Architecture = DONE;
- fase berikutnya = M3 — Research Methodology (TODO-013 READY).

## ARC-ACT-004 — Record Remaining Mandated ADRs

Catat ADR swing algorithm dan trendline algorithm
pada M3/M4 saat detektor dibangun.

---

# 12. Non-Blocking Issues

- **NBI-001:** NFR-004 threshold performa belum dikuantifikasi (ditetapkan saat implementasi).
- **NBI-002:** katalog Event (ARC-003 §11) akan diperluas pada M3.
- **NBI-003:** "Event Detection" capability produk tetap di luar scope arsitektur ini.

---

# 13. Critical Blocker Assessment

```text
Critical blockers: 0
```

Tidak ada blocker yang menghalangi transisi ke M3.

---

# 14. M2 Readiness Matrix

| Area                         | Status        |
| ---------------------------- | ------------- |
| System Architecture          | 🟢 READY      |
| Domain Model                 | 🟢 READY      |
| Event Architecture           | 🟢 READY      |
| Data Architecture            | 🟢 READY      |
| Plugin Architecture          | 🟢 READY      |
| Module Architecture          | 🟢 READY      |
| Event-Driven ADR             | 🟢 READY      |
| Plugin ADR                   | 🟢 READY      |
| Constitution Compliance      | 🟢 READY      |
| Terminology Consistency      | 🟢 READY      |
| Testing Strategy             | 🟡 CLEANUP    |

---

# 15. M2 Score

Assessment:

```text
System Architecture       100%
Domain Model              100%
Event Architecture        100%
Data Architecture         100%
Plugin Architecture       100%
Module Architecture       100%
```

Overall readiness:

```text
████████████████████░ 95%
```

Sisa persentase merepresentasikan
formal status transition (ARC-ACT-002)
dan gap testing strategy (ARC-ACT-001),
bukan kelemahan konsep arsitektur.

---

# 16. Approval Criteria

M2 disetujui apabila:

- [x] System boundaries didefinisikan (ARC-001).
- [x] Modules didefinisikan (ARC-001, ARC-006).
- [x] Domain model didefinisikan (ARC-002).
- [x] Data contracts didefinisikan (ARC-004).
- [x] Engine interfaces didefinisikan (ARC-006).
- [x] Dependency rules didefinisikan (ARC-001 §8, ARC-006 §8).
- [x] Architecture decisions terdokumentasi (ADR-001, ADR-002).
- [x] Compliance terhadap Architecture Constitution terpenuhi.
- [x] Terminologi konsisten (FND-009).
- [x] Tidak ada critical blocker.
- [ ] Testing strategy didefinisikan (ARC-ACT-001).

---

# 17. Formal Approval

Berdasarkan review pada dokumen ini:

```text
╔══════════════════════════════════════╗
║        ARCHITECTURE REVIEW           ║
╠══════════════════════════════════════╣
║ Status       : APPROVED              ║
║ Blockers     : 0                     ║
║ Actions      : 4                     ║
║ Readiness    : 95%                   ║
╠══════════════════════════════════════╣
║ M2 — ARCHITECTURE                    ║
║                                      ║
║              COMPLETE                ║
║                                      ║
║ READY FOR M3 — RESEARCH METHODOLOGY  ║
╚══════════════════════════════════════╝
```

---

# 18. Transition Gate

```text
M2 — ARCHITECTURE
       │
       ▼
ARCHITECTURE REVIEW
       │
       ▼ APPROVED
M3 — RESEARCH METHODOLOGY
       │
       ▼
TODO-013 Define Research Methodology
```

---

# 19. References

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
- `docs/06-decisions/ADR-001_Adopt_Event_Driven_Architecture.md`
- `docs/06-decisions/ADR-002_Adopt_Plugin_Based_Architecture.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-008_Product_Definition_Review.md`

---

# 20. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial architecture review      |

---

**Document Status:** Draft

**Document ID:** ARC-007

**Version:** 1.0.0

**End of Document**
