---
title: Project Glossary
document_id: FND-009
version: 1.0.0
status: Active
category: Foundation
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-003
  - FND-005
  - FND-007
  - FND-008

purpose: Establish the controlled vocabulary used throughout Market Research Engine
---

# Project Glossary

> **If we use the same words differently, we are building different systems.**

---

# 1. Purpose

FND-009 mendefinisikan vocabulary resmi
yang digunakan di seluruh Market Research Engine (MRE).

Glossary ini bertujuan memastikan:

- terminology konsisten;
- domain concepts tidak ambigu;
- documentation menggunakan istilah yang sama;
- source code menggunakan terminology yang sama;
- experiment menggunakan definisi yang sama;
- statistical metrics memiliki arti yang jelas;
- communication antar development/research context tetap sinkron.

---

# 2. Terminology Rules

## Rule 001 — One Concept, One Name

Jika satu konsep sudah memiliki
nama resmi, gunakan nama tersebut.

Contoh:

```text
Trade
```

jangan berganti-ganti menjadi:

```text
Transaction
Position
Deal
Order
```

jika yang dimaksud sebenarnya adalah
satu konsep yang sama.

---

# 3. Rule 002 — Order ≠ Trade ≠ Position

Ketiga istilah ini memiliki
arti berbeda.

```text
Order
  ↓
Execution
  ↓
Position
  ↓
Exit
  ↓
Trade
```

Detail domain final akan didefinisikan
dalam Architecture phase.

---

# 4. Rule 003 — Signal ≠ Trade

Signal adalah hasil dari
strategy logic.

Trade adalah hasil dari
execution/simulation.

Contoh:

```text
Signal
   ↓
Order
   ↓
Execution
   ↓
Trade
```

Tidak semua signal harus
menghasilkan trade.

---

# 5. Rule 004 — Hypothesis ≠ Conclusion

Hypothesis adalah sesuatu
yang ingin diuji.

Conclusion adalah hasil
setelah evidence dianalisis.

---

# 6. Rule 005 — Result ≠ Evidence

Result adalah output experiment.

Evidence adalah result yang telah
dianalisis dalam konteks
research question.

---

# 7. Rule 006 — Backtest ≠ Proof

Backtest adalah metode
simulasi historical.

Backtest tidak otomatis
membuktikan bahwa strategy
memiliki future edge.

---

# 8. Core Project Terms

---

## 8.1 Market Research Engine (MRE)

Research/backtesting framework
yang digunakan untuk:

- menguji trading hypotheses;
- menjalankan experiments;
- mengukur statistical behavior;
- membandingkan assumptions;
- menghasilkan evidence.

---

## 8.2 Research

Proses sistematis untuk
menghasilkan evidence terhadap
suatu hypothesis.

---

## 8.3 Research Question

Pertanyaan yang ingin
dijawab oleh research.

Contoh:

> Apakah RSI Trendline Breakout
> memiliki measurable statistical edge?

---

## 8.4 Hypothesis

Pernyataan yang dapat diuji
menggunakan evidence.

Contoh:

> RSI Trendline Breakout menghasilkan
> positive expectancy pada kondisi
> market tertentu.

---

## 8.5 Experiment

Prosedur terkontrol untuk
menguji hypothesis.

Experiment harus memiliki:

- dataset;
- configuration;
- assumptions;
- execution rules;
- metrics;
- result;
- conclusion.

---

## 8.6 Experiment Configuration

Sekumpulan parameter dan
assumptions yang menentukan
bagaimana experiment dijalankan.

Contoh:

```text
symbol
timeframe
date range
strategy parameters
RR
SL
TP
position sizing
transaction cost
slippage
```

---

## 8.7 Experiment ID

Identifier unik untuk
mengidentifikasi satu experiment.

Contoh:

```text
EXP-001
```

---

## 8.8 Baseline

Experiment awal yang digunakan
sebagai reference point.

Baseline dilakukan sebelum
optimization atau modification
besar.

---

## 8.9 Control

Variabel yang sengaja
dipertahankan tetap selama
experiment.

---

## 8.10 Independent Variable

Variabel yang sengaja diubah
untuk melihat pengaruhnya.

Contoh:

```text
Risk/Reward
```

---

## 8.11 Dependent Variable

Output yang diukur sebagai
akibat perubahan experiment.

Contoh:

```text
Expectancy
Win Rate
Profit Factor
```

---

# 9. Market Data Terms

---

## 9.1 Market Data

Data yang merepresentasikan
historical atau live market behavior.

Untuk MVP:

