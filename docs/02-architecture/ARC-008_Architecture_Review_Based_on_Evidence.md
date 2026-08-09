---
title: Architecture Review Based on Evidence
document_id: ARC-008
version: 1.0.8
status: Result
category: Architecture
owner: Market Research Engine Core Team
created: 2026-08-09
last_updated: 2026-08-09

depends_on:
  - FND-001
  - FND-006
  - FND-007
  - FND-008
  - ARC-005
  - ARC-006
  - ARC-007
  - ADR-001
  - ADR-002
  - PRD-003
  - EXP-001

referenced_by:
  - FND-006
  - FND-008

purpose: Record the M7 evidence-based architecture review (TODO-028) — what the real EXP-001 experiment revealed about the architecture, and the resulting improvement direction for iteration
---

# Architecture Review Based on Evidence

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ARC-008 adalah **review arsitektur berdasarkan evidence** (TODO-028,
FND-008 §43) — evaluasi arsitektur MRE dari pengalaman experiment nyata,
bukan dari penelaahan dokumen.

Dokumen ini menjawab lima pertanyaan review
(FND-008 §43 Objective):

- What was difficult?
- What abstraction failed?
- What data was missing?
- What should be simplified?
- What should be generalized?

Review menilai arsitektur terhadap evidence yang teramati selama
M5 (baseline, EXP-001 §15) dan M6 (sensitivity §16, out-of-sample §17,
robustness §18, conclusion §19).

---

# 2. Review Principle

```text
ARCHITECTURE SIZED TO EVIDENCE
arsitektur dinilai dari apa yang berjalan,
bukan dari apa yang ditulis
```

Evidence bersumber dari:

- hasil experiment nyata (EXP-001 §15–§19);
- perilaku kode yang teramati (module `src/mre/`);
- abstraksi yang dibutuhkan namun tidak ada saat experiment dijalankan.

---

# 3. Evidence Sources

| Source                | Evidence                                                  |
| --------------------- | --------------------------------------------------------- |
| EXP-001 §15 (baseline)| 1403 trades, determinisme dua run identik (FR-010)        |
| EXP-001 §16 (sensitivity) | grid 6×3 reusable lewat frozen config + `replace()`   |
| EXP-001 §17 (OOS)     | segment train/test dibuat dari candle slice               |
| EXP-001 §18 (robustness) | 4 periode + 1 market + 7 cost grid + 5 combos          |
| EXP-001 §19 (conclusion) | verdict PARTIALLY SUPPORTED pada biaya nol/near-zero   |
| `src/mre/`            | struktur package teramati saat iterasi                    |

---

# 4. Review Result

## Final Status

```text
M7 ARCHITECTURE REVIEW: EVIDENCE-BASED
```

## Overall Assessment

```text
CORE HOLDS, PERIPHERY DRIFTS
```

Arsitektur inti (pipeline `compute_report()`, frozen config, pure
functions, deterministic) **terbukti menahan beban experiment** dan
harus dipertahankan. Namun tiga hal yang dijanjikan arsitektur
**belum terwujud di kode** (strategi sebagai plugin, config YAML,
deduplikasi signal), dan data terbatas pada satu timeframe + dua market.

Tidak ada critical blocker terhadap iterasi M7.

---

# 5. What Was Difficult

## 5.1 Signal Overlap (Trade Duplikat)

EXP-001 §15.3 Observasi:

```text
banyak Trade duplikat/identik (trigger RSI_TRENDLINE_BROKEN berdekatan
memakai konfirmasi yang sama) — artefak semantik combine() (ENG-003 §8),
bukan keputusan strategy. Didokumentasikan untuk iterasi
(kemungkinan deduplikasi Signal pada M6/M7).
```

`combine()` (`src/mre/engines/signal_engine.py:12`) menghasilkan satu
Signal per trigger Event yang valid; trigger berdekatan yang memakai
konfirmasi yang sama menghasilkan Signal yang hampir identik. Ini
menggelembungkan trade count (1403) dan mendistorsi metrik agregat.

- **Difficulty:** jumlah trade tidak merepresentasikan keputusan unik;
  metrik expectancy/PF tercemar duplikat.
- **Akar:** signal definition tidak mendefinisikan "kapan signal baru
  valid" (cooldown/deduplikasi).
