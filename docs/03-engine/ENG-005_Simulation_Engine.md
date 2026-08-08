---
title: Simulation Engine
document_id: ENG-005
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
  - ARC-002
  - ARC-004
  - ARC-006
  - PRD-001
  - PRD-003
  - PRD-004
  - PRD-006
  - PRD-007
  - RSH-001
  - DEV-002
  - ENG-003

referenced_by:
  - FND-006
  - FND-008
  - ENG-006

purpose: Define the Simulation Engine implementation spec — order/position/trade lifecycle and execution rules (TODO-019, FEAT-006)
---

# Simulation Engine

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ENG-005 mendefinisikan **Simulation Engine** — spesifikasi implementasi
untuk TODO-019 (Build Simulation Engine) dan FEAT-006 (Trade Simulation).

Dokumen ini menurunkan model Order/Position/Trade (ARC-002 §7.7–7.9).

---

# 2. Scope

Scope ENG-005:

- lifecycle Entry → Position → Exit → Trade Result;
- execution rules (position sizing, transaction cost, slippage);
- optional stop-loss / take-profit;
- P&L dan holding period.

Di luar scope ENG-005:

- live trading / order execution (Rule 003, PRD-001 §11);
- optimasi (PRD-001 §11);
- statistik (ENG-006).

Catatan: pada MVP, eksperimen baseline tidak menggunakan
TP/SL (PRD-006 §9); engine tetap mendukung TP/SL
sebagai execution rule opsional untuk eksperimen berikutnya.

---

# 3. Audience

- tim MRE;
- software engineer;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per ARC-006 §7.5:

```text
SimulationEngine: simulate(signals, execution_rules) → Trade ledger
```

Per PRD-003 §7.6:

- input: Signal;
- processing: mengevaluasi behavior Signal menjadi simulated trades
  dengan execution rules (position sizing, transaction cost, slippage);
- failure conditions: semantik Signal tidak valid; execution rules tidak ada.

Critical requirement (TODO-019): no future information may influence
past execution.

---

# 5. Definitions

Terminologi mengikuti **FND-009**.

| Term        | Definition                                  |
| ----------- | ------------------------------------------- |
| Order       | Instruksi entry/exit level simulasi (FND-009 §14.1) |
| Position    | Exposure aktif terhadap instrument (FND-009 §15.1) |
| Trade       | Satu completed research transaction lifecycle (FND-009 §15.4) |
| Execution   | Asumsi eksekusi (entry/exit, sizing) (RSH-001 §14) |

---

# 6. Domain Models

## 6.1 Order (ARC-002 §7.7)

| Atribut           | Tipe   | Deskripsi                |
| ----------------- | ------ | ------------------------ |
| `order_type`      | string | market / limit / stop    |
| `side`            | string | long / short             |
| `price`           | float  | Harga eksekusi           |
| `trigger`         | object | Referensi candle         |
| `execution_status`| string | executed / pending       |

## 6.2 Position (ARC-002 §7.8)

| Atribut      | Tipe     | Deskripsi          |
| ------------ | -------- | ------------------ |
| `side`       | string   | long / short       |
| `entry_price`| float    | Harga masuk        |
| `size`       | float    | Ukuran posisi      |
| `opened_at`  | datetime | Waktu buka         |
| `closed_at`  | datetime | Waktu tutup        |

## 6.3 Trade (ARC-002 §7.9)

| Atribut         | Tipe     | Deskripsi                   |
| --------------- | -------- | --------------------------- |
| `trade_id`      | string   | ID deterministik            |
| `entry`         | Order    | Order entry                 |
| `position`      | Position | Posisi                      |
| `exit`          | Order    | Order exit                  |
| `result`        | string   | WIN / LOSS / BREAKEVEN      |
| `holding_period`| timedelta| Durasi posisi               |
| `pnl`           | float    | P&L neto (setelah biaya)    |

---

# 7. Execution Rules

| Atribut            | Tipe   | Default | Deskripsi                      |
| ------------------ | ------ | ------- | ------------------------------ |
| `position_size`    | float  | 1.0     | Unit posisi tetap              |
| `commission_rate`  | float  | 0.0     | Fraksi notional per sisi       |
| `slippage_rate`    | float  | 0.0     | Fraksi harga per sisi          |
| `hold_bars`        | int    | 10      | Exit setelah N bar             |
| `stop_loss`        | float  | None    | Level SL (opsional, off di MVP)|
| `take_profit`      | float  | None    | Level TP (opsional, off di MVP)|

Slippage selalu konservatif (memperburuk harga).

---

# 8. Simulation Semantics

```text
Signal → entry (open bar berikutnya + slippage)
       → Position
       → exit (hold_bars / SL / TP / data habis)
       → Trade (pnl, result, holding_period)
```

1. Entry: bar setelah Signal (`entry_bar = signal_index + 1`);
   tidak ada bar berikutnya → Signal tidak dieksekusi.
2. Exit prioritas per bar:
   - SL lebih dulu (konservatif long/short);
   - lalu TP;
   - lalu scheduled `hold_bars` exit di close.
3. Data habis sebelum exit → exit di close bar terakhir.
4. Setiap Signal menghasilkan satu Trade independen.

## In-Bar Assumption

- TP/SL dievaluasi dari entry bar (intrabar, bar-level).
- Bila SL dan TP sama-sama kena dalam satu bar:
  - long: SL dianggap lebih dulu (konservatif);
  - short: SL dianggap lebih dulu (konservatif).
- Gap: bila open sudah melampaui level → exit di open.

## P&L

```text
long:  pnl = (exit_price - entry_price) * size - commission
short: pnl = (entry_price - exit_price) * size - commission
commission = commission_rate * (notional_entry + notional_exit)
```

Slippage termuat dalam entry/exit price.

---

# 9. Failure Conditions

- execution rules invalid (size ≤ 0, rate < 0, hold_bars < 1) → ValueError;
- signal_type tidak dikenal → ValueError;
- signal tanpa timestamp di candles → dilewati (NO SIGNAL semantics).

---

# 10. No Future Information (TODO-019)

- loop hanya membaca bar sampai exit;
- truncation test: memperpanjang data tidak mengubah
  Trade yang sudah selesai sebelum titik truncation.

---

# 11. Testing (DEV-002)

- unit test model Order/Position/Trade;
- unit test execution rules (slippage, commission, hold_bars, SL/TP);
- unit test no-future-information dan determinism.

---

# 12. Traceability

| Item           | Requirement / Feature       |
| -------------- | --------------------------- |
| Models         | ARC-002 §7.7–7.9            |
| simulate       | ARC-006 §7.5, FEAT-006, FR-006 |
| Execution rules| RSH-001 §14                 |
| No lookahead   | TODO-019 critical requirement |

---

# 13. Compliance

| Article / Rule   | Simulation requirement      |
| ---------------- | --------------------------- |
| Article 7        | Deterministic               |
| Article 13       | Models immutable            |
| Rule 003         | Signal ≠ Trade; simulasi, bukan live |

---

# 14. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-004_Data_Architecture.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/01-product/PRD-001_Product_Vision.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `docs/01-product/PRD-007_Feature_Specification.md`
- `docs/05-research/RSH-001_Research_Methodology.md`
- `docs/04-development/DEV-002_Testing_Strategy.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`

---

# 15. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial simulation engine spec   |

---

**Document Status:** Draft

**Document ID:** ENG-005

**Version:** 1.0.0

**End of Document**