```text
Historical OHLCV
```

---

## 9.2 Historical Data

Market data dari periode
yang telah terjadi.

---

## 9.3 Dataset

Kumpulan data yang digunakan
oleh sebuah experiment.

---

## 9.4 Dataset Version

Identifier yang memungkinkan
dataset tertentu direproduksi.

Contoh:

```text
XAUUSD_H1_2020_2025_v001
```

---

## 9.5 OHLCV

Singkatan dari:

```text
Open
High
Low
Close
Volume
```

---

## 9.6 Candle / Bar

Satu unit observasi market
dalam timeframe tertentu.

Contoh:

```text
XAUUSD H1
```

berarti satu candle
merepresentasikan satu jam.

---

## 9.7 Timestamp

Waktu yang terkait dengan
market observation.

Timezone harus selalu
didefinisikan secara eksplisit.

---

## 9.8 Symbol

Identifier instrument.

Contoh:

```text
XAUUSD
EURUSD
USDJPY
```

---

## 9.9 Timeframe

Interval waktu setiap candle.

Contoh:

```text
M5
M15
H1
H4
D1
```

---

## 9.10 Data Integrity

Kondisi ketika data memenuhi
aturan validity dan consistency
yang telah ditentukan.

---

## 9.11 Missing Data

Market observation yang
hilang atau tidak tersedia.

---

## 9.12 Duplicate Data

Observation yang muncul lebih
dari sekali untuk identifier
yang seharusnya unik.

---

# 10. Strategy Terms

---

## 10.1 Strategy

Sekumpulan deterministic rules
yang digunakan untuk menghasilkan
research signals dan/atau
trade decisions.

---

## 10.2 Strategy Rule

Satu aturan spesifik
dalam sebuah strategy.

Contoh:

```text
RSI > 50
```

---

## 10.3 Strategy Parameter

Nilai yang dapat dikonfigurasi
dalam strategy.

Contoh:

```text
RSI Period = 14
```

---

## 10.4 Indicator

Perhitungan matematis
berdasarkan market data.

Contoh:

```text
RSI
EMA
ATR
SMA
```

---

## 10.5 RSI

Relative Strength Index.

Momentum oscillator yang
mengukur magnitude relatif
perubahan harga.

Dalam MRE, RSI merupakan
technical indicator yang dapat
digunakan sebagai input strategy.

---

## 10.6 Trendline

Garis yang merepresentasikan
hubungan tertentu antara
market points.

Dalam konteks RSI Trendline
Breakout, trendline dapat
dibangun berdasarkan swing
atau pivot pada RSI.

Definisi algoritmik final
akan ditentukan pada strategy
specification.

---

## 10.7 Breakout

Pergerakan yang melewati
boundary atau level yang
telah didefinisikan.

Breakout harus memiliki
deterministic definition.

---

## 10.8 RSI Trendline Breakout

Initial research strategy
yang menjadi experiment pertama MRE.

Conceptual structure:

```text
Price Data
    ↓
RSI
    ↓
RSI Structure
    ↓
RSI Trendline
    ↓
Trendline Break
    ↓
Signal
```

Exact rules belum dianggap
final sampai strategy specification
ditetapkan.

---

# 11. Market Structure Terms

---

## 11.1 Swing High

Market point yang memenuhi
aturan tertentu untuk dianggap
sebagai local high.

---

## 11.2 Swing Low

Market point yang memenuhi
aturan tertentu untuk dianggap
sebagai local low.

---

## 11.3 Pivot

Reference point yang digunakan
untuk menentukan market structure.

---

## 11.4 Trend

Directional market behavior
yang didefinisikan menggunakan
aturan tertentu.

---

## 11.5 Market Regime

Kondisi market tertentu
yang memiliki karakteristik
statistical/structural berbeda.

Contoh conceptual regimes:

```text
Trending
Ranging
High Volatility
Low Volatility
```

---

# 12. Event Terms

---

## 12.1 Event

Sebuah occurrence yang
terdeteksi oleh system.

Contoh:

```text
RSI Cross
Trendline Break
Swing High Formed
```

---

## 12.2 Event Detection

Proses mendeteksi event
dari market observations.

---

## 12.3 Event Timestamp

Waktu ketika event
dianggap terjadi berdasarkan
aturan system.

---

## 12.4 Event Sequence

Urutan events yang terjadi
dalam historical data.

---

# 13. Signal Terms

---

## 13.1 Signal

Output strategy yang
menunjukkan kondisi tertentu
telah terpenuhi.

Contoh:

```text
LONG
SHORT
NO SIGNAL
```

