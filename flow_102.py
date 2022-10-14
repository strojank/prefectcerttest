from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd
import httpx
import yfinance as yf


@task(retries=1, retry_delay_seconds=10, cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=1))
def pull_data(ticker):
    df = yf.download(ticker)
    print(df.head())
    return df

@flow
def msft():
    data = pull_data("MSFT")
    return data

@flow
def google():
    data = pull_data("goog")
    return data

@flow
def main_flow():
    m_data = msft()
    g_data = google()
    return m_data, g_data

if __name__ == "__main__":
    main_flow()
