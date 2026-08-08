---
title: Event Architecture
document_id: ARC-003
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
  - ARC-006
  - PRD-003
  - PRD-004
  - PRD-008

referenced_by:
  - ARC-006

purpose: Define the Event model, lifecycle, and constraints of the event-driven core
---

# Event Architecture

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ARC-003 mendefinisikan **event architecture** dari Market Research Engine (MRE).

Dokumen ini menjawab kebutuhan ADR wajib
**event-driven architecture** (ARC-001 §14) dan menurunkan
model Event dari ARC-002 §7.5 menjadi arsitektur yang dapat diimplementasi.

ARC-003 menetapkan:

- model Event (skema atribut);
- siklus hidup Event;
- kontrak detektor;
- constraint Event (Article 1, 3, 5, 6, 7, 13).

---

# 2. Scope

Scope ARC-003:

- model Event dan atribut;
- timeline Event;
- kontrak detektor;
- integrasi Event → Signal.

Di luar scope ARC-003:

- schema data OHLCV (ARC-004);
- plugin design (ARC-005);
- module layout dan interface engine (ARC-006);
- capability produk "Event Detection" (FND-010 §32).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- arsitek;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per Article 1, **Event adalah unit atomik** sistem.
Signal mengagregasi Event; Trade lahir dari evaluasi Signal.

Detektor adalah satu-satunya sumber Event (Article 2, Article 3).
Indikator menghasilkan data; tidak pernah menghasilkan rekomendasi (Article 8).

Keputusan arsitektur ini dicatat dalam **ADR-001** (event-driven).

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term         | Definition                                         |
| ------------ | -------------------------------------------------- |
| Event        | Fakta atomik yang dihasilkan detektor (FND-009 §12) |
| Detector     | Komponen yang memancarkan Event dari data          |
| Timeline     | Urutan Event terurut waktu untuk sebuah dataset    |
| Signal       | Agregasi beberapa Event (FND-009 §13)              |
| Event stream | Aliran Event hasil deteksi                         |

---

# 6. Event Semantics

Per **PRD-003 §9.1** (klarfikasi PRD-ACT-003), dua makna "Event"
tidak boleh dicampur:

| Makna                    | Konteks            |
| ------------------------ | ------------------ |
| **Event arsitektur**     | Mekanisme: fakta atomik dari detektor (dokumen ini) |
| **"Event Detection"**    | Capability produk (FND-010 §32) |

Dokumen ini hanya membahas Event sebagai mekanisme arsitektur.

---

# 7. Event Model

Per ARC-002 §7.5:

| Atribut           | Tipe      | Deskripsi                                    |
| ----------------- | --------- | -------------------------------------------- |
| `event_type`      | string    | Jenis fakta (Swing High, RSI Divergence, …)  |
| `timestamp`       | datetime  | Waktu kejadian (timezone-aware, ISO 8601)    |
| `source_detector` | string    | Detector pemancar (id plugin)                |
| `reference`       | candle/…  | Referensi data/candle pendukung               |
| `payload`         | object    | Data tambahan kontekstual (opsional)          |
| `experiment_id`   | string    | Eksperimen asal (konteks reproducibility)    |

Constraint:

- Event **immutable** (Article 13) — tidak ada mutasi setelah dibuat;
- Event **deterministic** (Article 7) — detector yang sama + data yang sama menghasilkan Event yang sama;
- Event adalah **fakta, bukan rekomendasi** (Article 3) — tidak ada arah Trade di dalam Event.

---

# 8. Event Lifecycle

```text
data + indicator series
        ↓
    Detector (pure function)
        ↓
    Event (fakta, immutable)
        ↓
    Timeline / Event stream
        ↓
    SignalEngine → Signal (agregasi)
        ↓
    SimulationEngine → Trade
```

Per Article 5, setiap Signal menyimpan daftar Event penyusunnya —
keputusan selalu dapat dijelaskan.

---

# 9. Detector Contract

Per Article 2 dan PRD-004 FR-004:

- Detector adalah **pure function**: input (data + indicator series), output Event;
- Detector independen — **tidak ada Event yang bocor antar detector**;
- Detector menghasilkan Event, bukan rekomendasi;
- Detector menerima input hanya melalui kontrak inti (konfigurasi, Event, Signal) — per Article 11.

---

# 10. EventEngine

Kontrak EventEngine (ARC-006 §7.3):

```text
detect(dataset, indicator_series, detector_set) → Event timeline
```

Responsibility:

- menjalankan detektor sebagai pure functions;
- mengelola timeline Event sebagai unit atomik;
- menangani warm-up (data tidak cukup) sebagai failure condition (PRD-003 §7.4);
- output deterministik untuk dataset yang sama.

---

# 11. Event Catalog (Initial)

Contoh `event_type` (ARC-002 §7.5):

| event_type             | Sumber         | Keterangan                         |
| ---------------------- | -------------- | ---------------------------------- |
| `SWING_HIGH`           | swing detector | Swing High terdeteksi              |
| `SWING_LOW`            | swing detector | Swing Low terdeteksi               |
| `BREAK_OF_STRUCTURE`   | structure det. | Break of structure                 |
| `RSI_DIVERGENCE`       | rsi detector   | Divergensi RSI                     |
| `TRENDLINE_BREAKOUT`   | trendline det. | Breakout trendline                 |
| `EMA_CROSS`            | ema detector   | Perlintasan EMA                    |

Katalog ini akan diperluas pada **M3 — Research Core**
mengikuti kontrak detektor (ARC-005).

---

# 12. Traceability

| Item              | Requirement / Feature     |
| ----------------- | ------------------------- |
| Event model       | FR-004, Article 1, 3      |
| Detector contract | FR-004, Article 2, 11     |
| EventEngine       | FEAT-004, PRD-003 §7.4    |
| Event immutability| Article 13, NFR-003       |

---

# 13. Compliance

| Constitution Article | Event requirement                     |
| -------------------- | ------------------------------------- |
| Article 1            | Event unit atomik                     |
| Article 2            | Detector independen; no event leak    |
| Article 3            | Event = fakta, bukan rekomendasi      |
| Article 5            | Keputusan dapat dijelaskan (via Signal) |
| Article 6            | Stateless; Event stateless            |
| Article 7            | Deterministic                         |
| Article 13           | Data/Event immutable                   |

---

# 14. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-008_Product_Definition_Review.md`
- `docs/06-decisions/ADR-001_Event_Driven_Architecture.md`

---

# 15. Revision History

| Version | Date       | Changes                     |
| ------- | ---------- | --------------------------- |
| 1.1.0   | 2026-08-08 | Approved via M2 Architecture Review (ARC-007) |
| 1.0.0   | 2026-08-08 | Initial event architecture  |

---

**Document Status:** Approved

**Document ID:** ARC-003

**Version:** 1.1.0

**End of Document**
