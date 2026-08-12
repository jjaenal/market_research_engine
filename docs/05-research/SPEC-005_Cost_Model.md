---
title: Cost Model
document_id: SPEC-005
version: 1.0.0
status: Draft
category: Research
owner: Market Research Engine Core Team
created: 2026-08-11
last_updated: 2026-08-11

depends_on:
  - FND-009
  - RSH-001
  - RSH-002
  - ENG-005
  - ENG-006

referenced_by:
  - EXP-002
  - EXP-003
  - EXP-004
  - EXP-005
  - EXP-006
  - EXP-007
  - EXP-008

purpose: Unambiguous, reproducible venue cost accounting and engine-computed breakeven (audit E-3/E-7)
---

# SPEC-005 — Cost Model

> Measure the Market. Discover the Edge.

---

# 1. Purpose

SPEC-005 mendefinisikan **akuntansi biaya venue yang tidak ambigu dan
reproducible** untuk backtesting OHLC, termasuk komputasi **breakeven**
yang dapat dieksekusi dari kode.

Dokumen ini menjawab temuan audit E-3 (breakeven — metrik penerimaan
utama — hanya dihitung manual via interpolasi di dokumen) dan E-7
(venue cost aktual 1.0 bps/side tidak ada dalam grid robustness).

---

# 2. Scope

Scope SPEC-005:

- commission per sisi (fraksi notional);
- slippage per sisi (konservatif);
- asumsi single-price (tanpa bid/ask spread);
- cost timing (entry dan exit);
- komputasi breakeven engine-level.

Di luar scope SPEC-005:

- eksekusi tick-level, partial fills;
- fee schedule spesifik venue;
- formula entry/exit (SPEC-003/SPEC-004).

---

# 3. Inputs

| Input             | Deskripsi                                        |
| ----------------- | ------------------------------------------------ |
| `entry_price`     | Harga fill entry (open bar entry, BEFORE slippage) |
| `exit_price`      | Harga fill exit (raw)                            |
| `position_size`   | Ukuran posisi (default 1.0)                      |
| `commission_rate` | Fraksi notional per sisi (default 0.0)           |
| `slippage_rate`   | Fraksi harga per sisi (default 0.0)              |

---

# 4. Deterministic Rules

## 4.1 Slippage (Konservatif)

- Entry memperburuk harga; exit memperburuk harga (mengecilkan gap
  keuntungan).
- long:
  - entry = `open × (1 + rate)`;
  - exit  = `exit_raw × (1 − rate)`.
- short:
  - entry = `open × (1 − rate)`;
  - exit  = `exit_raw × (1 + rate)`.
- `rate == 0.0` → harga tidak berubah.

## 4.2 Commission

- `commission = commission_rate × (notional_entry + notional_exit)`
  (round trip — biaya dikenakan pada entry **dan** exit).
- `pnl = Δharga × position_size − commission`.

## 4.3 Single-Price Series

- Seri OHLC adalah **harga tunggal**; spread bid/ask **tidak dimodelkan**.
- Bila venue cost riil mencakup spread, spread tersebut **diwakili** ke
  dalam commission/slippage rate (lihat EXP-002 §9.5) dan dinyatakan
  eksplisit.

## 4.4 Cost Timing

- Slippage entry diterapkan pada open bar entry.
- Slippage exit diterapkan pada exit raw (level SL/TP, open gap,
  close scheduled, atau close bar terakhir — SPEC-004).

## 4.5 Breakeven (E-3)

- Breakeven = total biaya per sisi (bps) di mana expectancy menyentuh
  nol: `expectancy(total_bps) > 0` untuk `total_bps < breakeven`.
- Dihitung **di engine** (`compute_breakeven`, `src/mre/core/robustness.py`)
  via binary search pada total bps dengan menjaga rasio
  commission:slippage konfigurasi (proportional scaling, `_split_cost`).
- Expectancy monoton non-increasing terhadap total biaya per sisi → root
  tunggal.
- Hasil khusus:
  - expectancy ≤ 0 pada biaya nol → `0.0` (gross edge tidak ada);
  - expectancy > 0 hingga `max_bps` (20) → `None` (tidak tercapai).

## 4.6 Representatif Venue Cost (E-7)

- Cost grid robustness **wajib memuat** venue cost aktual yang dipakai
  baseline (1.0 bps/side total: commission 3e-05 + slippage 7e-05).
- Entri pertama grid = zero-cost control (determinism check).

---

# 5. Edge Cases

| Kasus                          | Perilaku deterministik             |
| ------------------------------ | ---------------------------------- |
| Zero-cost baseline             | Slippage/commission 0 → harga murni |
| ekspektasi negatif pada 0 cost | breakeven = 0.0                     |
| Positive sampai max_bps        | breakeven = None                    |
| Harga NaN                      | Dengan asumsi data tervalidasi (validator) — tidak dihandel khusus |

---

# 6. Non-Goals

- tick-level execution;
- fee schedule / reglementer venue spesifik;
- partial fills;
- spread dinamis intrabar.

---

# 7. Traceability

| Item                       | Code / Doc                                            |
| -------------------------- | ----------------------------------------------------- |
| `ExecutionConfig`          | `src/mre/models/execution.py`                          |
| `_apply_slippage` / commission | `src/mre/engines/simulation_engine.py`               |
| `compute_breakeven`/`_split_cost` | `src/mre/core/robustness.py`                     |
| `COST_GRID` (venue cost ter-sertakan, E-7) | `src/mre/core/robustness.py`            |
| Venue cost 1.0 bps/side    | EXP-002 §9.5 (spread + commission + slippage ≈ 1.0 bps/side) |

---

# 8. Compliance

| Document / Rule  | Requirement                    |
| ---------------- | ------------------------------ |
| FND-009          | Backtest ≠ Proof               |
| RSH-001 §7.2     | Pre-registration               |
| Article 7        | Deterministic                  |
| Article 13       | Immutable data                 |

---

# 9. References

- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/07-experiments/EXP-002_RSI_Trendline_Breakout_Real_Venue_Cost.md`
- `src/mre/core/robustness.py`
- `src/mre/engines/simulation_engine.py`

---

# 10. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-11 | Initial Cost Model spec (E-3/E-7) |

---

**Document Status:** Draft

**Document ID:** SPEC-005

**Version:** 1.0.0

**End of Document**