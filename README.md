# Real-Time Quant Analytics Dashboard

## Overview
This project is a real-time quantitative analytics prototype designed to demonstrate an end-to-end
data pipeline from live market data ingestion to statistical analysis and interactive visualization.
It is intended as a research and monitoring tool for quantitative trading use cases such as
statistical arbitrage, pair analysis, and market microstructure observation.

The system ingests live tick-level trade data from Binance via WebSocket, processes and resamples
the data into configurable timeframes, computes key statistical metrics, and presents them through
an interactive dashboard.

---

## Key Features
- Live WebSocket-based ingestion of tick-level trade data
- Multi-timeframe resampling (1 second, 1 minute, 5 minutes)
- Ordinary Least Squares (OLS) hedge ratio estimation
- Spread calculation for pair analysis
- Rolling Z-score for mean-reversion detection
- Rolling correlation analysis
- Augmented Dickey-Fuller (ADF) test for stationarity
- Real-time alerting based on Z-score thresholds
- Interactive charts with zoom, pan, and hover support
- Export of processed analytics data to CSV

---

## System Architecture
The application is structured as a modular pipeline with clear separation of concerns:

1. **Data Ingestion**  
   A background WebSocket client subscribes to Binance trade streams and continuously receives
   tick-level data without blocking the UI.

2. **Data Storage & Resampling**  
   Incoming ticks are stored in-memory using Pandas and resampled into user-selected timeframes
   to reduce noise and align with trading analytics.

3. **Analytics Engine**  
   Statistical computations such as hedge ratio estimation, spread construction, Z-score
   normalization, correlation, and stationarity testing are performed on the resampled data.

4. **Visualization & Alerts**  
   A Streamlit-based frontend renders interactive visualizations and surfaces real-time alerts
   when predefined statistical thresholds are breached.

This modular design allows new data sources, analytics, or visualization components to be added
with minimal changes to the existing codebase.

---

## Technologies Used
- **Python** – Core application logic
- **Streamlit** – Interactive frontend and application runner
- **Pandas & NumPy** – Data manipulation and numerical computation
- **Statsmodels** – Statistical testing (ADF test)
- **Plotly** – Interactive visualizations
- **Binance WebSocket API** – Live market data source

---

## How to Run Locally

### 1. Install dependencies

pip install -r requirements.txt