---

## 13.2 Entry Signal

Signal yang memenuhi
condition untuk membuka
potential trade.

---

## 13.3 Exit Signal

Signal yang menunjukkan
condition untuk keluar
dari position.

---

## 13.4 Signal Confirmation

Condition tambahan yang harus
terpenuhi sebelum signal
dianggap valid.

---

## 13.5 Signal Timestamp

Timestamp ketika signal
dianggap valid.

---

# 14. Execution Terms

---

## 14.1 Order

Instruksi untuk melakukan
entry atau exit.

---

## 14.2 Market Order

Order yang diasumsikan
dieksekusi pada market
berdasarkan execution model.

---

## 14.3 Limit Order

Order yang hanya dapat
dieksekusi pada harga tertentu
atau lebih baik sesuai
simulation rules.

---

## 14.4 Stop Order

Order yang aktif setelah
harga mencapai trigger level.

---

## 14.5 Execution

Proses ketika order dianggap
terisi oleh simulation model.

---

## 14.6 Fill Price

Harga yang digunakan sebagai
harga execution.

---

## 14.7 Slippage

Perbedaan antara intended
execution price dan actual
simulated fill price.

---

## 14.8 Transaction Cost

Biaya yang diasumsikan
terjadi ketika melakukan
transaction.

Contoh:

```text
Commission
Spread
Fees
```

---

# 15. Position & Trade Terms

---

## 15.1 Position

Exposure yang sedang aktif
terhadap suatu instrument.

---

## 15.2 Long Position

Position yang memperoleh
profit ketika harga bergerak
naik, berdasarkan model
simulation.

---

## 15.3 Short Position

Position yang memperoleh
profit ketika harga bergerak
turun, berdasarkan model
simulation.

---

## 15.4 Trade

Satu completed research
transaction lifecycle.

Concept:

```text
Entry
  ↓
Position
  ↓
Exit
  ↓
Trade Result
```

---

## 15.5 Entry Price

Harga ketika position
dianggap dibuka.

---

## 15.6 Exit Price

Harga ketika position
dianggap ditutup.

---

## 15.7 Stop Loss (SL)

Rule atau price level yang
membatasi kerugian sesuai
simulation assumptions.

---

## 15.8 Take Profit (TP)

Rule atau price level yang
digunakan untuk merealisasikan
profit sesuai simulation
assumptions.

---

## 15.9 Holding Period

Durasi antara entry
dan exit.

---

# 16. Risk & Reward Terms

---

## 16.1 Risk

Jumlah kerugian yang
didefinisikan sebagai
reference untuk sebuah trade.

---

## 16.2 Reward

Jumlah profit target yang
didefinisikan relatif terhadap
risk.

---

## 16.3 Risk/Reward Ratio (RR)

Perbandingan reward terhadap
risk.

Contoh:

```text
Risk = $100
Reward = $200

RR = 1:2
```

---

## 16.4 R-Multiple

Return sebuah trade yang
dinormalisasi berdasarkan
initial risk.

Contoh:

```text
Risk = $100

Profit = $200

R = +2R
```

Loss:

```text
Loss = $100

R = -1R
```

R-multiple sangat berguna
untuk membandingkan trade
dengan position size berbeda.

---

## 16.5 Position Size

Ukuran position yang
digunakan dalam trade.

---

## 16.6 Risk Per Trade

Jumlah risk yang dialokasikan
untuk satu trade.

---

# 17. Probability Terms

---

## 17.1 Win Rate

Persentase trade yang
menghasilkan positive result.

```text
Win Rate =
Winning Trades / Total Trades
```

---

## 17.2 Loss Rate

Persentase trade yang
menghasilkan negative result.

```text
Loss Rate =
Losing Trades / Total Trades
```

---

## 17.3 Breakeven Rate

Persentase trade yang
menghasilkan approximately
zero result setelah definisi
cost dan tolerance ditentukan.

---

## 17.4 Probability of Win

Estimasi probabilitas bahwa
sebuah trade menghasilkan
positive result berdasarkan
sample yang digunakan.

---

## 17.5 Sample Size

Jumlah observations atau
trades yang digunakan
dalam analysis.

---

# 18. Expectancy Terms

---

## 18.1 Expectancy

Expected average outcome
per trade berdasarkan
probability dan payoff.

Conceptual formula:

```text
E =
(Pwin × AvgWin)
-
(Ploss × AvgLoss)
```

Contoh:

```text
Win Rate = 40%
Average Win = +2R
Loss Rate = 60%
Average Loss = -1R

E =
(0.40 × 2)
-
(0.60 × 1)

E = +0.20R
```