- **Arah:** deduplikasi Signal pada iterasi (EXP-001 §15.3).

## 5.2 Konfigurasi di-hardcode di CLI

Parameter strategi (rsi_period, swing_left, price_lookback, hold_bars,
dll.) di-hardcode di `_exp001_signal_definition()` dan CLI `main()`
(`src/mre/core/experiment_runner.py:130,158`). Sensitivity/OOS/
Robustness masing-masing menyalin `_exp001_config()`.

- **Difficulty:** mengubah satu nilai berarti mengedit kode + menjalankan
  ulang; tidak ada satu source of truth untuk konfigurasi experiment.
- **Arah:** Article 12 (config over hardcode) belum terpenuhi penuh —
  konfigurasi adalah frozen dataclass, bukan file external.

## 5.3 Segment Split Kehilangan Warm-up

OOS dan robustness membuat segment CSV dari `candle.slice` lalu menjalankan
`compute_report()` pada tiap segment (`out_of_sample.py:54`, `robustness.py:92`).
Karena `rsi()` mengembalikan NaN pada `period` posisi pertama
(`src/mre/indicators/rsi.py:13,19`), **awal tiap segment kehilangan
events** — jumlah signal per segment tidak sebanding dengan panjangnya.

- **Difficulty:** perbandingan antar-slice (period 1..4) sedikit bias oleh
  warm-up yang hilang di batas segment; trade count slice tidak proporsional.
- **Catatan:** ini artifact methodology, bukan data; tidak membatalkan
  kesimpulan (semua slice kena perlakuan sama), namun membatasi
  interpretasi kuantitatif.

---

# 6. What Abstraction Failed

## 6.1 Strategi Bukan Plugin

ARC-005 §6 dan ARC-006 mendefinisikan:

```text
| Strategy | strategies/ | timeline Event | Signal |
├── strategies/    # strategi sebagai plugin (STRATEGY)
```

