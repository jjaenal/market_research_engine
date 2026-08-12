---
title: SL/TP & Exit Rules
document_id: SPEC-004
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

referenced_by:
  - EXP-004
  - EXP-008

purpose: Unambiguous stop-loss / take-profit and hold-exit semantics for OHLC backtesting (audit E-9)
---

# SPEC-004 — SL/TP & Exit Rules

> Measure the Market. Discover the Edge.

---

# 1. Purpose

SPEC-004 mendefinisikan **semantik exit deterministik** untuk Stop Loss /
Take Profit (SL/TP) dan hold-exit pada backtesting OHLC.

Dokumen ini menjawab temuan audit E-9 (SL/TP exit documentation tidak
standar): EXP-004 §10 kontradiktif dengan kode, EXP-008 membiarkan
mekanisme exit tidak terdokumentasi. Dokumen ini menjadi **single source
of truth** yang diimplementasikan di `simulation_engine.py`
(`_find_exit`, `_resolve_stop_take`).

---

# 2. Scope

Scope SPEC-004:

- SL/TP absolute dan ATR-multiple;
- prioritas same-bar collision;
- gap handling (open melampaui level);
- hold-bars exit;
- end-of-data exit;
- eligibility SL/TP sejak entry bar.

Di luar scope SPEC-004:

- trailing stop, session-close berbasis waktu;
- tick-level fills, partial fills;
- entry semantics (SPEC-003 / ENG-005).

---

# 3. Inputs

| Input         | Deskripsi                                   |
| ------------- | ------------------------------------------- |
| `entry_price` | Harga entry (open bar entry + slippage)     |
| `entry_bar`   | Index bar entry                             |
| `atr_series`  | Serial ATR (untuk SL/TP ATR-multiple)       |
| SL/TP config  | `stop_loss`, `take_profit` dan/atau `stop_loss_atr`, `take_profit_atr`, `atr_period` |
| `hold_bars`   | Jumlah bar hold sebelum scheduled exit      |

---

# 4. Deterministic Rules

## 4.1 ATR Anchor (E-2)

- SL/TP ATR-multiple dihitung dengan ATR pada bar **terakhir yang telah
  ditutup**: `atr_series[entry_bar - 1]`.
- ATR pada bar entry TIDAK digunakan — bar entry belum lengkap saat
  level harus ditentukan (same-bar leak).
- `entry_bar >= 1` selalu berlaku (entry paling awal di bar 1).
- ATR NaN (warm-up) → level SL/TP tidak diset (tanpa SL/TP).

## 4.2 Level Price

```text
long:  stop = entry_price − stop_loss_atr × ATR      take = entry_price + take_profit_atr × ATR
short: stop = entry_price + stop_loss_atr × ATR      take = entry_price − take_profit_atr × ATR
```

Level absolute (`stop_loss`/`take_profit`) dipakai apa adanya.
Level ATR-multiple menang jika keduanya dikonfigurasi.

## 4.3 Same-Bar Collision Priority

Dalam satu bar, pemeriksaan berurutan:

```text
1. Stop Loss  (konservatif: dianggap lebih dulu)
2. Take Profit
```

Long:

- SL terisi jika `open <= sl` (gap) atau `low <= sl`;
- TP terisi jika `open >= tp` (gap) atau `high >= tp`.

Short:

- SL terisi jika `open >= sl` (gap) atau `high >= sl`;
- TP terisi jika `open <= tp` (gap) atau `low <= tp`.

## 4.4 Gap Handling

- Bila `open` bar sudah melampaui level → exit di **open** (long: `open <= sl`
  atau `open >= tp`; short: `open >= sl` atau `open <= tp`).
- Bila hanya intrabar yang menyentuh level → exit di **level**.
- Gap yang melampaui SL dan TP sekaligus dalam satu bar diselesaikan
  oleh urutan 4.3 (SL dulu → exit di open, konservatif).
- Tidak ada rekonstruksi path intrabar.

## 4.5 Hold-Bars Exit

- Exit terjadwal pada close bar `entry_bar + hold_bars`.
- Pemeriksaan SL/TP berlaku untuk semua bar dari `entry_bar` (termasuk
  bar entry itu sendiri — SL/TP eligible sejak entry bar, dinyatakan
  eksplisit; tidak ada satu bar "amnestied").
- Bila data habis sebelum exit → exit di close bar terakhir.

---

# 5. Edge Cases

| Kasus                                  | Perilaku deterministik            |
| -------------------------------------- | --------------------------------- |
| SL dan TP kena dalam satu bar          | SL dulu (4.3)                     |
| Open melampaui kedua level              | SL dulu → exit di open (4.3/4.4)  |
| ATR NaN (warm-up)                      | Level tidak diset                 |
| Candle terakhir                          | Exit di close bar terakhir        |
| hold_bars tercapai tanpa sentuh level  | Exit di close bar scheduled       |

---

# 6. Non-Goals

- trailing stop;
- time-based session closes;
- intrabar fills / partial fills;
- bid/ask spread (single-price OHLC, SPEC-005).

---

# 7. Traceability

| Item                     | Code / Doc                       |
| ------------------------ | -------------------------------- |
| `_resolve_stop_take`     | `src/mre/engines/simulation_engine.py` |
| `_find_exit`             | `src/mre/engines/simulation_engine.py` |
| RQ-007 (SL/TP ATR-multiple) | ARC-008 §14.2                |
| E-2 (ATR anchor)         | Audit findings, `_resolve_stop_take` |
| E-9 (standardize docs)   | Audit findings                  |

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
- `docs/05-research/RSH-001_Research_Methodology.md`
- `docs/05-research/RSH-002_Experiment_Specification.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `src/mre/engines/simulation_engine.py`

---

# 10. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-11 | Initial SL/TP & Exit Rules spec (E-9) |

---

**Document Status:** Draft

**Document ID:** SPEC-004

**Version:** 1.0.0

**End of Document**