Expectancy positif tidak
menjamin future profitability,
tetapi merupakan salah satu
baseline metric penting.

---

# 19. Performance Terms

---

## 19.1 Gross Profit

Total positive P&L
sebelum dikurangi
gross losses dan biaya
sesuai reporting definition.

---

## 19.2 Gross Loss

Total negative P&L.

---

## 19.3 Net P&L

Total result setelah
komponen biaya yang
didefinisikan experiment
diperhitungkan.

---

## 19.4 Profit Factor

Perbandingan gross profit
terhadap gross loss.

```text
Profit Factor =
Gross Profit / Absolute Gross Loss
```

---

## 19.5 Equity Curve

Representasi perubahan
equity sepanjang sequence
trades.

---

## 19.6 Drawdown

Penurunan equity dari
peak sebelumnya menuju
subsequent trough.

---

## 19.7 Maximum Drawdown

Drawdown terbesar yang
terjadi dalam observation
period.

---

## 19.8 Recovery

Periode yang diperlukan
untuk kembali dari drawdown
menuju previous equity peak.

---

## 19.9 Winning Streak

Jumlah consecutive
winning trades.

---

## 19.10 Losing Streak

Jumlah consecutive
losing trades.

---

# 20. Bias Terms

---

## 20.1 Lookahead Bias

Situasi ketika information
yang secara chronological
belum tersedia pada saat
decision digunakan untuk
membuat historical decision.

Ini merupakan critical
research integrity issue.

---

## 20.2 Data Leakage

Information dari future
atau unavailable context
masuk ke training,
calculation,
atau decision process.

---

## 20.3 Survivorship Bias

Bias yang muncul ketika
dataset hanya berisi entities
yang survive hingga
periode tertentu.

---

## 20.4 Selection Bias

Bias akibat pemilihan
data/sample yang tidak
merepresentasikan population
yang ingin diteliti.

---

# 21. Overfitting Terms

---

## 21.1 Overfitting

Strategy atau model terlalu
disesuaikan terhadap historical
sample sehingga performance
tidak generalize dengan baik.

---

## 21.2 Curve Fitting

Bentuk overfitting ketika
parameter dibuat terlalu cocok
terhadap historical pattern.

---

## 21.3 Data Snooping

Penggunaan atau eksplorasi
data berulang kali sehingga
hasil yang terlihat bagus
dapat muncul secara kebetulan
dan kemudian dianggap sebagai
evidence.

---

## 21.4 Parameter Optimization

Proses mencari parameter
yang memberikan objective
tertentu pada dataset.

Optimization harus dilakukan
setelah baseline tersedia.

---

# 22. Validation Terms

---

## 22.1 In-Sample

Data yang digunakan untuk
development atau parameter
selection.

---

## 22.2 Out-of-Sample (OOS)

Data yang tidak digunakan
untuk development atau
parameter selection dan
digunakan untuk validation.

---

## 22.3 Train Set

Dataset yang digunakan
untuk development atau
parameter fitting.

---

## 22.4 Test Set

Dataset yang digunakan
untuk mengevaluasi performance
pada data yang tidak digunakan
selama fitting.

---

## 22.5 Walk-Forward Analysis

Validation process yang
secara sequential melakukan:

```text
Train
  ↓
Test
  ↓
Move Forward
  ↓
Train
  ↓
Test
```

---

## 22.6 Robustness

Kemampuan strategy atau
result untuk tetap memiliki
characteristics yang reasonable
ketika assumptions atau
conditions berubah dalam
rentang yang masuk akal.

---

## 22.7 Sensitivity Analysis

Analysis terhadap perubahan
output akibat perubahan
parameter atau assumption.

---

## 22.8 Stress Test

Pengujian pada kondisi
yang lebih berat daripada
baseline.

Contoh:

```text
Higher Costs
Higher Slippage
Different RR
Different Market Period
```

---

# 23. Statistical Terms

---

## 23.1 Distribution

Pola penyebaran values
dalam sample.

---

## 23.2 Mean

Rata-rata arithmetic
dari observations.

---

## 23.3 Median

Nilai tengah setelah
observations diurutkan.

---

## 23.4 Variance

Ukuran penyebaran
observations terhadap mean.

---

## 23.5 Standard Deviation

Ukuran dispersion
dari observations.

---

## 23.6 Confidence Interval

Rentang estimasi yang
menggambarkan uncertainty
terhadap parameter yang
diestimasi berdasarkan
metode statistik tertentu.

---

