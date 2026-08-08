---
title: Domain Model
document_id: ARC-002
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
  - PRD-003
  - PRD-004

referenced_by:
  - ARC-003
  - ARC-004
  - ARC-006

purpose: Define the domain model of MRE — core entities, their attributes, relationships, and semantic distinctions
---

# Domain Model

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ARC-002 mendefinisikan **domain model** dari Market Research Engine (MRE).

Dokumen ini menjawab TODO-010 — Define Domain Model (FND-008).

ARC-002 menetapkan:

- entitas inti (initial entities);
- atribut kunci setiap entitas;
- relasi antar entitas;
- perbedaan semantik antar konsep (Order ≠ Trade ≠ Position, dst).

---

# 2. Scope

Scope ARC-002:

- entitas domain;
- atribut dan relasi;
- semantic distinctions;
- lifecycle utama.

Di luar scope ARC-002:

- data model detail / persistensi (ARC-004);
- event architecture (ARC-003);
- module layout (ARC-006);
- implementasi teknis.

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- arsitek;
- quantitative researcher;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Product phase menghasilkan pipeline (PRD-003):

```text
Import → Validate → Configure → Execute → Signals → Simulate → Statistics → Report → Evaluate
```

ARC-001 menetapkan 10 module.
ARC-002 mendefinisikan entitas yang
mengalir di antara module tersebut.

Terminologi mengikuti **FND-009 — Project Glossary** (One Concept, One Name).

---

# 5. Definitions

| Term       | Definition (FND-009)                          |
| ---------- | --------------------------------------------- |
| Event      | Occurrence yang terdeteksi oleh system        |
| Signal     | Output strategy yang menunjukkan kondisi terpenuhi |
| Order      | Instruksi untuk entry atau exit               |
| Position   | Exposure aktif terhadap instrument            |
| Trade      | Satu completed research transaction lifecycle |
| Candle     | Satu unit observasi market dalam timeframe    |

---

# 6. Domain Model Overview

```text
EXPERIMENT ──uses──► DATASET ──contains──► CANDLE
     │
     └──────────uses──► STRATEGY ──uses──► INDICATOR
                                  │
                                  ▼
                              DETECTOR (module)
                                  │
                                  ▼
                               EVENT ◄── agregasi ──► SIGNAL
                                                          │
                                                          ▼
                                                        ORDER (simulasi)
                                                          │
                                                          ▼
                                                       POSITION
                                                          │
                                                          ▼
                                                        TRADE ──► RESULT ──► REPORT
```

---

# 7. Entity Definitions

## 7.1 Experiment

- **Definition:** prosedur terkontrol untuk menguji hypothesis (FND-009 §8.5).
- **Atribut:** experiment_id, configuration (frozen), dataset_version, status, timestamps.
- **Relasi:** menggunakan satu Dataset; satu Strategy; menghasilkan Report.
- **Pipeline:** PRD-003 §7.3.
- **Constraint:** config over hardcode (Article 12); reproducible (FR-010).

## 7.2 Dataset

- **Definition:** kumpulan data yang digunakan oleh experiment (FND-009 §9.3).
- **Atribut:** dataset_version, symbol, timeframe, date_range, candles, data_integrity.
- **Relasi:** mengandung Candle (1..n); digunakan Experiment.
- **Pipeline:** PRD-003 §7.1, §7.2.
- **Constraint:** immutable (Article 13).

## 7.3 Candle

- **Definition:** satu unit observasi market dalam timeframe (FND-009 §9.6).
- **Atribut:** timestamp, open, high, low, close, volume.
- **Relasi:** bagian dari Dataset.
- **Pipeline:** PRD-003 §7.1.

## 7.4 Indicator

- **Definition:** perhitungan matematis berdasarkan market data (FND-009 §10.4).
- **Atribut:** name, parameters (window, periode), series nilai (IndicatorSeries), symbol, timeframe.
- **Relasi:** digunakan Strategy; menghasilkan data untuk Detector.
- **Pipeline:** PRD-003 §7.4 (input).
- **Constraint:** indicator tidak pernah mengeksekusi Trade (Article 8).

## 7.5 Event

- **Definition:** occurrence yang terdeteksi oleh system (FND-009 §12.1).
- **Atribut:** event_type, timestamp, source_detector, referensi data/candle.
- **Relasi:** unit atomik; dikombinasikan menjadi Signal.
- **Pipeline:** PRD-003 §7.4 output.
- **Constraint:** Event adalah unit atomik (Article 1); fakta, bukan rekomendasi (Article 3).

Contoh event_type: Swing High, Swing Low, Break of Structure, RSI Divergence, Trendline Breakout, EMA Cross.

