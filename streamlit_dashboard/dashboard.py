import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(page_title="NIFTY50 Dashboard", layout="wide")
st.title("NIFTY50 Stock Prediction Dashboard")

# Fetch last 30 days of NIFTY50 data
end_date = datetime.today()
start_date = end_date - timedelta(days=30)
df = yf.download("^NSEI", start=start_date, end=end_date, interval="1d")

st.subheader("Last 30 Days Close Prices")
st.line_chart(df['Close'])

# Load next-day prediction
try:
    pred_df = pd.read_csv("../airflow_data/predictions/next_day_prediction.csv")
    next_day_close = pred_df['Next_Day_Close'].values[0]
    st.subheader("Next Day Predicted Close Price")
    st.metric(label="Predicted Close", value=f"{next_day_close:.2f}")
except FileNotFoundError:
    st.warning("Prediction file not found. Run the Airflow DAG first!")

if st.checkbox("Show Raw Data"):
    st.subheader("NIFTY50 Last 30 Days Data")
    st.dataframe(df)