## 23.7 Statistical Significance

Indikasi bahwa observed
effect relatif tidak mudah
dijelaskan hanya oleh
random variation menurut
statistical test tertentu.

Statistical significance
tidak sama dengan
economic significance.

---

## 23.8 Statistical Edge

Perbedaan antara expected
outcome strategy dan baseline/
random expectation yang
cukup konsisten untuk
dianggap meaningful
berdasarkan methodology
yang digunakan.

---

# 24. Research Integrity Terms

---

## 24.1 Reproducibility

Kemampuan menjalankan
experiment kembali dengan
input/configuration yang sama
dan mendapatkan result
yang sama atau equivalently
deterministic.

---

## 24.2 Repeatability

Kemampuan memperoleh
hasil konsisten ketika
experiment diulang dalam
kondisi yang sama.

---

## 24.3 Traceability

Kemampuan menelusuri
hasil kembali ke:

```text
Dataset
+
Configuration
+
Code Version
+
Experiment
```

---

## 24.4 Deterministic

Output ditentukan secara
konsisten oleh input dan
configuration yang sama.

---

## 24.5 Auditability

Kemampuan memeriksa bagaimana
sebuah result dihasilkan.

---

# 25. Software Architecture Terms

---

## 25.1 Module

Unit logical dalam system
yang memiliki responsibility
tertentu.

---

## 25.2 Component

Unit software yang memiliki
behavior/interface tertentu.

---

## 25.3 Interface

Contract yang mendefinisikan
bagaimana component berinteraksi.

---

## 25.4 Data Contract

Definition mengenai struktur,
semantics, dan validity
data yang dipertukarkan.

---

## 25.5 Domain Model

Representasi concepts dan
relationships yang relevan
dengan domain MRE.

---

## 25.6 Dependency

Relationship ketika satu
component membutuhkan
component lain.

---

## 25.7 Coupling

Degree of dependency antara
components.

---

## 25.8 Cohesion

Seberapa erat responsibility
dalam satu module saling
berhubungan.

---

## 25.9 Separation of Concerns

Prinsip memisahkan
responsibilities berbeda
ke dalam boundaries yang jelas.

---

# 26. Engine Terms

---

## 26.1 Data Engine

Component yang bertanggung
jawab terhadap loading,
validation, normalization,
dan access market data.

---

## 26.2 Indicator Layer

Layer yang menghasilkan
technical measurements
dari market data.

---

## 26.3 Event Engine

Component yang mendeteksi
market events.

---

## 26.4 Signal Engine

Component yang mengubah
events dan rules menjadi
research signals.

---

## 26.5 Simulation Engine

Component yang mensimulasikan
order, position, execution,
dan trade lifecycle.

---

## 26.6 Statistics Engine

Component yang menghitung
research metrics.

---

## 26.7 Reporting Engine

Component yang mengubah
experiment results menjadi
human-readable research output.

---

# 27. Backtesting Terms

---

## 27.1 Backtest

Simulation of a trading
strategy against historical
market data.

---

## 27.2 Backtest Engine

System component yang
menjalankan historical
strategy simulation.

---

## 27.3 Backtest Result

Output dari backtest,
termasuk trades dan metrics.

---

## 27.4 Trade Log

Record detail dari
individual simulated trades.

Minimum conceptual fields:

```text
entry
exit
direction
entry price
exit price
SL
TP
P&L
R
timestamp
```

---

## 27.5 Equity Curve

Sequence yang menunjukkan
perubahan simulated equity
sepanjang backtest.

---

# 28. Development Terms

---

## 28.1 Sprint

Time-bounded development
cycle dengan objective
tertentu.

---

## 28.2 Milestone

Major checkpoint dalam
roadmap.

---

## 28.3 Backlog

Kumpulan pekerjaan yang
belum selesai.

---

## 28.4 TODO

Actionable tasks yang
berasal dari roadmap,
requirements, research,
atau engineering needs.

---

## 28.5 Definition of Ready

Criteria yang harus dipenuhi
sebelum task siap dikerjakan.

---

## 28.6 Definition of Done

Criteria yang harus dipenuhi
sebelum task dianggap selesai.

---

## 28.7 Blocker

Condition yang mencegah
task dilanjutkan.

---

## 28.8 Technical Debt

Trade-off implementasi
yang membuat future change
menjadi lebih mahal atau
lebih sulit.

---

# 29. Documentation Terms

---

## 29.1 Document ID

Identifier unik untuk
sebuah document.

Contoh:

```text
FND-009
```

---

## 29.2 Foundation Document

