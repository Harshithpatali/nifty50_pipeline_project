# Nifty50 Pipeline Project

A **Stock Prediction Pipeline** for Nifty50 using **Apache Airflow** for task orchestration and **Streamlit** for visualization. This project automates data fetching, trains ML models, stores predictions, and displays them via a web dashboard.

---

## Folder Structure




---

## Features

- Automated **data fetching** and preprocessing with Airflow DAGs.
- Train ML models to **predict next-day Nifty50 close prices**.
- Store predictions and models in organized directories.
- **Streamlit dashboard** to visualize historical data and predictions.
- Fully **Dockerized** setup for Airflow and Streamlit.

---

## Prerequisites

- Docker & Docker Compose
- Python 3.10
- Airflow 2.10.2
- Streamlit

---

## Setup & Run (All-in-One)

1. **Clone the repository**

```bash
git clone https://github.com/Harshithpatali/nifty50_pipeline_project.git
cd nifty50_pipeline_project

docker compose run airflow-webserver airflow db init


docker compose run airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin


# Stop all containers
docker compose down

# Rebuild images
docker compose build

# Start services in detached mode
docker compose up -d

# View logs
docker compose logs -f



---

If you want, I can also **write a `.gitignore` ready to push**, optimized for Airflow, Streamlit, and Docker, so your GitHub repo stays clean.  

Do you want me to do that next?
