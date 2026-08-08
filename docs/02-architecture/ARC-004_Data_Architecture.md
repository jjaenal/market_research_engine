---
title: Data Architecture
document_id: ARC-004
version: 1.0.0
status: Draft
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
  - ARC-002
  - PRD-003
  - PRD-004
  - PRD-006

referenced_by:
  - ARC-006

purpose: Define the data model of MRE — schema, CSV contract, integrity rules, and dataset versioning
---

# Data Architecture

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ARC-004 mendefinisikan **data architecture** dari Market Research Engine (MRE).

Dokumen ini menjawab TODO-011 — Define Data Model (FND-008).

ARC-004 menetapkan:

- schema data (Candle + metadata Dataset);
- kontrak format input CSV;
- aturan data integrity;
- dataset versioning dan immutability.

---

# 2. Scope

Scope ARC-004:

- schema Candle dan Dataset metadata;
- kontrak CSV;
- aturan validasi data;
- versioning dataset.

Di luar scope ARC-004:

- persistensi penyimpanan teknis;
- domain model (ARC-002);
- event architecture (ARC-003);
- module layout (ARC-006).

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- data scientist;
- quantitative researcher;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Pipeline MRE dimulai dari data (PRD-003 §7.1, §7.2):

```text
CSV → Import → Validate → ...
```

Schema data harus didefinisikan secara eksplisit
agar experiment reproducible (FND-009 §9.4).

---

# 5. Definitions

Terminologi mengikuti **FND-009 — Project Glossary**.

| Term             | Definition                                |
| ---------------- | ----------------------------------------- |
| Market Data      | Data harga dan volume dari market          |
| Historical Data  | Data historis untuk backtesting/research  |
| Dataset          | Kumpulan data yang digunakan experiment   |
| Dataset Version  | Identifier agar dataset dapat direproduksi |
| OHLCV            | Open, High, Low, Close, Volume            |
| Candle           | Satu unit observasi market dalam timeframe |
| Data Integrity   | Konsistensi dan kebenaran data            |

---

# 6. Data Model

## 6.1 Candle Schema

| Field     | Type       | Description                  | Constraint              |
| --------- | ---------- | ---------------------------- | ----------------------- |
| timestamp | datetime   | Waktu candle (timezone-aware) | unik, strictly increasing |
| open      | float      | Harga pembukaan              | > 0                     |
| high      | float      | Harga tertinggi              | ≥ max(open, close)      |
| low       | float      | Harga terendah               | ≤ min(open, close)      |
| close     | float      | Harga penutupan              | > 0                     |
| volume    | float/int  | Volume transaksi             | ≥ 0                     |

Timezone harus didefinisikan eksplisit (FND-009 §9.7).

## 6.2 Dataset Metadata

| Field           | Type   | Description                          |
| --------------- | ------ | ------------------------------------ |
| dataset_version | string | Identifier unik dan reproducible     |
| symbol          | string | Contoh: XAUUSD                       |
| timeframe       | string | Contoh: H1                           |
| timezone        | string | Contoh: UTC                          |
| source          | string | Sumber data                          |
| date_range      | range  | Rentang waktu data                   |
| candle_count    | int    | Jumlah candle                        |
| integrity_status | string | Hasil validasi                       |

---

# 7. CSV Contract

Format input import (PRD-003 §7.1, PRD-006 §8.1):

```csv
timestamp,open,high,low,close,volume
2020-01-01T00:00:00Z,1520.10,1522.00,1518.50,1521.30,1000
```

Aturan:

- satu file CSV untuk satu symbol + timeframe;
- kolom wajib: timestamp, open, high, low, close, volume;
- timestamp format ISO 8601 dengan timezone eksplisit;
- UTF-8, pemisah koma;
- tidak ada kolom opsional yang diwajibkan saat ini.

Kegagalan (PRD-003 §7.1 failure conditions):

- file tidak ditemukan;
- kolom wajib hilang;
- format timestamp tidak dikenal;
- nilai bukan angka.

---

# 8. Data Integrity Rules

Validasi (PRD-003 §7.2, FR-002):

| Aturan                        | Konsekuensi            |
| ----------------------------- | ---------------------- |
| timestamp duplikat            | Dataset ditolak        |
| candle tidak urut             | Dataset ditolak        |
| harga ≤ 0                     | Dataset ditolak        |
| high < max(open, close)       | Dataset ditolak        |
| low > min(open, close)        | Dataset ditolak        |
| missing data melebihi ambang  | Ditandai / ditolak     |
| volume < 0                    | Dataset ditolak        |

Hasil validasi dicatat pada `integrity_status`.

---

# 9. Immutability

Per FND-001 Article 13:

> Historical Data tidak boleh dimodifikasi.

Konsekuensi:

- dataset yang sudah tervalidasi tidak boleh diubah;
- transformasi menghasilkan dataset baru;
- dataset_version merepresentasikan satu snapshot.

---

# 10. Dataset Versioning

Pattern (FND-009 §9.4):

```text
SYMBOL_TIMEFRAME_START_END_vNNN
```

Contoh:

```text
XAUUSD_H1_2020_2025_v001
```

Aturan:

- dataset_version immutable;
- setiap perubahan data menghasilkan versi baru;
- experiment mereferensikan dataset_version (FR-003, FR-010).

---

# 11. Traceability

| Item                    | Requirement / Feature     |
| ----------------------- | ------------------------- |
| Candle schema           | FR-001 (load data)        |
| CSV contract            | FR-001, FEAT-001          |
| Integrity rules         | FR-002, FEAT-002          |
| Dataset versioning      | FR-010 (reproduce), FEAT-009 |
| Immutability            | Article 13                |

---

# 12. Compliance

| Constitution Article | Data requirement                    |
| -------------------- | ----------------------------------- |
| Article 7            | Processing deterministic             |
| Article 13           | Data immutable                      |
| Article 14           | DATA module satu tanggung jawab     |

---

# 13. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-006_MVP_Definition.md`

---

# 14. Revision History

| Version | Date       | Changes               |
| ------- | ---------- | --------------------- |
| 1.0.0   | 2026-08-08 | Initial data architecture |

---

**Document Status:** Draft

**Document ID:** ARC-004

**Version:** 1.0.0

**End of Document**