Dokumen yang mendefinisikan
project governance,
context, vocabulary,
dan operating rules.

---

## 29.3 Product Document

Dokumen yang mendefinisikan
product requirements,
users,
workflow,
dan features.

---

## 29.4 Architecture Document

Dokumen yang menjelaskan
system structure,
boundaries,
interfaces,
dan technical decisions.

---

## 29.5 Research Document

Dokumen yang menjelaskan
hypothesis,
experiment,
methodology,
results,
dan conclusions.

---

## 29.6 Decision Log

Record keputusan penting
beserta alasan dan impact-nya.

---

# 30. Status Terms

---

## 30.1 PLANNED

Task sudah didefinisikan
tetapi belum siap dieksekusi.

---

## 30.2 READY

Task memiliki dependency
dan information yang cukup
untuk dimulai.

---

## 30.3 IN_PROGRESS

Task sedang aktif dikerjakan.

---

## 30.4 BLOCKED

Task tidak dapat dilanjutkan
karena dependency atau issue
tertentu.

---

## 30.5 REVIEW

Task telah dikerjakan dan
sedang diverifikasi.

---

## 30.6 DONE

Task memenuhi Definition
of Done.

---

## 30.7 DEFERRED

Task sengaja ditunda untuk
fase atau milestone berikutnya.

---

## 30.8 CANCELLED

Task tidak akan dilanjutkan.

---

# 31. Priority Terms

---

## 31.1 P0

Critical.

Jika tidak dikerjakan,
current milestone atau project
akan terblokir.

---

## 31.2 P1

High priority.

Penting untuk current
milestone atau core capability.

---

## 31.3 P2

Medium priority.

Berguna tetapi tidak
blocking.

---

## 31.4 P3

Low priority.

Future enhancement.

---

# 32. MRE Core Concepts

Conceptual hierarchy:

```text
Market Data
     ↓
Indicator
     ↓
Event
     ↓
Signal
     ↓
Order
     ↓
Execution
     ↓
Position
     ↓
Trade
     ↓
Statistics
     ↓
Evidence
     ↓
Research Knowledge
```

Ini merupakan salah satu
model konseptual terpenting
dalam MRE.

---

# 33. Conceptual Distinction

## Data

```text
What happened?
```

## Indicator

```text
What can we calculate?
```

## Event

```text
What happened that matters?
```

## Signal

```text
What condition has been detected?
```

## Order

```text
What should be simulated?
```

## Execution

```text
How was it filled?
```

## Trade

```text
What was the complete outcome?
```

## Statistics

```text
What does the sample show?
```

## Evidence

```text
What can we reasonably infer?
```

## Knowledge

```text
What have we learned?
```

---

# 34. Critical Distinctions

| Concept A                | Concept B             | Difference                                         |
| ------------------------ | --------------------- | -------------------------------------------------- |
| Signal                   | Trade                 | Signal ≠ execution                                 |
| Order                    | Trade                 | Order is instruction; trade is lifecycle           |
| Position                 | Trade                 | Position is exposure; trade is completed lifecycle |
| Backtest                 | Research              | Backtest is method; research is broader            |
| Result                   | Evidence              | Result requires interpretation                     |
| Win Rate                 | Expectancy            | Frequency ≠ payoff                                 |
| RR                       | Expectancy            | Payoff ratio ≠ expected outcome                    |
| Optimization             | Validation            | Optimization searches; validation tests            |
| In-Sample                | OOS                   | Development ≠ unseen evaluation                    |
| Statistical Significance | Economic Significance | Statistical ≠ practical value                      |
| Profit                   | Edge                  | Profit in sample ≠ durable edge                    |

---

# 35. Trading Strategy Research Vocabulary

For strategy research,
prefer:

```text
Strategy
Rule
Condition
Event
Signal
Entry
Exit
Execution
Trade
Result
Metric
Experiment
```

Avoid vague terms such as:

```text
Setup
Good Signal
Strong Market
Clean Chart
High Probability
Looks Good
```

unless explicitly defined.

---

# 36. "High Probability" Rule

The phrase:

> High Probability

must never be used as a
technical conclusion by itself.

Instead provide:

```text
Win Rate
Sample Size
Confidence Interval
Time Period
Market
Timeframe
Experiment Configuration
```

---

# 37. "Profitable Strategy" Rule

The phrase:

> Profitable Strategy

must be accompanied by:

- dataset;
- period;
- assumptions;
- transaction costs;
- sample size;
- metrics;
- validation methodology.

A strategy being profitable
in one backtest does not
automatically establish
a durable edge.

