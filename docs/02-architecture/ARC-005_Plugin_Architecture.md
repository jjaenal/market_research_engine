---
title: Plugin Architecture
document_id: ARC-005
version: 1.1.0
status: Approved
category: Architecture
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
  - ARC-006
  - PRD-004
  - PRD-005
  - PRD-007

referenced_by:
  - ARC-006

purpose: Define the plugin system for detectors, indicators, and strategies
---

# Plugin Architecture

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ARC-005 mendefinisikan **plugin architecture** dari Market Research Engine (MRE).

Dokumen ini menjawab kebutuhan ADR wajib **plugin architecture**
(ARC-001 §14) dan detail kontrak plugin dari ARC-006 §9.

ARC-005 menetapkan:

- jenis plugin;
- kontrak plugin (interface);
- registrasi dan loading plugin;
- isolasi plugin (Article 11).

---

# 2. Scope

Scope ARC-005:

- jenis plugin (indicator, detector, strategy);
- kontrak plugin;
- mekanisme registrasi/loading;
- isolasi plugin.

Di luar scope ARC-005:

- model Event (ARC-003);
- module layout (ARC-006);
- schema data (ARC-004);
- katalog detektor spesifik (M3 — Research Core).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- arsitek;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per **Article 11 (Plugin First)**, strategi dan detektor
ditambahkan sebagai plugin tanpa mengubah engine (PRD-007 FEAT-011, NFR-006).

Per **Article 12**, plugin dijalankan melalui konfigurasi (FR-012).

Per **TODO-012 critical requirement** (ARC-006 §9):

> Strategy implementation must not
> directly depend on unrelated infrastructure.

Keputusan arsitektur ini dicatat dalam **ADR-002** (plugin).

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term     | Definition                                          |
| -------- | --------------------------------------------------- |
| Plugin   | Ekstensi yang ditambahkan tanpa mengubah engine     |
| Detector | Plugin yang memancarkan Event (ARC-003)            |
| Strategy | Plugin yang mengombinasikan Event menjadi Signal    |
| Registry | Daftar plugin yang terdaftar dan dapat dimuat       |

---

# 6. Plugin Types

| Plugin Type | Package     | Input                        | Output        |
| ----------- | ----------- | ---------------------------- | ------------- |
| Indicator   | `indicators/` | Dataset                     | IndicatorSeries |
| Detector    | `detectors/`  | data + indicator series     | Event         |
| Strategy    | `strategies/` | timeline Event              | Signal        |

---

# 7. Plugin Contract

Setiap plugin mengekspos kontrak inti:

| Atribut          | Deskripsi                                |
| ---------------- | ---------------------------------------- |
| `plugin_id`      | Identitas unik plugin                    |
| `plugin_version` | Versi semantik plugin                    |
| `config_schema`  | Skema konfigurasi (dari YAML experiment) |
| `run(inputs)`    | Fungsi pure: input → output              |

Aturan:

- plugin adalah **pure function** (Article 6, Article 7);
- plugin menerima input hanya melalui kontrak inti;
- plugin tidak membaca state global;
- plugin tidak menulis langsung ke storage (Article 13).

---

# 8. Detector Plugin

Per ARC-003 §9:

```text
detector(data, indicator_series) → Event
```

- output selalu Event (Article 3);
- tidak ada Event yang bocor antar detector (Article 2);
- konfigurasi detektor (parameter) datang dari eksperimen (FR-012).

---

# 9. Strategy Plugin

Per ARC-006 §9 dan TODO-012 critical requirement:

```text
strategy(timeline_event) → Signal
```

- strategy bergantung hanya pada interface inti
  (Event, Signal, konfigurasi), bukan pada engine/infrastructure;
- Signal dapat dijelaskan — menyimpan daftar Event penyusun (Article 5);
- Signal ≠ Trade (Rule 003); eksekusi Trade di luar tanggung jawab strategy.

---

# 10. Registration and Loading

1. Plugin dideklarasikan dalam konfigurasi eksperimen (YAML) —
   `plugin_id` + parameter.
2. Registry memuat plugin dari package yang dikenal
   (`indicators/`, `detectors/`, `strategies/`).
3. Konfigurasi divalidasi terhadap `config_schema`.
4. Plugin dijalankan oleh engine terkait (ARC-006).

Kegagalan:

- `plugin_id` tidak dikenal → eksperimen gagal (PRD-003 §7.4);
- konfigurasi tidak valid → eksperimen gagal (PRD-003 §7.3);
- data tidak cukup (warm-up) → deteksi gagal terdefinisi (PRD-003 §7.4).

---

# 11. Plugin Isolation

Per Article 11 dan NFR-006:

- plugin hanya bergantung pada interface inti;
- tidak ada dependensi silang antar plugin;
- tidak ada akses langsung ke infrastructure
  (engine, storage, network) tanpa melalui kontrak inti;
- menambahkan strategi/detektor baru tidak mengubah engine.

---

# 12. Traceability

| Item              | Requirement / Feature     |
| ----------------- | ------------------------- |
| Plugin contract   | FR-004, FR-012            |
| Plugin system     | FEAT-011, NFR-006         |
| Strategy plugin   | TODO-012 critical requirement |
| Config over hardcode | FR-012                  |

---

# 13. Compliance

| Constitution Article | Plugin requirement                  |
| -------------------- | ----------------------------------- |
| Article 6            | Stateless; plugin tanpa state global |
| Article 7            | Deterministic                       |
| Article 11           | Plugin First                        |
| Article 12           | Config over hardcode (FR-012)      |
| Article 14           | Satu plugin satu tanggung jawab     |

---

# 14. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-003_Event_Architecture.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-005_Non_Functional_Requirements.md`
- `docs/01-product/PRD-007_Feature_Specification.md`
- `docs/06-decisions/ADR-002_Adopt_Plugin_Based_Architecture.md`

---

# 15. Revision History

| Version | Date       | Changes                  |
| ------- | ---------- | ------------------------ |
| 1.1.0   | 2026-08-08 | Approved via M2 Architecture Review (ARC-007) |
| 1.0.0   | 2026-08-08 | Initial plugin architecture |

---

**Document Status:** Approved

**Document ID:** ARC-005

**Version:** 1.1.0

**End of Document**
