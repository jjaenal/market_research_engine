---
title: Breakout Detection
document_id: SPEC-002
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
  - ENG-002

referenced_by:
  - EXP-001
  - EXP-005
  - EXP-006
  - EXP-007
  - EXP-008

purpose: Deterministic, close-vs-level price breakout definition used by all momentum and structure strategies (audit E-9)
---

# SPEC-002 — Breakout Detection

> Measure the Market. Discover the Edge.

---

# 1. Purpose

SPEC-002 mendefinisikan **breakout harga deterministik** berbasis
**close vs level** (Donchian N-bar) yang menjadi dasar event
`PRICE_CONFIRMATION` dan komparasi level struktural swing-high.

Dokumen ini menutup ambiguitas audit: apakah breakout dihitung dari
close, wick/intrabar, atau gap; bagaimana tie dihandle; dan kapan
breakout *knowable*.

---

# 2. Scope

Scope SPEC-002:

- event `PRICE_CONFIRMATION` (close > highest-high N-bar);
- peran trigger vs konfirmasi dalam struktur sinyal;
- tie handling (equal close vs level);
- close vs wick/intrabar;
- komparasi terhadap level struktural swing-high (EXP-007/008);
- timing knowability breakout.

Di luar scope SPEC-002:

- break trendline pada seri indikator (RSI trendline — ADR-004);
- swing/fractal detection (SPEC-001);
- sinyal / entry semantics (SPEC-003).

---

# 3. Inputs

| Input      | Deskripsi                                          |
| ---------- | -------------------------------------------------- |
| `candles`  | Seri candle OHLC terurut                           |
| `lookback` | Jumlah bar window tinggi tertinggi (default 20)    |
| level      | Level pembanding opsional (highest-high atau swing-high fractal) |

---

# 4. Deterministic Rules

## 4.1 PRICE_CONFIRMATION (Donchian)

- Breakout terjadi jika dan hanya jika
  `close[i] > max(high[j], j ∈ [i−lookback, i−1])` (**strict**).
- Candle `i` sendiri **tidak** termasuk ke dalam window-nya.
- **Wick/intrabar BUKAN breakout**: harga intraday yang menembus level
  namun close tidak di atasnya tidak menghasilkan event.
- **Tie tidak memicu**: `close[i] == level` tidak menghasilkan event.

## 4.2 Level Struktural (Swing-High)

- Untuk strategi struktur (EXP-007/008), level pembanding adalah swing-high
  fractal (SPEC-001); komparasi tetap `close > level` (strict).
- Klaim "level tercakup dalam window N-bar" (EXP-007 §8) harus **dibuktikan
  deterministik** dari data (di mana swing-high berada relative terhadap
  window), bukan dinyatakan tanpa verifikasi.

## 4.3 Timing Knowability

- Event `PRICE_CONFIRMATION` knowable pada **close bar `i` sendiri**:
  `confirmable_at = timestamps[i]`, `confirmable_ref = i`.
- Tidak ada window konfirmasi tambahan untuk breakout itu sendiri.

## 4.4 Peran Trigger vs Konfirmasi

- Peran breakout (trigger atau konfirmasi) ditentukan oleh `SignalRule`
  per strategi (SPEC-003), bukan oleh detektor.
- Breakout berulang: setiap bar yang memenuhi §4.1 menghasilkan event
  tersendiri; deduplikasi/adopsi hanya terjadi pada level sinyal
  (`SignalRule.cooldown`, SPEC-003).

---

# 5. Edge Cases

| Kasus                                        | Perilaku deterministik        |
| -------------------------------------------- | ----------------------------- |
| Gap-up menembus level tanpa close di atasnya | Bukan breakout                |
| Close sama dengan level                      | Bukan breakout (tie)          |
| Breakout berulang dalam beberapa bar         | Satu event per bar            |
| Level di dalam window                        | Bergantung data; harus diverifikasi (§4.2) |
| Bar terakhir                                  | Knowable di close bar terakhir |

---

# 6. Non-Goals

- stop/limit order simulation (SPEC-003/SPEC-004);
- break trendline RSI (ADR-004);
- swing detection (SPEC-001).

---

# 7. Traceability

| Item                          | Code / Doc                          |
| ----------------------------- | ----------------------------------- |
| `detect_price_confirmation`   | `src/mre/detectors/price_confirmation.py` |
| Event model                   | `src/mre/models/event.py` (`PRICE_CONFIRMATION`) |
| Pemanggil                     | `src/mre/engines/event_engine.py` (lookback = `price_lookback`) |
| Komparasi swing-high          | `src/mre/detectors/swing.py` + signal definition strategi `swing_breakout`) |
| ADR-004 (trendline RSI)       | `docs/06-decisions/ADR-004_Trendline_Algorithm.md` |

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
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/06-decisions/ADR-004_Trendline_Algorithm.md`
- `src/mre/detectors/price_confirmation.py`

---

# 10. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-11 | Initial Breakout Detection spec  |

---

**Document Status:** Draft

**Document ID:** SPEC-002

**Version:** 1.0.0

**End of Document**