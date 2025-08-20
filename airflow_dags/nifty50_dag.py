from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import os

DATA_DIR = '/opt/airflow/airflow_data'
MODEL_DIR = '/opt/airflow/airflow_models'
PRED_DIR = '/opt/airflow/airflow_data/predictions'

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(PRED_DIR, exist_ok=True)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'nifty50_prediction',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

def fetch_data():
    df = yf.download("^NSEI", period="1y", interval="1d")
    df.to_csv(f"{DATA_DIR}/nifty50.csv")
    print("Data fetched!")

def preprocess():
    df = pd.read_csv(f"{DATA_DIR}/nifty50.csv")
    df['Prev_Close'] = df['Close'].shift(1)
    df.dropna(inplace=True)
    df.to_csv(f"{DATA_DIR}/nifty50_processed.csv", index=False)
    print("Data preprocessed!")

def train_model():
    df = pd.read_csv(f"{DATA_DIR}/nifty50_processed.csv")
    X = df[['Prev_Close']]
    y = df['Close']
    model = LinearRegression()
    model.fit(X, y)
    import joblib
    joblib.dump(model, f"{MODEL_DIR}/nifty50_model.pkl")
    print("Model trained!")

def predict():
    df = pd.read_csv(f"{DATA_DIR}/nifty50_processed.csv")
    import joblib
    model = joblib.load(f"{MODEL_DIR}/nifty50_model.pkl")
    last_close = df['Close'].iloc[-1]
    next_day_pred = model.predict([[last_close]])
    pred_df = pd.DataFrame({'Next_Day_Close': next_day_pred})
    pred_df.to_csv(f"{PRED_DIR}/next_day_prediction.csv", index=False)
    print("Prediction saved!")

t1 = PythonOperator(task_id='fetch_data', python_callable=fetch_data, dag=dag)
t2 = PythonOperator(task_id='preprocess', python_callable=preprocess, dag=dag)
t3 = PythonOperator(task_id='train_model', python_callable=train_model, dag=dag)
t4 = PythonOperator(task_id='predict', python_callable=predict, dag=dag)

t1 >> t2 >> t3 >> t4
