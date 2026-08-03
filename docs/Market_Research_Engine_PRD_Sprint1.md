# Market Research Engine (MRE)

## Product Requirements Document (PRD)

Version: 0.1 (Foundation)

## Vision

**Market Research Engine (MRE)** adalah framework untuk menguji
hipotesis trading secara ilmiah menggunakan pendekatan event-driven dan
analisis statistik.

Prinsip utama:

> Jangan percaya strategi. Percaya data.

Framework ini bukan sekadar backtester. Backtest hanyalah salah satu
output dari proses riset.

------------------------------------------------------------------------

# Goals

-   Membangun framework reusable untuk menguji berbagai strategi
    trading.
-   Memisahkan *market research* dari *trade simulation*.
-   Menghasilkan metrik statistik yang dapat direproduksi.
-   Mendukung eksperimen bertahap.

------------------------------------------------------------------------

# Non Goals (Sprint 1)

-   Tidak ada entry BUY/SELL.
-   Tidak ada TP/SL.
-   Tidak ada optimasi.
-   Tidak ada machine learning.

------------------------------------------------------------------------

# Architecture

``` text
CSV
 │
 ▼
Data Loader
 │
 ▼
Validator
 │
 ▼
Domain Models
 │
 ▼
Detector Layer
 │
 ▼
Event Engine
 │
 ▼
Probability Engine
 │
 ▼
Trading Engine (Future)
 │
 ▼
Reports
```

------------------------------------------------------------------------

# Core Principles

1.  Event-driven architecture.
2.  Pure functions (input → output).
3.  Reproducible experiments.
4.  Configuration over hardcode.
5.  Unit-test first.
6.  Strategy sebagai plugin.

------------------------------------------------------------------------

# Domain Model

## Candle

-   timestamp
-   open
-   high
-   low
-   close
-   volume

## Swing

-   index
-   price
-   type (HIGH/LOW)

## Trendline

-   start
-   end
-   slope
-   intercept

## IndicatorSeries

Representasi umum untuk RSI, EMA, ATR, dll.

## Event

-   type
-   index
-   metadata

Contoh: - SWING_HIGH - SWING_LOW - RSI_BREAKOUT - PRICE_BREAKOUT

## Signal

Kombinasi beberapa event.

Contoh:

RSI_BREAKOUT + PRICE_BREAKOUT =\> BUY_SIGNAL

## Trade

Dipakai mulai Sprint berikutnya.

------------------------------------------------------------------------

# Folder Structure

``` text
market_research_engine/
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── core/
│   ├── models/
│   ├── loaders/
│   ├── indicators/
│   ├── detectors/
│   ├── engines/
│   ├── reports/
│   ├── utils/
│   └── strategies/
├── tests/
├── datasets/
├── experiments/
└── reports/
```

------------------------------------------------------------------------

# Sprint 1 Deliverables

## 1. Project Skeleton

Target: - Struktur project siap dikembangkan.

## 2. Domain Models

Implementasi: - Candle - Swing - Trendline - IndicatorSeries - Event -
Signal - Trade

## 3. CSV Loader

Harus mendukung: - Header / tanpa header - Delimiter koma / titik koma -
Variasi format tanggal - Missing value - Duplicate - Sorting timestamp

## 4. Dataset Validator

Validasi: - OHLC valid - Timestamp ascending - Duplicate - Missing
value - Gap detection

## 5. Config

Gunakan YAML.

Contoh:

``` yaml
dataset:
  path: datasets/XAUUSD_H1.csv

indicator:
  rsi: 14

fractal:
  left: 2
  right: 2
```

## 6. Logger

Minimal level: - INFO - WARNING - ERROR

## 7. Unit Test

Minimal: - Loader - Validator - Models - Utils

------------------------------------------------------------------------

# Coding Standards

-   Type hints.
-   Dataclass bila sesuai.
-   Pure function.
-   Tidak ada print dalam business logic.
-   Dokumentasi setiap public class/function.

------------------------------------------------------------------------

# Experiment Philosophy

Setiap eksperimen memiliki: - ID - Hipotesis - Dataset - Parameter -
Hasil - Kesimpulan

Contoh:

EXP-0001

Hipotesis: RSI Trendline Breakout meningkatkan probabilitas breakout
price.

------------------------------------------------------------------------

# Future Roadmap

Sprint 2 - Swing Detector - RSI - Trendline Builder

Sprint 3 - Event Engine - Probability Engine

Sprint 4 - Trade Simulator

Sprint 5 - Optimization

Sprint 6 - Strategy Comparison

Sprint 7 - Monte Carlo - Walk Forward - ML Experiment

------------------------------------------------------------------------

# Definition of Done Sprint 1

-   Project structure selesai.
-   Domain model stabil.
-   CSV Loader robust.
-   Validator berjalan.
-   Config YAML.
-   Logger tersedia.
-   Unit test hijau.
-   README tersedia.

Belum ada trading.

Sprint 1 dianggap berhasil bila framework sudah mampu membaca,
memvalidasi, dan merepresentasikan data market secara konsisten.

------------------------------------------------------------------------

# Guiding Principle

> "Tambahkan fitur hanya jika eksperimen membutuhkannya."
