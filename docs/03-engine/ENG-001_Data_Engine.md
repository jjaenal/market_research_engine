---
title: Data Engine
document_id: ENG-001
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
  - ARC-004
  - ARC-006
  - ARC-007
  - PRD-003
  - PRD-004
  - PRD-007
  - DEV-002
  - RSH-002

referenced_by:
  - FND-006
  - FND-008
  - ENG-002

purpose: Define the Data Engine implementation spec — CSV loading, schema detection, timestamp parsing, normalization, and validation (TODO-015, FEAT-001/002)
---

# Data Engine

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ENG-001 mendefinisikan **Data Engine** — spesifikasi implementasi
untuk TODO-015 (Build Data Engine) dan FEAT-001/002.

Dokumen ini menurunkan schema dan integrity rules (ARC-004)
menjadi spesifikasi engine yang dapat dibangun dan diuji (DEV-002).

---

# 2. Scope

Scope ENG-001:

- loading CSV (PRD-003 §7.1);
- deteksi schema;
- parsing dan normalisasi timestamp;
- validasi OHLC (PRD-003 §7.2, FR-002);
- penanganan missing data;
- Dataset metadata (ARC-004 §6.2).

Di luar scope ENG-001:

- persistensi teknis;
- indikator (ENG-016);
- engine lain (ENG-002..ENG-007).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Pipeline MRE dimulai dari data (PRD-003 §7.1, §7.2):

```text
CSV → Import → Validate → ...
```

Kontrak CSV dan integrity rules ditetapkan di ARC-004 §7 dan §8.

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term            | Definition                                |
| --------------- | ----------------------------------------- |
| Dataset         | Kumpulan candle + metadata (ARC-002)      |
| Candle          | Satu unit observasi market (ARC-004 §6.1) |
| Data Integrity  | Konsistensi dan kebenaran data (ARC-004)  |
| OHLCV           | Open, High, Low, Close, Volume            |

---

# 6. Interface

Per ARC-006 §7.1:

```text
load_dataset(source, config) → Dataset
validate(dataset) → ValidationResult
```

Kontrak:

- `load_dataset` membaca dan mem-parsing CSV;
- `validate` menerapkan integrity rules (ARC-004 §8);
- output `Dataset` immutable (Article 13).

---

# 7. Responsibilities (TODO-015)

| Responsibility       | Detail                                  |
| -------------------- | --------------------------------------- |
| Load CSV             | Baca file, deteksi kolom wajib          |
| Detect schema        | Verifikasi kolom: timestamp, open, high, low, close, volume |
| Parse timestamp      | ISO 8601 dengan timezone eksplisit      |
| Normalize data       | Konversi angka (float), normalisasi timestamp |
| Validate OHLC        | Integrity rules (ARC-004 §8)            |
| Handle missing data  | Deteksi nilai kosong, tandai/ditolak    |
| Reject invalid data  | Dataset ditolak dengan penyebab eksplisit |

---

# 8. Failure Conditions

Per ARC-004 §7 dan PRD-003 §7.1/§7.2:

| Failure                    | Konsekuensi        |
| -------------------------- | ------------------ |
| File tidak ditemukan       | Ditolak            |
| Kolom wajib hilang         | Ditolak            |
| Format timestamp tidak dikenal | Ditolak        |
| Nilai bukan angka          | Ditolak            |
| timestamp duplikat         | Ditolak            |
| candle tidak urut          | Ditolak            |
| harga ≤ 0                  | Ditolak            |
| high < max(open, close)    | Ditolak            |
| low > min(open, close)     | Ditolak            |
| volume < 0                 | Ditolak            |
| missing data melebihi ambang | Ditandai/ditolak |

Semua kegagalan dicatat eksplisit
pada `integrity_status` dan/atau error.

---

# 9. Dataset Versioning

Per ARC-004 §10:

```text
SYMBOL_TIMEFRAME_START_END_vNNN
```

`dataset_version` merepresentasikan satu snapshot immutable.

---

# 10. Testing (DEV-002)

Unit tests (DEV-002 §7, TODO-015 Tests):

- valid CSV → Dataset lengkap;
- missing columns → ditolak;
- malformed timestamp → ditolak;
- duplicate timestamp → ditolak;
- invalid OHLC → ditolak;
- missing values → ditandai/ditolak;
- unsorted data → ditolak.

Golden/acceptance test: file fixture CSV
→ Dataset yang sudah diverifikasi (DEV-002 §9).

---

# 11. Traceability

| Item              | Requirement / Feature     |
| ----------------- | ------------------------- |
| Load CSV          | FR-001, FEAT-001          |
| Validate          | FR-002, FEAT-002          |
| Integrity rules   | ARC-004 §8                |
| Dataset metadata  | ARC-004 §6.2              |
| Versioning        | FR-010, FEAT-009          |

---

# 12. Compliance

| Constitution Article | Data Engine requirement          |
| -------------------- | -------------------------------- |
| Article 7            | Processing deterministic         |
| Article 13           | Data immutable                   |
| Article 14           | DATA module satu tanggung jawab  |

---

# 13. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-004_Data_Architecture.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-007_Feature_Specification.md`
- `docs/04-development/DEV-002_Testing_Strategy.md`
- `docs/05-research/RSH-002_Experiment_Specification.md`

---

# 14. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial data engine spec         |

---

**Document Status:** Draft

**Document ID:** ENG-001

**Version:** 1.0.0

**End of Document**
