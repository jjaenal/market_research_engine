---
title: Signal Engine
document_id: ENG-003
version: 1.2.0
status: Draft
category: Engine
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-09

depends_on:
  - FND-001
  - FND-005
  - FND-009
  - ARC-002
  - ARC-003
  - ARC-005
  - ARC-006
  - PRD-003
  - PRD-004
  - PRD-007
  - DEV-002
  - ENG-002

referenced_by:
  - FND-006
  - FND-008
  - ENG-004

purpose: Define the Signal Engine implementation spec — Signal model and event combination (TODO-018, FEAT-005)
---

# Signal Engine

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ENG-003 mendefinisikan **Signal Engine** — spesifikasi implementasi
untuk TODO-018 (Build Signal Engine) dan FEAT-005 (Signal Generator).

Dokumen ini menurunkan model Signal (ARC-002 §7.6)
dan kontrak strategy plugin (ARC-005 §9).

---

# 2. Scope

Scope ENG-003:

- model Signal;
- definisi Signal (SignalRule);
- kombinasi Event → Signal (`combine`).

Di luar scope ENG-003:

- simulasi Trade (ENG-005);
- statistik (ENG-006);
- probability (ENG-004).

---

# 3. Audience

- tim MRE;
- software engineer;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per ARC-006 §7.4:

```text
SignalEngine: combine(events, signal_definition) → Signal list
```

Per PRD-003 §7.5:

- input: timeline Event;
- processing: mengombinasikan Event menjadi Signal sesuai definisi Signal;
- failure conditions: definisi Signal tidak ada; kombinasi Event ambigu.

Per Article 4: Signal adalah agregasi evidence.
Per Article 5: setiap Signal menyimpan daftar Event penyusunnya.
Per Rule 003: Signal ≠ Trade.

---

# 5. Definitions

Terminologi mengikuti **FND-009**.

| Term          | Definition                                   |
| ------------- | -------------------------------------------- |
| Signal        | Output strategy yang menunjukkan kondisi terpenuhi (FND-009 §13.1) |
| SignalRule    | Definisi deterministik kombinasi Event       |
| Trigger       | Event pembuka urutan                         |
| Confirmation  | Event konfirmasi dalam window                |
| Signal Timestamp | Timestamp saat Signal dianggap valid (FND-009 §13.5) |

---

# 6. Signal Model

Per ARC-002 §7.6:

| Atribut        | Tipe       | Deskripsi                       |
| -------------- | ---------- | ------------------------------- |
| `signal_type`  | string     | LONG / SHORT / NO SIGNAL        |
| `timestamp`    | datetime   | Signal valid (FND-009 §13.5)    |
| `events`       | tuple      | Event penyusun (Article 5)      |
| `confirmation` | bool       | Konfirmasi terpenuhi            |

Atribut tambahan (traceability):

| Atribut         | Tipe   | Deskripsi                  |
| --------------- | ------ | -------------------------- |
| `source_strategy` | string | Strategy asal (plugin id)  |
| `experiment_id` | string | Eksperimen asal            |

Signal immutable (Article 13), deterministic (Article 7).

---

# 7. Signal Definition (SignalRule)

```text
Event A (trigger)
+
Event B (confirmation)
+
Filter C (opsional, iterasi berikutnya)
=
LONG
```

| Atribut            | Tipe              | Deskripsi                        |
| ------------------ | ----------------- | -------------------------------- |
| `signal_type`      | string            | LONG / SHORT                     |
| `trigger`          | string            | event_type pembuka               |
| `confirmations`    | tuple[string]     | event_type konfirmasi (unique)   |
| `window`           | int               | max jarak reference (candle)     |
| `source_strategy`  | string            | plugin strategy asal             |
| `trigger_payload`  | dict              | filter payload trigger (opsional)|
| `cooldown`         | int               | dedup gap (candle), 0 = off      |

Konstraint:

- `window >= 1`;
- `confirmations` tidak kosong dan tidak duplikat (anti-ambigu);
- kunci `trigger_payload` harus string dengan operator dikenali:
  `eq`, `neq`, `lt`, `le`, `gt`, `ge` (sufiks `__<op>`), default `eq`;
- `cooldown >= 0`.