**Tidak ada package `strategies/` di `src/mre/`.** Satu-satunya strategi
adalah `_exp001_signal_definition()` yang di-hardcode di
`src/mre/core/experiment_runner.py:130` — justru embed di orchestrator,
melanggar ARC-005 §7 ("Strategy implementation must not be embedded in
engine") dan spirit Article 11 (Plugin First).

- **Failed:** janji plugin strategy (ARC-005, ADR-002) belum diwujudkan;
  experiment hanya bisa berisi strategi yang ditulis di dalam core.
- **Konsekuensi:** EXP-001 hanya mampu menguji satu definisi signal;
  ekspansi strategi (TODO-029) akan terkendala.

> **Resolved by ARC-ACT-010:** `src/mre/strategies/` — registry
> (`register`/`get`) + `exp001.py`. `ExperimentConfig.strategy_id`
> me-resolve `signal_definition` dari registry; strategi baru cukup
> mendaftar, tanpa mengubah engine.

## 6.2 Config "Over Hardcode" (YAML) Belum Ada

Article 12 / FR-012 menjanjikan config-driven execution (ARC-005 §10).
Realisasi: frozen `ExperimentConfig` dataclass + hardcode di CLI.
AGENTS.md mencatat "The docs' 'config over hardcode (YAML)' is
aspirational, not implemented."

- **Failed:** parameter tetap hidup di kode; reproducibility terikat pada
  commit, bukan pada berkas config yang versi-able.

> **Resolved by ARC-ACT-011:** `configs/EXP-001.yaml` + loader
> (`load_experiment_config()`); parameter frozen versi-able di berkas,
> reproducibility berbasis berkas (FR-012).

## 6.3 Deduplikasi Signal Tidak Didefinisikan

Semantik `combine()` (ENG-003 §8) menghasilkan signal overlap (§5.1).
Abstraksi ini berfungsi benar secara mekanik, namun **semantik "signal
tunggal" yang dibutuhkan experiment tidak didefinisikan** — sehingga
duplikat menembus sampai ke simulation.

---

# 7. What Data Was Missing

| Data                          | Dampak                                               |
| ----------------------------- | ---------------------------------------------------- |
| Timeframe selain H1           | robustness tidak menguji dimensi timeframe (EXP-001 §18.5) |
| Market ketiga+                | hanya XAUUSD + XAGUSD; cross-market tidak menggeneralisasi  |
| Biaya eksekusi nyata venue    | cost grid diasumsikan, bukan dari broker/venue nyata (EXP-001 §18.3) |
| Label regime/condition market | period-3 negatif mengindikasikan ketergantungan regime, tak ada data untuk menguji (FND-006 §17 expected RQ) |

Keterbatasan data ini adalah batasan **lingkup dataset**, bukan kelemahan
arsitektur. Namun arsitektur saat ini tidak memiliki slot data
"market condition" — sehingga RQ regime dependency (FND-006 §17) belum
bisa dijawab.

---

# 8. What Should Be Simplified

- **Renderer:** ada empat perender markdown terpisah — `render`
  (`reporting_engine`), `sensitivity.to_markdown`, `out_of_sample.to_markdown`,
  `robustness.to_markdown`. Semua pure string, struktur hampir sama.
  Satu helper tabel/heading bersama cukup.
- **Config builder:** `_exp001_config()` disalin di `sensitivity.py`,
  `out_of_sample.py`, dan `robustness.py`. Pindah ke satu tempat
  (mis. `experiment_runner` atau module config baru) mengurangi duplikasi.
- **CLI:** tiga CLI terpisah (`sensitivity.py`, `out_of_sample.py`,
  `robustness.py`) dengan pola argparse identik. Bisa dipersatukan dalam
  satu CLI `experiment` dengan subcommand.

> **Resolved by ARC-ACT-014:** helper `mre/utils/markdown.py`
> (`heading`/`table`) dipakai `report`, `sensitivity`, `out_of_sample`,
> dan `robustness`; `exp001_config()` satu tempat di
> `experiment_runner.py`; `src/mre/cli.py` satu entrypoint dengan
> subcommand `baseline|sensitivity|oos|robustness`, module `main()`
> menjadi delegasi tipis ke CLI.

---

# 9. What Should Be Generalized

- **Strategi → plugin**: ekstrak `_exp001_signal_definition()` ke package
  `strategies/` per ARC-005 §6, dengan registry/registrasi sehingga
  `ExperimentConfig` menerima strategi terdaftar, bukan fungsi internal.
  > **Resolved by ARC-ACT-010** (`strategies/registry.py` + `exp001.py`).
- **Config eksternal**: konfigurasi experiment (frozen params) dipindah ke
  berkas config (YAML per Article 12 / FR-012) yang dibaca CLI —
  reproducibility berbasis berkas, bukan hardcode commit.
  > **Resolved by ARC-ACT-011** (`configs/EXP-001.yaml` + loader).
- **Deduplikasi signal**: definisikan semantik "satu signal per episode
  trigger+confirmation" (cooldown) sebagai opsi di `SignalRule`, sehingga
  experiment baru mendapat trade count yang merepresentasikan keputusan
  unik.
- **Segment runner**: abstraksi "run config pada rentang candle" yang dipakai
  OOS (train/test) dan robustness (period slices) dijadikan satu util
  bersama (mis. `run_on_slice`), menghilangkan duplikasi
  `write_candle_csv` + `compute_report` di dua module.

---

# 10. What Worked (Dipertahankan)

| Kekuatan                       | Evidence                                            |
| ------------------------------ | --------------------------------------------------- |
| Pipeline `compute_report()`    | dipakai ulang oleh sensitivity/OOS/robustness tanpa modifikasi |
| Frozen config + `replace()`    | grid param/cost dijalankan lewat variasi immutabel (sensitivity.py:47, robustness.py:137) |
| Pure deterministic functions   | dua run berbeda menghasilkan metrik identik (EXP-001 §15, FR-010) |
| `write_candle_csv` dipakai bersama | OOS train/test + robustness period slices reuse satu util |
| Renderer pure string            | laporan ditulis hanya di CLI entrypoint (no side-effect di business logic) |
| Satu normalized dataset reusable | sensitivity/OOS/robustness berbagi satu file normalized (Article 13) |

Pola ini **harus dipertahankan** pada iterasi M7.

---

# 11. Recommended Actions

## ARC-ACT-010 — Extract Strategy Plugin Package

Ekstrak `_exp001_signal_definition()` dari `experiment_runner.py` ke
package `strategies/` dengan registry sederhana (ARC-005 §6). Perlu ADR
untuk mekanisme registrasi bila mempengaruhi interface engine.

**Status: DONE** (`src/mre/strategies/` — `registry.py` + `exp001.py`).
`ExperimentConfig.strategy_id` me-resolve `signal_definition` dari
registry; `combine(events, signal_definition)` tetap tidak berubah —
plugin hanya menyuplai konfigurasi (Article 12). **ADR tidak diperlukan**
karena mekanisme registrasi tidak mengubah interface engine.

## ARC-ACT-011 — Move Experiment Config to External File

Pindahkan parameter frozen dari hardcode CLI ke berkas config (YAML,
Article 12 / FR-012); CLI membaca berkas dan menghasilkan
`ExperimentConfig`. Reproducibility berbasis berkas.

**Status: DONE** (`configs/EXP-001.yaml` + `load_experiment_config()`).
Frozen params hidup di berkas YAML yang dikomit (single source of
truth, RSH-002 §9); CLI hanya menimpa path dataset/report saat run.
`exp001_config()` adalah wrapper tipis di atas loader.

## ARC-ACT-012 — Define Signal Deduplication Semantics

Tambah opsi cooldown/deduplikasi pada `SignalRule` dan `combine()` untuk
mengatasi signal overlap (EXP-001 §15.3); re-run EXP-001 setelahnya.

**Status: DONE** (SignalRule.cooldown, ENG-003 §8.1). Re-run EXP-001
dengan cooldown > 0 didelegasikan ke iterasi berikutnya; baseline tetap
frozen (cooldown 0).

## ARC-ACT-013 — Unify Segment Runner

Buat util bersama untuk "run frozen config pada rentang candle" dan
pakai di OOS + robustness; hapus duplikasi `write_candle_csv` +
`compute_report`.

**Status: DONE** (`src/mre/core/segments.py` — `run_on_slice()`,
`SegmentRun`, `ensure_normalized()`). OOS train/test dan robustness
period slices kini berbagi satu implementasi slice→CSV→compute.

## ARC-ACT-014 — Unify Renderers & Config Builder

Satu helper markdown tabel/heading bersama; `_exp001_config()` satu
tempat; CLI eksperimen satu entrypoint dengan subcommand.

**Status: DONE** (`src/mre/utils/markdown.py` — `heading()`/`table()`;
`src/mre/core/experiment_runner.py` — `exp001_config()`; `src/mre/cli.py`
— satu entrypoint dengan subcommand `baseline|sensitivity|oos|robustness`,
module `main()` delegasi ke CLI). Baseline config & renderer dipakai
seragam di semua eksperimen.

---

# 12. Non-Blocking Issues

- **NBI-010:** data terbatas H1 + 2 market; ekspansi data adalah TODO-030
  (Market Expansion, DEFERRED), tidak menghalangi iterasi.
- **NBI-011:** ENG-004 Probability Engine tetap tanpa doc/impl — cakupan
  probability ditangani statistics engine (FND-006), tidak memblokir.
- **NBI-012:** bias warm-up pada segment split (§5.3) tidak membatalkan
  kesimpulan, namun dicatat sebagai keterbatasan metodologi.

---

# 13. Critical Blocker Assessment

```text
Critical blockers: 0
```

Tidak ada blocker yang menghalangi iterasi M7.

---

# 14. M7 Direction — Next Research Question

Per FND-007 §38, iterasi selesai ketika pertanyaan penelitian berikutnya
terdefinisi jelas. Dari conclusion EXP-001 §19 (edge hanya pada biaya
nol/near-zero) dan evidence di atas:

```text
NEXT RESEARCH QUESTION (draft)
Apakah edge RSI trendline breakout tetap positif setelah biaya eksekusi
realistis, apabila signal di-deduplikasi (satu keputusan per episode)
dan dieksekusi pada regime market yang terseleksi?
```

Pertanyaan ini menuntun iterasi: ARC-ACT-012 (deduplikasi) dulu, lalu
eksperimen ulang pada biaya realistis (EXP-001 §18.3) dengan regime
selection.

## 14.1 Jawaban — Re-run (M7 Iteration)

Re-run dieksekusi lewat pipeline yang sama (`compute_report()` +
`combine()` + `simulate()`), dengan:

- **deduplikasi:** `SignalRule.cooldown` (ENG-003 §8.1) — satu keputusan
  per episode;
- **regime selection:** ATR volatility regime (`src/mre/indicators/regime.py`)
  — label "high"/"low" dari perbandingan ATR short (14) vs ATR long (100);
- **cost grid:** biaya eksekusi realistis per sisi (commission/slippage,
  0.02%–0.05%, RSH-003 §10).

Expectancy per skenario (n = jumlah signal setelah filter):

| Skenario        | n   | 0.0      | 0.02%    | 0.05%    |
| --------------- | --- | -------- | -------- | -------- |
| cooldown 0, all | 1403 | 0.8683 | 0.1539 | −0.9176 |
| cooldown 0, high| 698  | 1.2506 | 0.5269 | −0.5587 |
| cooldown 0, low | 704  | 0.5068 | −0.1988| −1.2571 |
| cooldown 10, all| 1095 | 0.8781 | 0.1679 | −0.8974 |
| cooldown 10, high| 532 | 1.2276 | 0.5097 | −0.5672 |
| cooldown 10, low | 562 | 0.5692 | −0.1343| −1.1894 |
| cooldown 20, all| 992  | 0.7203 | 0.0115 | −1.0516 |
| cooldown 20, high| 480 | 0.8262 | 0.1158 | −0.9498 |
| cooldown 20, low | 511 | 0.6447 | −0.0631| −1.1249 |

**Jawaban: TIDAK.** Edge tidak tetap positif setelah biaya eksekusi
realistis, bahkan dengan deduplikasi + regime selection sekaligus:

- deduplikasi (cooldown > 0) mengurangi trade count (signal overlap,
  §5.1) namun **tidak memulihkan edge** pada biaya realistis;
- regime "high" adalah yang paling tahan biaya (expectancy terbaik di
  tiap tingkat cost), tetapi masih negatif pada 0.05%/sisi (−0.56 s/d
  −0.95);
- biaya 0.05% per sisi menghilangkan edge di **semua** kombinasi
  cooldown × regime.

Kesimpulan research question ini dicatat lebih lengkap di EXP-001 §19.6.
Slang waktu ini juga menutup data gap "label regime/condition market"
(§7): arsitektur kini memiliki slot `regime_config` + indicator regime,
sehingga RQ regime dependency (FND-006 §17) dapat dijawab.

## 14.2 Next Research Question — Risk Management (SL/TP)

RQ-006 dijawab **TIDAK**: deduplikasi + regime selection tidak memulihkan
edge pada biaya realistis (EXP-001 §19.6). Arah mitigasi biaya berikutnya
yang dipilih: **risk management SL/TP**.

```text
NEXT RESEARCH QUESTION (RQ-007, pre-registered — RSH-001 §7.2)
Apakah menambahkan stop-loss/take-profit berbasis ATR-multiple pada
EXP-001 memulihkan expectancy positif pada biaya eksekusi realistis?
```

Pre-registration (per RSH-001 §7.2, dinyatakan sebelum experiment):

- **Hipotesis:** SL/TP ATR-multiple (exit dini membatasi loss dan mengunci
  profit) meningkatkan expectancy pada biaya realistis dibanding baseline
  tanpa SL/TP.
- **Independent variables:** `stop_loss_atr` (SL = entry ∓ N×ATR) dan
  `take_profit_atr` (TP = entry ± N×ATR), N ∈ grid yang pre-defined;
  biaya eksekusi per sisi (0–0.05%, RSH-003 §10).
- **Control variables:** dataset, signal definition, deduplikasi (cooldown),
  regime selection tetap seperti konfigurasi frozen.
- **Metrik:** expectancy, win rate, PF pada tiap level biaya; dibanding
  terhadap baseline tanpa SL/TP (control).
- **Kriteria:** edge "bertahan" bila expectancy > 0 pada biaya realistis
  (0.02%/0.05%) dengan n ≥ min_sample.

Hasil dicatat di EXP-001 §19.7.

## 14.3 Jawaban — RQ-007 (Risk Management SL/TP)

Re-run dieksekusi lewat pipeline yang sama dengan `stop_loss_atr` /
`take_profit_atr` (SL/TP dihitung dari ATR di entry bar, no lookahead;
`src/mre/models/execution.py` + `src/mre/engines/simulation_engine.py`).

Expectancy (n = 1403 signal, cooldown 0, tanpa regime filter):

| SL/TP (ATR)    | 0.0      | 0.02%    | 0.05%    |
| --------------- | -------- | -------- | -------- |
| none (baseline) | 0.8683   | 0.1539   | −0.9176  |
| SL 1.0          | 1.0165   | 0.3021   | −0.7696  |
| SL 1.0 / TP 4.0 | 1.0534   | 0.3390   | −0.7326  |
| SL 2.0 / TP 4.0 | 0.8974   | 0.1830   | −0.8886  |

Breakeven cost (titik expectancy menyeberang nol):

| Skenario        | Breakeven/sisi |
| --------------- | -------------- |
| all, no SL/TP   | 26 bps         |
| all, SL 1.0/TP 4.0 | 30 bps      |
| high, no SL/TP  | 36 bps         |
| high, SL 1.0/TP 4.0 | 42 bps     |

Kombinasi terkuat (cooldown 10, regime high, SL 1.0/TP 4.0) tetap
negatif pada 0.05%/sisi (−0.51).

**Jawaban: TIDAK.** SL/TP ATR-multiple **memperbaiki** tolerance biaya
(breakeven naik ~4–6 bps/sisi dan expectancy pada 0.02% membaik),
namun **tidak memulihkan edge** pada 0.05%/sisi — kriteria pre-registration
(expectancy > 0 pada 0.05%) tidak terpenuhi di semua kombinasi. Konklusi
baseline EXP-001 §19 diperkuat lagi.

---

# 15. Approval

Berdasarkan review pada dokumen ini:

```text
╔══════════════════════════════════════╗
║      ARCHITECTURE REVIEW             ║
╠══════════════════════════════════════╣
║ Basis         : EVIDENCE (EXP-001)   ║
║ Blockers      : 0                    ║
║ Actions       : 5                    ║
║ Core verdict  : HOLDS                ║
╠══════════════════════════════════════╣
║ M7 — ITERATION                       ║
║                                      ║
║ READY FOR NEXT RESEARCH QUESTION     ║
╚══════════════════════════════════════╝
```

---

# 16. References

- `docs/00-foundation/FND-006_Project_Status.md`
- `docs/00-foundation/FND-007_Roadmap.md`
- `docs/00-foundation/FND-008_TODO.md`
- `docs/02-architecture/ARC-005_Plugin_Architecture.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/06-decisions/ADR-001_Adopt_Event_Driven_Architecture.md`
- `docs/06-decisions/ADR-002_Adopt_Plugin_Based_Architecture.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/07-experiments/EXP-001_RSI_Trendline_Breakout_Baseline.md`

---

# 17. Revision History

| Version | Date       | Changes                                    |
| ------- | ---------- | ------------------------------------------ |
| 1.0.8   | 2026-08-09 | RQ-007 answered (§14.3): SL/TP ATR-multiple raises breakeven cost but does not restore edge at 0.05%/side |
| 1.0.7   | 2026-08-09 | RQ-007 pre-registered (§14.2): risk management SL/TP ATR-multiple |
| 1.0.6   | 2026-08-09 | M7 re-run recorded (§14.1): cooldown + ATR regime + cost grid; RQ answered TIDAK; regime slot added (indicators/regime.py, regime_config) |
| 1.0.5   | 2026-08-09 | ARC-ACT-011 marked DONE (configs/EXP-001.yaml + loader) |
| 1.0.4   | 2026-08-09 | ARC-ACT-010 marked DONE (strategies/ package + registry) |
| 1.0.3   | 2026-08-09 | ARC-ACT-014 marked DONE (markdown utils, exp001_config, mre.cli) |
| 1.0.2   | 2026-08-09 | ARC-ACT-013 marked DONE (core/segments.py) |
| 1.0.1   | 2026-08-09 | ARC-ACT-012 marked DONE (ENG-003 §8.1)     |
| 1.0.0   | 2026-08-09 | Initial evidence-based architecture review (TODO-028) |

---

**Document Status:** Result

**Document ID:** ARC-008

**Version:** 1.0.8

**End of Document**
