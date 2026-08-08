---
title: Document ID Standard
document_id: FND-003
version: 1.0.0
status: Approved
category: Foundation
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001_Project_Charter.md
  - FND-002_Documentation_Standard.md

referenced_by:
  - FND-004_Document_Index.md
  - All Project Documentation
---

# Document ID Standard

> **Every document has an identity. Every identity has a purpose.**

---

# 1. Purpose

Dokumen ini mendefinisikan sistem identifikasi resmi untuk seluruh
dokumentasi Market Research Engine (MRE).

Document ID digunakan untuk:

- mengidentifikasi dokumen secara unik;
- membedakan dokumen berdasarkan domain;
- mempermudah referensi silang;
- mempermudah tracking perubahan;
- mencegah duplikasi dokumen;
- mempermudah komunikasi antar developer dan researcher;
- membantu AI assistant memahami struktur knowledge base;
- menjaga dokumentasi tetap terorganisir ketika project berkembang.

Document ID merupakan bagian dari governance dokumentasi MRE.

---

# 2. Scope

Standar ini berlaku untuk seluruh dokumen yang berada di repository
Market Research Engine.

Termasuk:

- Foundation Documents
- Product Documents
- Architecture Documents
- Engineering Documents
- Research Documents
- Architecture Decision Records
- Experiment Documents
- Templates
- Reference Documents

Standar ini tidak berlaku untuk:

- source code;
- dataset;
- generated report;
- binary artifact;
- temporary files;
- build artifacts.

---

# 3. Design Goals

Sistem Document ID harus memenuhi lima karakteristik.

## 3.1 Unique

Setiap dokumen resmi harus memiliki ID unik.

Tidak boleh ada dua dokumen aktif dengan ID yang sama.

---

## 3.2 Stable

Document ID tidak berubah hanya karena:

- judul berubah;
- isi dokumen diperbarui;
- file dipindahkan dalam kategori yang sama.

ID merepresentasikan identitas dokumen,
bukan nama file.

---

## 3.3 Human Readable

Developer harus dapat memahami kategori dokumen
hanya dengan melihat ID.

Contoh:

```text
ARC-004
```

langsung menunjukkan bahwa dokumen tersebut
berada dalam domain Architecture.

---

## 3.4 Machine Friendly

Format ID harus mudah diproses oleh:

- script;
- documentation tooling;
- search engine;
- AI assistant;
- CI/CD;
- documentation generator.

---

## 3.5 Predictable

ID harus mengikuti pola yang konsisten.

Tidak boleh dibuat secara random.

---

# 4. Document ID Format

Format standar:

```text
<PREFIX>-<NUMBER>
```

Contoh:

```text
FND-001
PRD-001
ARC-001
ENG-001
DEV-001
RSH-001
ADR-001
EXP-001
TMP-001
REF-001
```

---

# 5. Prefix Registry

Prefix menunjukkan kategori utama dokumen.

| Prefix | Category                     | Description                                  |
| ------ | ---------------------------- | -------------------------------------------- |
| `FND`  | Foundation                   | Identitas dan fondasi project                |
| `PRD`  | Product                      | Product vision dan requirements              |
| `ARC`  | Architecture                 | Arsitektur dan desain sistem                 |
| `ENG`  | Engine                       | Spesifikasi engine dan core subsystem        |
| `DEV`  | Development                  | Development process dan engineering practice |
| `RSH`  | Research                     | Metodologi dan penelitian                    |
| `ADR`  | Architecture Decision Record | Keputusan arsitektur                         |
| `EXP`  | Experiment                   | Eksperimen dan hasil penelitian              |
| `TMP`  | Template                     | Template dokumentasi                         |
| `REF`  | Reference                    | Referensi teknis atau pengetahuan pendukung  |

---

# 6. Foundation Documents

Prefix:

```text
FND
```

Foundation digunakan untuk dokumen yang mendefinisikan
identitas, prinsip, aturan, dan status project.

Contoh:

```text
FND-001 Project Charter
FND-002 Documentation Standard
FND-003 Document ID Standard
FND-004 Document Index
FND-005 Project Context
FND-006 Project Status
FND-007 Roadmap
FND-008 TODO
FND-009 Glossary
```

Foundation documents menjadi referensi utama
untuk seluruh kategori lainnya.

---

# 7. Product Documents

Prefix:

```text
PRD
```

Product digunakan untuk dokumen yang menjelaskan
produk, pengguna, kebutuhan, dan behavior.

Contoh:

```text
PRD-001 Product Vision
PRD-002 Product Requirements Document
PRD-003 User Stories
PRD-004 Use Cases
PRD-005 Feature Specification
```

Product document tidak boleh mendefinisikan
detail implementasi internal secara berlebihan.

Product menjelaskan:

> What and Why.

Architecture menjelaskan:

> How.

---

# 8. Architecture Documents

Prefix:

```text
ARC
```

Architecture digunakan untuk dokumen yang menjelaskan
struktur dan desain teknis framework.

Contoh:

```text
ARC-001 System Architecture
ARC-002 Domain Model
ARC-003 Event Architecture
ARC-004 Data Architecture
ARC-005 Plugin Architecture
ARC-006 Module Architecture
```

Architecture documents harus konsisten dengan
Architecture Constitution pada `FND-001`.

---

# 9. Engine Documents

Prefix:

```text
ENG
```

Engine digunakan untuk dokumentasi mengenai
subsystem atau engine tertentu.

Contoh:

```text
ENG-001 Data Engine
ENG-002 Event Engine
ENG-003 Signal Engine
ENG-004 Probability Engine
ENG-005 Simulation Engine
ENG-006 Statistics Engine
ENG-007 Reporting Engine
```

Engine document harus menjelaskan:

- purpose;
- responsibility;
- inputs;
- outputs;
- dependencies;
- interfaces;
- constraints;
- testing requirements.

---

# 10. Development Documents

Prefix:

```text
DEV
```

Development digunakan untuk dokumentasi
mengenai proses software engineering.

Contoh:

```text
DEV-001 Coding Standard
DEV-002 Testing Strategy
DEV-003 Git Workflow
DEV-004 Development Guide
DEV-005 Release Process
```

---

# 11. Research Documents

Prefix:

```text
RSH
```

Research digunakan untuk metodologi
dan framework penelitian.

Contoh:

```text
RSH-001 Research Methodology
RSH-002 Backtest Protocol
RSH-003 Validation Methodology
RSH-004 Statistical Methodology
```

Research documents menjelaskan bagaimana
eksperimen seharusnya dilakukan.

---

# 12. Architecture Decision Records

Prefix:

```text
ADR
```

ADR digunakan untuk keputusan arsitektur
yang memiliki dampak signifikan terhadap project.

Contoh:

```text
ADR-001 Adopt Event-Driven Architecture
ADR-002 Use Immutable Dataset Model
ADR-003 Adopt Plugin-Based Detector Architecture
```

ADR memiliki lifecycle sendiri:

```text
Proposed
    ↓
Accepted
    ↓
Superseded
    ↓
Deprecated
```

Tidak semua ADR harus tetap aktif.

Namun histori keputusan harus dipertahankan.

---

# 13. Experiment Documents

Prefix:

```text
EXP
```

Experiment digunakan untuk mendokumentasikan
eksperimen penelitian tertentu.

Contoh:

```text
EXP-001 RSI Trendline Breakout Baseline
EXP-002 RSI Trendline Breakout RR Analysis
EXP-003 EMA Filter Experiment
```

Experiment harus memiliki hubungan dengan:

- hypothesis;
- dataset;
- configuration;
- strategy;
- result;
- conclusion.

Contoh:

```text
RSH-001
   │
   └── EXP-001
          │
          └── Result
```

---

# 14. Template Documents

Prefix:

```text
TMP
```

Template digunakan untuk dokumen yang akan
digunakan berulang kali.

Contoh:

```text
TMP-001 Standard Document
TMP-002 Architecture Decision Record
TMP-003 Experiment Report
TMP-004 Design Specification
```

Template tidak dianggap sebagai project specification.

