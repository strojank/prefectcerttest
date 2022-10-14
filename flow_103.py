from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd
import requests
from prefect.blocks.system import Secret


secret_block = Secret.load("alphavantage")

# Access the stored secret


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
@task
def get_data():
    KEY = secret_block.get()
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={KEY}'
    r = requests.get(url)
    data = r.json()
    logger = get_run_logger()
    logger.info("LOGGING is ON")
    return data


@flow
def main_flow():
    data = get_data()
    return data


if __name__ == "__main__":
    main_flow()
