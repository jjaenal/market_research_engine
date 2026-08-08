---
title: Event Engine
document_id: ENG-002
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
  - ARC-001
  - ARC-002
  - ARC-003
  - ARC-004
  - ARC-005
  - ARC-006
  - ARC-007
  - PRD-003
  - PRD-004
  - DEV-002
  - ENG-001
  - ENG-008

referenced_by:
  - FND-006
  - FND-008
  - ENG-003

purpose: Define the Event Engine implementation spec — detectors, Event model usage, and timeline orchestration (TODO-017, FEAT-004)
---

# Event Engine

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ENG-002 mendefinisikan **Event Engine** — spesifikasi implementasi
untuk TODO-017 (Build Event Engine) dan FEAT-004 (Execute Strategy).

Dokumen ini menurunkan model Event (ARC-003)
dan kontrak detektor (ARC-005) menjadi engine yang dapat dibangun.

---

# 2. Scope

Scope ENG-002:

- detektor awal (swing, RSI trendline, price confirmation);
- model Event (ARC-003 §7);
- orchestrasi timeline Event (ARC-006 §7.3).

Di luar scope ENG-002:

- sinyal (ENG-003);
- plugin detail (ARC-005);
- indikator (ENG-008).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per ARC-006 §7.3:

```text
EventEngine: detect(dataset, indicator_series, detector_set) → Event timeline
```

Per ARC-003, Event adalah unit atomik (Article 1);
detektor independen (Article 2);
detektor menghasilkan fakta, bukan rekomendasi (Article 3).

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term        | Definition                                      |
| ----------- | ----------------------------------------------- |
| Event       | Fakta atomik dari detektor (ARC-003)            |
| Detector    | Plugin yang memancarkan Event (ARC-005)         |
| Timeline    | Urutan Event terurut waktu                      |
| Swing       | Pivot / fractal point (FND-009 §11)             |
| Trendline   | Garis yang merepresentasikan hubungan market (FND-009 §10.6) |

---

# 6. Event Model

Per ARC-003 §7:

| Atribut           | Tipe      | Deskripsi                              |
| ----------------- | --------- | -------------------------------------- |
| `event_type`      | string    | Jenis fakta                            |
| `timestamp`       | datetime  | Waktu kejadian (timezone-aware)        |
| `source_detector` | string    | Detector pemancar                      |
| `reference`       | object    | Referensi data/candle pendukung        |
| `payload`         | object    | Data kontekstual (opsional)            |
| `experiment_id`   | string    | Eksperimen asal                        |

Event immutable (Article 13), deterministic (Article 7),
fakta bukan rekomendasi (Article 3).

---

# 7. Initial Detectors

## 7.1 Swing Detector (fractal)

Mendeteksi Swing High / Swing Low pada suatu series
(RSI atau price) menggunakan window fractal `left`/`right`:

```text
swing_high di i: series[i] > series[j] untuk semua j di [i-left, i+right], j ≠ i
swing_low  di i: series[i] < series[j] untuk semua j di [i-left, i+right], j ≠ i
```

Event: `SWING_HIGH`, `SWING_LOW`.

Algoritma dicatat dalam **ADR-003**.

## 7.2 RSI Trendline Detector

Membangun trendline dari dua swing terakhir pada RSI:

- up-trendline dari dua swing low terakhir (slope > 0);
- `RSI_TRENDLINE_CREATED` saat swing low kedua terkonfirmasi;
- `RSI_TRENDLINE_BROKEN` saat RSI menembus garis trendline aktif.

Algoritma dicatat dalam **ADR-004**.

## 7.3 Price Confirmation Detector

Mendeteksi konfirmasi momentum harga secara independen:

- `PRICE_CONFIRMATION` saat close menembus highest high
  dalam window lookback terakhir.

Detector ini tidak membaca hasil detector lain (Article 2).

---

# 8. Detector Independence

Per Article 2:

- setiap detector hanya membaca data + indicator series;
- tidak ada Event yang bocor antar detector;
- integrasi hanya terjadi pada Signal Engine (ENG-003).

---

# 9. Timeline Orchestration

```text
candles + indicators
        ↓
SwingDetector ─┐
RsiTrendline ──┼→ EventEngine → timeline (sorted by timestamp)
PriceConfirm ──┘
```

- seluruh Event digabung dan diurutkan berdasarkan timestamp;
- Event immutable dan deterministic.

---

# 10. Testing (DEV-002)

- unit test tiap detector terhadap data referensi;
- test Event model (immutable, fields);
- test timeline terurut;
- test determinism dan no-lookahead.

---

# 11. Traceability

| Item              | Requirement / Feature     |
| ----------------- | ------------------------- |
| Event model       | ARC-003 §7, Article 1, 3  |
| Detectors         | TODO-017, FEAT-004        |
| Independence      | Article 2                 |
| Timeline          | ARC-006 §7.3              |

---

# 12. Compliance

| Constitution Article | Event Engine requirement    |
| -------------------- | --------------------------- |
| Article 1            | Event unit atomik           |
| Article 2            | Detector independen         |
| Article 3            | Fakta, bukan rekomendasi    |
| Article 7            | Deterministic               |
| Article 13           | Event immutable             |

---

# 13. References

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
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/04-development/DEV-002_Testing_Strategy.md`
- `docs/03-engine/ENG-001_Data_Engine.md`
- `docs/03-engine/ENG-008_Indicator_Layer.md`
- `docs/06-decisions/ADR-003_Swing_Algorithm.md`
- `docs/06-decisions/ADR-004_Trendline_Algorithm.md`

---

# 14. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial event engine spec        |

---

**Document Status:** Draft

**Document ID:** ENG-002

**Version:** 1.0.0

**End of Document**