---

# 38. "Best RR" Rule

The phrase:

> Best RR

must specify:

```text
Best according to what?
```

Possible objectives:

```text
Expectancy
Profit Factor
Maximum Drawdown
Return
Risk-adjusted Return
```

Therefore MRE should prefer:

> **RR with highest measured objective
> under the defined experiment conditions.**

---

# 39. "Probability" Rule

Whenever probability is reported,
MRE should specify:

```text
Probability of What?
Based on Which Sample?
Under Which Conditions?
```

Example:

```text
Probability of winning a trade
based on 1,000 historical trades
under EXP-001 configuration.
```

---

# 40. "Edge" Rule

Edge should be treated as
a research hypothesis,
not an assumption.

Preferred wording:

```text
Observed Positive Expectancy
```

before claiming:

```text
Durable Statistical Edge
```

---

# 41. Naming Consistency

Preferred:

```text
trade_count
win_rate
expectancy
profit_factor
max_drawdown
entry_price
exit_price
```

Avoid inconsistent synonyms:

```text
number_of_trades
total_deals
winning_percentage
PF
DD_max
```

unless an external format
requires them.

---

# 42. Abbreviation Policy

Common abbreviations:

| Term                    | Abbreviation |
| ----------------------- | ------------ |
| Market Research Engine  | MRE          |
| Risk/Reward             | RR           |
| Stop Loss               | SL           |
| Take Profit             | TP           |
| Relative Strength Index | RSI          |
| Average True Range      | ATR          |
| Out-of-Sample           | OOS          |
| Profit Factor           | PF           |
| Maximum Drawdown        | MDD          |
| Return on Investment    | ROI          |

First occurrence in formal
documentation should generally
use full term followed by
abbreviation.

---

# 43. Unknown Terms

Jika sebuah term belum
memiliki definisi resmi:

```text
TERM STATUS = UNDEFINED
```

Jangan membuat multiple
competing definitions.

Tambahkan ke glossary
setelah definition disepakati.

---

# 44. Glossary Governance

Glossary dapat berubah ketika:

- domain model berubah;
- architecture memperkenalkan
  terminology baru;
- research methodology
  membutuhkan distinction baru;
- ambiguous terminology ditemukan.

---

# 45. Glossary Change Process

```text
New Term
   ↓
Need Identified
   ↓
Definition Proposed
   ↓
Review
   ↓
Accepted
   ↓
Added to Glossary
   ↓
References Updated
```

---

# 46. Breaking Terminology Change

Jika sebuah term sudah digunakan
secara luas tetapi definisinya
berubah secara material:

```text
Old Definition
      ↓
Impact Analysis
      ↓
Migration
      ↓
New Definition
```

Source code dan documentation
harus disinkronkan.

---

# 47. Glossary Quality Rules

Definitions harus:

- concise;
- unambiguous;
- domain-specific;
- testable where applicable;
- consistent;
- free from circular definitions.

Bad:

> Trade adalah transaksi trading.

Better:

> Trade adalah completed research
> transaction lifecycle dari entry
> hingga exit.

---

# 48. Glossary as Domain Contract

Glossary bukan sekadar
kamus dokumentasi.

Ia menjadi contract antara:

```text
Product
Architecture
Code
Research
Experiment
Reporting
```

Jika Product mengatakan:

```text
Signal
```

Architecture dan Code harus
memahami konsep yang sama.

---

# 49. Foundation Vocabulary

Setelah FND-009,
Foundation vocabulary utama MRE:

```text
Project
Product
Research
Experiment
Hypothesis
Dataset
Strategy
Indicator
Event
Signal
Order
Execution
Position
Trade
Risk
Reward
RR
R-Multiple
Probability
Win Rate
Expectancy
Profit Factor
Drawdown
Bias
Overfitting
OOS
Robustness
Reproducibility
Evidence
```

---

# 50. Glossary Completion Criteria

FND-009 dianggap complete
apabila:

- [x] Core project terms defined.
- [x] Market data terms defined.
- [x] Strategy terms defined.
- [x] Event terms defined.
- [x] Signal terms defined.
- [x] Execution terms defined.
- [x] Trade terms defined.
- [x] Risk/reward terms defined.
- [x] Probability terms defined.
- [x] Performance terms defined.
- [x] Bias terms defined.
- [x] Validation terms defined.
- [x] Statistical terms defined.
- [x] Architecture terms defined.
- [x] Engine terms defined.
- [x] Development terms defined.
- [x] Documentation terms defined.
- [x] Status terms defined.
- [x] Priority terms defined.
- [x] Critical distinctions documented.
- [x] Governance defined.