Template merupakan alat untuk membuat specification.

---

# 15. Reference Documents

Prefix:

```text
REF
```

Reference digunakan untuk informasi pendukung
yang bukan merupakan core project specification.

Contoh:

```text
REF-001 Market Data Format
REF-002 Statistical Terminology
REF-003 Python Environment
```

Reference tidak boleh bertentangan dengan
Foundation atau Architecture documents.

---

# 16. Numbering Rules

Nomor dokumen menggunakan tiga digit.

Format:

```text
001
002
003
...
999
```

Contoh:

```text
FND-001
FND-002
FND-003
```

---

# 17. Sequential Numbering

Nomor diberikan secara sequential
dalam masing-masing kategori.

Contoh:

```text
FND-001
FND-002
FND-003
```

Tidak boleh langsung membuat:

```text
FND-001
FND-005
FND-009
```

tanpa alasan yang terdokumentasi.

Nomor yang sudah pernah digunakan
tidak boleh digunakan kembali.

---

# 18. Deleted Documents

Apabila sebuah dokumen dihapus,
Document ID tidak boleh digunakan kembali.

Contoh:

```text
ARC-004
```

dihapus.

Maka:

```text
ARC-004
```

tetap reserved permanently.

Hal ini menjaga histori repository
tetap dapat ditelusuri.

---

# 19. Deprecated Documents

Jika sebuah dokumen tidak lagi berlaku,
statusnya harus diubah menjadi:

```text
Deprecated
```

Dokumen tidak boleh langsung dihapus
jika masih memiliki historical value.

Jika digantikan oleh dokumen baru,
gunakan relationship:

```text
Superseded By: ARC-008
```

Contoh:

```text
ARC-003
Status: Deprecated
Superseded By: ARC-007
```

---

# 20. Document ID vs File Name

Document ID dan filename adalah dua konsep berbeda.

Document ID:

```text
ARC-003
```

Filename:

```text
Event_Architecture.md
```

Keduanya harus ditampilkan pada metadata.

Contoh:

```yaml
---
title: Event Architecture
document_id: ARC-003
---
```

Filename boleh berubah.

Document ID tetap.

---

# 21. Document ID in Markdown

Setiap dokumen resmi harus mencantumkan
Document ID pada bagian metadata.

Contoh:

```yaml
---
title: System Architecture
document_id: ARC-001
version: 1.0.0
status: Draft
category: Architecture
---
```

---

# 22. Cross-Reference Convention

Saat merujuk dokumen lain,
gunakan Document ID.

Contoh:

```text
See FND-001 for Project Charter.
```

Lebih baik daripada hanya:

```text
See Project Charter.
```

Karena Document ID bersifat unik.

---

# 23. Cross-Reference With Title

Untuk readability,
Document ID dapat disertai judul.

Format:

```text
FND-001 — Project Charter
```

Contoh:

> Architecture decisions must comply with
> `FND-001 — Project Charter`.

---

# 24. Document Relationships

Dokumen dapat memiliki relationship berikut:

```text
Depends On
Referenced By
Supersedes
Superseded By
Implements
Defines
Extends
Related To
```

Contoh:

```yaml
depends_on:
  - FND-001
  - FND-002

implements:
  - PRD-002

related_to:
  - ARC-003
```

---

# 25. Document Dependency

Dependency harus mengikuti arah yang logis.

Contoh:

```text
Foundation
    ↓
Product
    ↓
Architecture
    ↓
Engine
    ↓
Development
    ↓
Research
    ↓
Experiment
```

Namun dependency tidak harus selalu linear.

Contoh:

```text
FND-001
  │
  ├── PRD-001
  │      │
  │      └── ARC-001
  │
  └── ARC-001
         │
         └── ENG-001
```

---

# 26. Circular Dependency

Circular dependency harus dihindari.

Contoh yang tidak diperbolehkan:

```text
ARC-001
   ↓
ENG-001
   ↓
ARC-001
```

Jika circular dependency tidak dapat dihindari,
harus dibuat ADR untuk menjelaskan alasannya.

---

# 27. Document Lifecycle