## 7.6 Signal

- **Definition:** output strategy yang menunjukkan kondisi terpenuhi (FND-009 §13.1).
- **Atribut:** signal_type (LONG / SHORT / NO SIGNAL), events (daftar), timestamp, confirmation.
- **Relasi:** agregasi beberapa Event; masukan bagi simulasi.
- **Pipeline:** PRD-003 §7.5.
- **Constraint:** Signal ≠ Trade (Rule 003); keputusan dapat dijelaskan (Article 5).

## 7.7 Order

- **Definition:** instruksi untuk entry atau exit (FND-009 §14.1).
- **Atribut:** order_type (market/limit/stop), side, price, trigger, execution_status.
- **Relasi:** dihasilkan dari Signal (simulasi); menghasilkan Position.
- **Pipeline:** PRD-003 §7.6.
- **Catatan:** Order hanya pada level simulasi; eksekusi live di luar scope.

## 7.8 Position

- **Definition:** exposure aktif terhadap instrument (FND-009 §15.1).
- **Atribut:** side (long/short), entry_price, size, opened_at, closed_at.
- **Relasi:** lahir dari Order; menjadi Trade setelah exit.
- **Pipeline:** PRD-003 §7.6.

## 7.9 Trade

- **Definition:** satu completed research transaction lifecycle (FND-009 §15.4).
- **Atribut:** trade_id, entry, position, exit, result, holding_period, pnl.
- **Relasi:** hasil evaluasi Signal; masukan Statistik.
- **Pipeline:** PRD-003 §7.6 output.

Lifecycle Trade:

```text
Entry → Position → Exit → Trade Result
```

## 7.10 Strategy

- **Definition:** kumpulan deterministic rules untuk menghasilkan signal/trade decision (FND-009 §10.1).
- **Atribut:** rules, parameters, detector_set, signal_definition.
- **Relasi:** digunakan Experiment; menggunakan Indicator.
- **Pipeline:** PRD-003 §7.4.
- **Constraint:** deterministic (Article 7); strategi sebagai plugin (Article 11).

## 7.11 Result

- **Definition:** output pengukuran dari Trade ledger dan Event/Signal.
- **Atribut:** metrics (win rate, expectancy, drawdown, dst), sample_size, experiment_id.
- **Relasi:** dihasilkan dari Trade; masukan Report.
- **Pipeline:** PRD-003 §7.7.

## 7.12 Report

- **Definition:** output terstruktur dan reproducible dari eksperimen.
- **Atribut:** report_id, experiment_id, configuration, metadata dataset, metrics, conclusion_area.
- **Relasi:** menyajikan Result.
- **Pipeline:** PRD-003 §7.8.
- **Constraint:** report read-only (Article 9).

---

# 8. Semantic Distinctions

TODO-010 mewajibkan model membedakan
konsep yang secara semantik berbeda.

| Konsep A      | Konsep B      | Perbedaan                                             |
| ------------- | ------------- | ----------------------------------------------------- |
| Event         | Signal        | Event = fakta; Signal = agregasi beberapa Event        |
| Signal        | Trade         | Signal ≠ eksekusi (Rule 003)                           |
| Order         | Trade         | Order = instruksi; Trade = lifecycle selesai           |
| Order         | Position      | Order = instruksi; Position = exposure aktif           |
| Position      | Trade         | Position = exposure; Trade = selesai exit + result     |
| Indicator     | Detector      | Indicator = data; Detector = menghasilkan Event        |

---

# 9. Lifecycle

FND-001 Article 1:

```text
Event
  ↓
Signal
  ↓
Decision
  ↓
Trade
```

Sesuai PRD-003, Decision diekspresikan
sebagai execution rules pada SIMULATION module.

---

# 10. Compliance

| Constitution Article | Domain requirement                              |
| -------------------- | ----------------------------------------------- |
| Article 1            | Event unit atomik; Trade lahir dari evaluasi Signal |
| Article 2            | Detector independen (Event tidak bocor antar detector) |
| Article 3            | Event adalah fakta, bukan rekomendasi           |
| Article 4            | Signal = agregasi Event                         |
| Article 5            | Signal menyimpan daftar Event penyusunnya       |
| Article 13           | Dataset immutable                               |

---

# 11. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`

---

# 12. Revision History

| Version | Date       | Changes                |
| ------- | ---------- | ---------------------- |
| 1.1.0   | 2026-08-08 | Approved via M2 Architecture Review (ARC-007) |
| 1.0.0   | 2026-08-08 | Initial domain model   |

---

**Document Status:** Approved

**Document ID:** ARC-002

**Version:** 1.1.0

**End of Document**
