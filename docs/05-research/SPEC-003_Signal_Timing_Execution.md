---
title: Signal Timing & Execution
document_id: SPEC-003
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
  - ENG-003
  - ENG-005

referenced_by:
  - EXP-001
  - EXP-002
  - EXP-003
  - EXP-004
  - EXP-005
  - EXP-006
  - EXP-007
  - EXP-008

purpose: Bind when each piece of information is knowable and when execution occurs; eliminate lookahead (audit E-1/E-10)
---

# SPEC-003 — Signal Timing & Execution

> Measure the Market. Discover the Edge.

---

# 1. Purpose

SPEC-003 mengikat **kapan informasi dapat diketahui** dan **kapan
eksekusi terjadi**, sehingga sinyal bebas lookahead dan entry/exit
deterministik.

Dokumen ini menutup temuan audit E-1/E-10: swing backdating (event
di-stamp sebelum knowable), kontradiksi "entry pada candle breakout"
vs "next bar open", dan exit "open bar ke-hold_bars" vs "close".

---

# 2. Scope

Scope SPEC-003:

- kombinasi Event → Signal (`SignalRule`, window, cooldown);
- timestamp sinyal = saat seluruh konstituen knowable;
- entry (bar + harga fill);
- position lifecycle (satu Signal → satu Trade; konkuransi tidak dimodelkan);
- exit timing (SL/TP di SPEC-004; hold-exit close).

Di luar scope SPEC-003:

- formula SL/TP, gap, same-bar collision (SPEC-004);
- cost model (SPEC-005);
- deteksi swing/breakout (SPEC-001/SPEC-002).

---

# 3. Inputs

| Input               | Deskripsi                                        |
| ------------------- | ------------------------------------------------ |
| `events`            | Timeline Event terurut (dengan `confirmable_at`/`confirmable_ref`) |
| `signal_definition` | `SignalRule` dari plugin strategi (trigger, confirmations, window, cooldown, trigger_payload) |
| `candles`           | Seri candle OHLC                                 |
| `ExecutionConfig`   | hold_bars, position_size, slippage, SL/TP        |

---

# 4. Deterministic Rules

## 4.1 Knowability (E-1)

- Setiap Event membawa **waktu fakta** (`timestamp`) dan **waktu
  dapat-diketahui** (`confirmable_at`/`confirmable_ref` jika detektor
  membawanya; selain itu fallback ke fakta).
- Signal **tidak boleh dieksekusi** sebelum seluruh konstituennya
  knowable.

## 4.2 Kombinasi Event → Signal

Per `SignalRule`:

- trigger = Event pertama; harus diikuti oleh **event konfirmasi paling
  awal** dari setiap tipe yang diminta, dalam `window` candle reference
  (`_ref(confirmation) − _ref(trigger) ∈ (0, window]`).
- `trigger_payload` harus memenuhi filter payload deklaratif (mis.
  `{"slope__lt": 0.0}`).
- `signal_ref` = `max(_knowable_ref(e))` atas seluruh konstituen;
  `timestamp` = waktu knowable terkorespondensi.

## 4.3 Deduplikasi (Cooldown)

- `cooldown = 0`: legacy behavior — setiap trigger+konfirmasi yang valid
  menghasilkan Signal sendiri (overlap/duplikat dimungkinkan).
- `cooldown > 0`: Signal berikutnya dari rule yang sama ditekan bila
  `signal_ref < last_signal_ref + cooldown` (satu keputusan per episode).

## 4.4 Entry

- `entry_bar = max(signal_bar + 1, max_confirmable_ref + 1)` — bar open
  setelah signal **knowable**, bukan sekadar setelah timestamp fakta.
- Tidak ada bar setelahnya → Signal **tidak dieksekusi**.
- **Fill = open bar `entry_bar`** (market order) + slippage (SPEC-005).
- "Entry pada candle breakout" merujuk **candle keputusan** (bar sinyal),
  bukan fill (E-10).

## 4.5 Position Lifecycle

- Setiap Signal menghasilkan **satu Trade independen**.
- **Konkuransi tidak dimodelkan** pada engine saat ini: tidak ada guard
  overlap/position-bertabrakan, tidak ada pyramiding, tidak ada
  position-state machine — setiap sinyal dieksekusi apa adanya.
- Aturan ini **eksplisit**: bila eksperimen memerlukan guard konkuransi,
  konfigurasikan / spesifikasikan sebelum pre-registrasi (RSH-002 §9).

## 4.6 Exit Timing

- Exit oleh SL/TP (SPEC-004) atau **hold-exit di close bar
  `entry_bar + hold_bars`** (E-10).
- Data habis sebelum exit → exit di close bar terakhir.

---

# 5. Edge Cases

| Kasus                                        | Perilaku deterministik             |
| -------------------------------------------- | ---------------------------------- |
| Sinyal di candle terakhir                     | Tidak dieksekusi                   |
| Duplikat Signal pada timestamp sama           | Masing-masing dieksekusi (tanpa cooldown) |
| Sinyal overlapping / posisi bertabrakan       | Tidak ada guard — semua dieksekusi (§4.5) |
| Sinyal berlawanan saat posisi terbuka          | Tidak ada reversal logic — signal tetap dieksekusi |

---

# 6. Non-Goals

- intrabar fills / partial fills;
- pending orders (stop/limit) sebagai entry;
- trailing stop;
- position concurrency management (di luar engine saat ini).

---

# 7. Traceability

| Item                       | Code / Doc                                   |
| -------------------------- | -------------------------------------------- |
| `combine`                  | `src/mre/engines/signal_engine.py`           |
| `simulate`                 | `src/mre/engines/simulation_engine.py`       |
| `SignalRule` (window/cooldown) | `src/mre/models/signal_rule.py`           |
| Event knowability          | `src/mre/models/event.py`                    |
| `signal_window` (frozen di YAML, E-4) | `configs/EXP-*.yaml` + `experiment_runner.py` |

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
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `src/mre/engines/signal_engine.py`
- `src/mre/engines/simulation_engine.py`

---

# 10. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-11 | Initial Signal Timing & Execution spec (E-1/E-4/E-10) |

---

**Document Status:** Draft

**Document ID:** SPEC-003

**Version:** 1.0.0

**End of Document**