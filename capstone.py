from prefect import flow, task, get_run_logger
import httpx

@task
def fetch_weather(city):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude = city[1], longitude = city[2], hourly=["temperature_2m","cloudcover"]),
        )
    most_recent_temperature = float(weather.json()["hourly"]["temperature_2m"][0])
    most_recent_cloudcover = float(weather.json()["hourly"]["cloudcover"][0])
    logger = get_run_logger()
    logger.info(f"Most recent temp in {city[0]} {most_recent_temperature}C")
    logger.info(f"Most recent cloudcover in {city[0]} {most_recent_cloudcover}%")
    return most_recent_temperature


@flow
def weather_flow(cities=[["Vienna", 48.2092, 16.3728],["Athens", 37.9792, 23.7166],["Houston", 29.76, -95.36]]):
    fetch_weather.map(cities)

if __name__ == "__main__":
    weather_flow([["Vienna", 48.2092, 16.3728],["Athens", 37.9792, 23.7166],["Houston", 29.76, -95.36]])