Setiap dokumen mengikuti lifecycle:

```text
Created
   ↓
Draft
   ↓
Review
   ↓
Approved
   ↓
Maintained
   ↓
Deprecated
```

Tidak semua dokumen harus melalui semua tahap.

Contoh:

```text
TMP-001
```

dapat langsung:

```text
Draft
↓
Approved
```

---

# 28. Version vs Document ID

Document ID mengidentifikasi dokumen.

Version mengidentifikasi revisinya.

Contoh:

```text
FND-001
Version 1.0.0
```

Kemudian:

```text
FND-001
Version 1.1.0
```

Tetap merupakan dokumen yang sama.

Document ID tidak berubah.

---

# 29. Semantic Versioning

Dokumen menggunakan format:

```text
MAJOR.MINOR.PATCH
```

## MAJOR

Digunakan jika perubahan mengubah
fundamental meaning dokumen.

Contoh:

```text
1.0.0 → 2.0.0
```

---

## MINOR

Digunakan jika terdapat penambahan
informasi yang tidak merusak struktur
atau meaning sebelumnya.

Contoh:

```text
1.0.0 → 1.1.0
```

---

## PATCH

Digunakan untuk:

- typo;
- grammar;
- formatting;
- link correction;
- minor clarification.

Contoh:

```text
1.0.0 → 1.0.1
```

---

# 30. Reserved Prefixes

Prefix berikut reserved untuk penggunaan
di masa depan:

```text
SYS
API
OPS
SEC
```

Prefix tersebut tidak boleh digunakan
tanpa perubahan resmi terhadap standar ini.

---

# 31. Special Rule for ADR

ADR memiliki numbering global.

Contoh:

```text
ADR-001
ADR-002
ADR-003
```

Nomor ADR tidak dikelompokkan
berdasarkan subsystem.

Tujuannya adalah menjaga chronological history
dari architectural decisions.

---

# 32. Special Rule for Experiments

Experiment menggunakan sequential ID.

Contoh:

```text
EXP-001
EXP-002
EXP-003
```

Experiment ID bersifat immutable.

Jika experiment diulang dengan konfigurasi berbeda,
buat Experiment baru.

Contoh:

```text
EXP-001
```

Baseline.

Kemudian:

```text
EXP-002
```

Improved configuration.

Jangan mengubah `EXP-001` menjadi eksperimen lain.

---

# 33. Experiment Reproducibility

Setiap Experiment ID harus dapat dikaitkan
dengan minimal:

```text
Dataset
Configuration
Strategy
Code Version
Result
Conclusion
```

Contoh:

```text
EXP-001

Dataset:
XAUUSD H1

Strategy:
RSI Trendline Breakout

Configuration:
RR = 2.0

Code Version:
commit abc123

Result:
Win Rate = 42.7%
```

Dengan demikian sebuah experiment
dapat ditelusuri kembali.

---

# 34. Document Registry

Seluruh Document ID harus dicatat
dalam:

```text
FND-004 — Document Index
```

Document Index menjadi registry resmi.

Tidak boleh ada dokumen resmi
yang tidak terdaftar.

---

# 35. ID Allocation Process

Proses pembuatan dokumen baru:

```text
Identify Category
       ↓
Select Prefix
       ↓
Check Document Index
       ↓
Assign Next Number
       ↓
Create Document
       ↓
Register Document
```

Contoh:

Developer ingin membuat
System Architecture.

Category:

```text
Architecture
```

Prefix:

```text
ARC
```

Document Index terakhir:

```text
ARC-005
```

Maka document berikutnya:

```text
ARC-006
```

---

# 36. Duplicate Prevention

Sebelum membuat dokumen baru,
developer wajib melakukan pencarian
terhadap Document Index.

Tujuannya untuk memastikan
dokumen yang sama belum tersedia.

Jika konsep sudah memiliki dokumen,
buat perubahan pada dokumen tersebut
atau buat ADR jika diperlukan.

Jangan membuat dokumen duplikat.

---

# 37. AI Assistant Rules

AI assistant yang bekerja pada repository MRE
harus mengikuti aturan berikut:

