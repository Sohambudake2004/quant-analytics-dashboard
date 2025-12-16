import streamlit as st
import pandas as pd
import numpy as np
import websocket
import json
import threading
from statsmodels.tsa.stattools import adfuller
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📈 Real-Time Quant Analytics Dashboard")

# =========================
# Sidebar Controls
# =========================
symbols = st.sidebar.multiselect(
    "Select Trading Pairs",
    ["btcusdt", "ethusdt", "bnbusdt"],
    default=["btcusdt", "ethusdt"]
)

timeframe = st.sidebar.selectbox("Resample Timeframe", ["1S", "1min", "5min"])
rolling_window = st.sidebar.slider("Rolling Window", 20, 200, 60)
z_threshold = st.sidebar.slider("Z-Score Alert Threshold", 1.0, 4.0, 2.0)

# =========================
# Global Data Store
# =========================
if "ticks" not in st.session_state:
    st.session_state.ticks = []

def on_message(ws, message):
    data = json.loads(message)
    st.session_state.ticks.append({
        "timestamp": pd.to_datetime(data["T"], unit="ms"),
        "symbol": data["s"].lower(),
        "price": float(data["p"]),
        "qty": float(data["q"])
    })

def start_socket(symbol):
    url = f"wss://fstream.binance.com/ws/{symbol}@trade"
    ws = websocket.WebSocketApp(url, on_message=on_message)
    ws.run_forever()

if "started" not in st.session_state:
    for sym in symbols:
        threading.Thread(target=start_socket, args=(sym,), daemon=True).start()
    st.session_state.started = True

# =========================
# Data Processing
# =========================
df = pd.DataFrame(st.session_state.ticks)

if df.empty or len(df) < 100:
    st.warning("⏳ Waiting for live market data...")
    st.stop()

df = df.set_index("timestamp")
prices = df.pivot_table(values="price", index=df.index, columns="symbol")
prices = prices.resample(timeframe).last().dropna()

if len(prices.columns) < 2:
    st.warning("⚠ Please select at least two symbols")
    st.stop()

x = prices.iloc[:, 0]
y = prices.iloc[:, 1]

# =========================
# Quant Analytics
# =========================
hedge_ratio = np.polyfit(x, y, 1)[0]
spread = y - hedge_ratio * x
zscore = (spread - spread.rolling(rolling_window).mean()) / spread.rolling(rolling_window).std()
correlation = x.rolling(rolling_window).corr(y)

adf_p_value = adfuller(spread.dropna())[1]

# =========================
# Alerts
# =========================
if abs(zscore.iloc[-1]) > z_threshold:
    st.error(f"🚨 ALERT: Z-Score breached → {zscore.iloc[-1]:.2f}")

# =========================
# Visualization
# =========================
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x.index, y=x, name=x.name))
    fig.add_trace(go.Scatter(x=y.index, y=y, name=y.name))
    fig.update_layout(title="Price Comparison")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=spread.index, y=spread, name="Spread"))
    fig.add_trace(go.Scatter(x=zscore.index, y=zscore, name="Z-Score"))
    fig.update_layout(title="Spread & Z-Score")
    st.plotly_chart(fig, use_container_width=True)

st.metric("Hedge Ratio", round(hedge_ratio, 4))
st.metric("ADF Test p-value", round(adf_p_value, 4))

# =========================
# Export
# =========================
export_df = pd.DataFrame({
    "spread": spread,
    "zscore": zscore,
    "correlation": correlation
}).dropna()

st.download_button(
    "⬇ Download Analytics CSV",
    export_df.to_csv(),
    "quant_analytics.csv"
)