Filter payload memungkinkan pemilihan arah break di Signal Engine
(bukan di detector), konsisten dengan ENG-002 §8 — integrasi hanya
terjadi pada Signal Engine.

Contoh: down-trendline ditembus ke atas (bullish):

```text
trigger_payload: { "slope__lt": 0.0 }
```

---

# 8. Combination Semantics

`combine(events, signal_definition) → Signal list`

Per rule:

1. urutkan trigger events;
2. untuk tiap trigger, terapkan `trigger_payload` bila ada
   (trigger yang tidak lolos filter diabaikan);
3. untuk trigger lolos, cari konfirmasi terawal tiap tipe
   dalam window: `confirmation.reference - trigger.reference <= window`;
4. bila semua konfirmasi ada → emit Signal di timestamp
   terakhir (konfirmasi valid, FND-009 §13.5);
5. bila trigger tidak memenuhi → tanpa Signal (NO SIGNAL).

Determinisme (Article 7): konfirmasi terawal dipilih.

### 8.1 Deduplication (cooldown)

Per ARC-008 ARC-ACT-012 (signal overlap, EXP-001 §15.3):

- `cooldown = 0` (default): perilaku legacy — tiap trigger valid
  menghasilkan Signal;
- `cooldown > 0`: setelah Signal di-emit pada reference R (reference
  konfirmasi), trigger berikutnya yang akan menghasilkan Signal dengan
  reference < `R + cooldown` **disuppress** — satu keputusan per episode,
  bukan satu per trigger.

Semantik dedup diukur pada reference Signal (candle konfirmasi), bukan
reference trigger, sehingga trigger berdekatan yang memakai konfirmasi
yang sama digabung menjadi satu Signal (trade count merepresentasikan
keputusan unik, ARC-008 §9).

Dedup bersifat **per-rule**: tiap `SignalRule` melacak reference Signal
terakhir yang di-emit secara independen; aturan berbeda tidak saling
menekan.

---

# 9. Failure Conditions

Per PRD-003 §7.5:

- definisi Signal kosong → ValueError;
- kombinasi ambigu (duplikat konfirmasi) → ValueError.

---

# 10. Initial Signal Definition (MVP)

Experiment pertama (RSI Trendline Breakout) — LONG baseline:

```text
RSI_TRENDLINE_BROKEN (trigger, slope < 0 → down-trendline ditembus ke atas)
+
PRICE_CONFIRMATION (confirmation)
=
LONG
```

`window` dan `trigger_payload` dikonfigurasi pada
experiment config (FR-012).

SHORT (break bearish, slope > 0) membutuhkan price confirmation
arah bawah; belum ada detector-nya pada MVP (PRD-006 §8).

---

# 11. Testing (DEV-002)

- unit test Signal model (fields, immutable);
- unit test SignalRule (validasi, termasuk cooldown);
- unit test combine (window, determinism, failure conditions, dedup cooldown).

---

# 12. Traceability

| Item          | Requirement / Feature     |
| ------------- | ------------------------- |
| Signal model  | ARC-002 §7.6, Article 4, 5 |
| combine       | ARC-006 §7.4, FEAT-005, FR-005 |
| Dedup cooldown | ARC-008 ARC-ACT-012, EXP-001 §15.3 |
| Failure       | PRD-003 §7.5              |

---

# 13. Compliance

| Article | Signal Engine requirement   |
| ------- | --------------------------- |
| Article 4 | Signal = agregasi Event    |
| Article 5 | Signal menyimpan Event penyusun |
| Article 7 | Deterministic              |
| Article 13 | Signal immutable          |
| Rule 003 | Signal ≠ Trade              |

---

# 14. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-003_Event_Architecture.md`
- `docs/02-architecture/ARC-005_Plugin_Architecture.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-007_Feature_Specification.md`
- `docs/04-development/DEV-002_Testing_Strategy.md`
- `docs/03-engine/ENG-002_Event_Engine.md`

---

# 15. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.2.0   | 2026-08-09 | Add SignalRule cooldown dedup (ARC-008 ARC-ACT-012) |
| 1.1.0   | 2026-08-08 | Add SignalRule trigger_payload filter (direction selection in Signal Engine) |
| 1.0.0   | 2026-08-08 | Initial signal engine spec       |

---

**Document Status:** Draft

**Document ID:** ENG-003

**Version:** 1.2.0

**End of Document**