1. Selalu mempertahankan Document ID yang sudah ada.
2. Tidak membuat ID yang sudah pernah digunakan.
3. Tidak mengubah ID tanpa alasan resmi.
4. Memeriksa Document Index sebelum membuat dokumen baru.
5. Menggunakan Document ID ketika melakukan cross-reference.
6. Mengikuti prefix registry.
7. Tidak mengarang Document ID yang belum terdaftar.

AI assistant harus memperlakukan
Document ID sebagai identifier immutable.

---

# 38. Examples

## Foundation

```text
FND-001 — Project Charter
FND-002 — Documentation Standard
FND-003 — Document ID Standard
```

## Product

```text
PRD-001 — Product Vision
PRD-002 — Product Requirements
```

## Architecture

```text
ARC-001 — System Architecture
ARC-002 — Domain Model
ARC-003 — Event Architecture
```

## Engine

```text
ENG-001 — Data Engine
ENG-002 — Event Engine
ENG-003 — Probability Engine
```

## Development

```text
DEV-001 — Coding Standard
DEV-002 — Testing Strategy
```

## Research

```text
RSH-001 — Research Methodology
RSH-002 — Backtest Protocol
```

## ADR

```text
ADR-001 — Adopt Event-Driven Architecture
```

## Experiment

```text
EXP-001 — RSI Trendline Breakout Baseline
```

---

# 39. Anti-Patterns

Berikut contoh yang tidak diperbolehkan.

## Random ID

```text
DOC-9281
```

Tidak diperbolehkan.

---

## Reusing ID

```text
ARC-003
```

pernah digunakan lalu diberikan
ke dokumen lain.

Tidak diperbolehkan.

---

## Category Mismatch

```text
PRD-003 — Probability Engine Architecture
```

Tidak ideal.

Dokumen tersebut seharusnya berada
di Architecture atau Engine.

---

## Missing ID

Dokumen resmi tanpa:

```yaml
document_id:
```

Tidak diperbolehkan.

---

## Ambiguous Reference

```text
See architecture document.
```

Lebih baik:

```text
See ARC-001 — System Architecture.
```

---

# 40. Governance

Perubahan terhadap Document ID Standard
merupakan perubahan terhadap governance dokumentasi.

Perubahan besar harus:

1. Didokumentasikan.
2. Direview.
3. Menghasilkan perubahan version.
4. Memperbarui dokumen terkait.

Jika perubahan memengaruhi architecture,
buat ADR.

---

# 41. Definition of Done

Document ID Standard dianggap selesai apabila:

- [x] Prefix registry didefinisikan.
- [x] Numbering scheme didefinisikan.
- [x] Lifecycle didefinisikan.
- [x] Versioning didefinisikan.
- [x] Cross-reference didefinisikan.
- [x] Dependency rules didefinisikan.
- [x] ADR rules didefinisikan.
- [x] Experiment rules didefinisikan.
- [x] AI rules didefinisikan.
- [x] Document Index ditetapkan sebagai registry.
- [x] Governance perubahan didefinisikan.

---

# 42. Summary

Document ID adalah identitas resmi
setiap knowledge artifact dalam
Market Research Engine.

Format:

```text
<PREFIX>-<NUMBER>
```

Contoh:

```text
FND-001
PRD-001
ARC-001
ENG-001
DEV-001
RSH-001
ADR-001
EXP-001
TMP-001
REF-001
```

Document ID:

- unik;
- immutable;
- sequential;
- human-readable;
- machine-friendly.

---

# Closing Statement

Ketika Market Research Engine memiliki
puluhan atau bahkan ratusan dokumen,
struktur knowledge base harus tetap dapat dipahami.

Document ID menyediakan identitas tersebut.

Dengan sistem ini,
setiap keputusan,
spesifikasi,
eksperimen,
dan pengetahuan memiliki alamat yang jelas.

> **If knowledge has no identity, it is difficult to govern.**

Document ID memastikan knowledge
Market Research Engine tetap terstruktur,
terlacak,
dan dapat berkembang dalam jangka panjang.

---
