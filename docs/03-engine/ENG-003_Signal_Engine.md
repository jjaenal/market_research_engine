---
title: Signal Engine
document_id: ENG-003
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

| Atribut          | Tipe              | Deskripsi                        |
| ---------------- | ----------------- | -------------------------------- |
| `signal_type`    | string            | LONG / SHORT                     |
| `trigger`        | string            | event_type pembuka               |
| `confirmations`  | tuple[string]     | event_type konfirmasi (unique)   |
| `window`         | int               | max jarak reference (candle)     |
| `source_strategy`| string            | plugin strategy asal             |

Konstraint:

- `window >= 1`;
- `confirmations` tidak kosong dan tidak duplikat (anti-ambigu).

---

# 8. Combination Semantics

`combine(events, signal_definition) → Signal list`

Per rule:

1. urutkan trigger events;
2. untuk tiap trigger, cari konfirmasi terawal tiap tipe
   dalam window: `confirmation.reference - trigger.reference <= window`;
3. bila semua konfirmasi ada → emit Signal di timestamp
   terakhir (konfirmasi valid, FND-009 §13.5);
4. bila trigger tidak memenuhi → tanpa Signal (NO SIGNAL).

Determinisme (Article 7): konfirmasi terawal dipilih.

---

# 9. Failure Conditions

Per PRD-003 §7.5:

- definisi Signal kosong → ValueError;
- kombinasi ambigu (duplikat konfirmasi) → ValueError.

---

# 10. Initial Signal Definition (MVP)

Experiment pertama (RSI Trendline Breakout):

```text
RSI_TRENDLINE_BROKEN (trigger)
+
PRICE_CONFIRMATION (confirmation)
=
LONG
```

window dikonfigurasi pada experiment config (FR-012).

---

# 11. Testing (DEV-002)

- unit test Signal model (fields, immutable);
- unit test SignalRule (validasi);
- unit test combine (window, determinism, failure conditions).

---

# 12. Traceability

| Item          | Requirement / Feature     |
| ------------- | ------------------------- |
| Signal model  | ARC-002 §7.6, Article 4, 5 |
| combine       | ARC-006 §7.4, FEAT-005, FR-005 |
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
| 1.0.0   | 2026-08-08 | Initial signal engine spec       |

---

**Document Status:** Draft

**Document ID:** ENG-003

**Version:** 1.0.0

**End of Document**