---

# 51. Foundation Completion

Dengan selesainya FND-009,
Foundation Document Set menjadi:

```text
FND-001  Project Charter
FND-002  Documentation Standard
FND-003  Document ID Standard
FND-004  Document Index
FND-005  Project Context
FND-006  Project Status
FND-007  Project Roadmap
FND-008  Project TODO
FND-009  Project Glossary
```

---

# 52. Foundation State

```text
╔══════════════════════════════════════╗
║       FOUNDATION STATUS              ║
╠══════════════════════════════════════╣
║ FND-001  ██████████ DONE             ║
║ FND-002  ██████████ DONE             ║
║ FND-003  ██████████ DONE             ║
║ FND-004  ██████████ DONE             ║
║ FND-005  ██████████ DONE             ║
║ FND-006  ██████████ DONE             ║
║ FND-007  ██████████ DONE             ║
║ FND-008  ██████████ DONE             ║
║ FND-009  ██████████ DONE             ║
╠══════════════════════════════════════╣
║ FOUNDATION: COMPLETE                 ║
╚══════════════════════════════════════╝
```

---

# 53. Transition to Product Phase

Setelah Foundation selesai,
project dapat berpindah dari:

```text
M0 — FOUNDATION
```

menuju:

```text
M1 — PRODUCT DEFINITION
```

Namun transition harus melewati:

```text
Foundation Review
```

---

# 54. Foundation Review Checklist

Sebelum Product Phase:

- [ ] Semua FND documents tersedia.
- [ ] Document index synchronized.
- [ ] Project status updated.
- [ ] Roadmap synchronized.
- [ ] TODO synchronized.
- [ ] Terminology consistent.
- [ ] No major contradictions.
- [ ] Repository structure correct.
- [ ] Git history clean enough for transition.
- [ ] Product phase objective clear.

---

# 55. Next Phase

Setelah Foundation Review:

```text
M1 — PRODUCT DEFINITION
```

Primary question:

> **What exactly are we building?**

---

# Appendix A — Quick Glossary

```text
MRE
Market Research Engine

RESEARCH
Systematic process for generating evidence.

HYPOTHESIS
Testable statement.

EXPERIMENT
Controlled procedure used to test a hypothesis.

DATASET
Collection of data used by an experiment.

STRATEGY
Deterministic set of trading rules.

INDICATOR
Mathematical measurement derived from market data.

EVENT
Detected occurrence.

SIGNAL
Strategy output representing a defined condition.

ORDER
Instruction to enter or exit.

EXECUTION
Process by which an order is considered filled.

POSITION
Active market exposure.

TRADE
Completed entry-to-exit lifecycle.

RR
Reward relative to risk.

R-MULTIPLE
Trade result normalized by initial risk.

WIN RATE
Percentage of winning trades.

EXPECTANCY
Expected average outcome per trade.

PROFIT FACTOR
Gross profit divided by absolute gross loss.

DRAWDOWN
Decline from an equity peak.

LOOKAHEAD BIAS
Use of information unavailable at decision time.

OVERFITTING
Excessive adaptation to historical sample.

OOS
Data not used during development/fitting.

ROBUSTNESS
Stability under reasonable changes in assumptions.

REPRODUCIBILITY
Ability to recreate equivalent results.

EDGE
Evidence-supported advantage relative to baseline.

EVIDENCE
Analyzed result supporting or rejecting a hypothesis.
```

---

# Appendix B — AI Resume Context

Jika project dilanjutkan pada
conversation baru:

```text
Market Research Engine (MRE)
Foundation Phase is complete.

Foundation documents:

FND-001 Project Charter
FND-002 Documentation Standard
FND-003 Document ID Standard
FND-004 Document Index
FND-005 Project Context
FND-006 Project Status
FND-007 Project Roadmap
FND-008 Project TODO
FND-009 Project Glossary

Current transition:
M0 Foundation → M1 Product Definition

Before starting Product:
perform Foundation Review.

Initial research case:
RSI Trendline Breakout.

Core MVP:
Historical CSV
→ Data Validation
→ Strategy
→ Signal
→ Simulation
→ Statistics
→ Report.

Primary research questions:
Probability
Risk/Reward
Expectancy
Robustness
Out-of-Sample validity.

Core principle:
Backtest is evidence generation,
not automatic proof of future profitability.

Next major work:
Product Definition / PRD.
```

---

**Document Status:** Active

**Document ID:** FND-009

**Version:** 1.0.0

**End of Document**
