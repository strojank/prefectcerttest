from prefect import flow, task, get_run_logger
import httpx

@task
def fetch_weather(city, lat, lon):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude = lat, longitude = lon, hourly=["temperature_2m","cloudcover"]),
        )
    most_recent_temperature = float(weather.json()["hourly"]["temperature_2m"][0])
    most_recent_cloudcover = float(weather.json()["hourly"]["cloudcover"][0])
    print(f"Most recent temp in {city} {most_recent_temperature}C")
    print(f"Most recent cloudcover in {city} {most_recent_cloudcover}%")
    logger = get_run_logger()
    logger.info("LOGGING is ON")
    return most_recent_temperature

@task
def print_nums(nums):
    for n in nums:
        print(n)

@task
def times_two(num):
    return num * 2


@flow
def weather_flow(nums):
    print_nums(nums)
    fetch_weather("Vienna", 48.2092, 16.3728)
    fetch_weather("Athens", 37.9792, 23.7166)
    fetch_weather("Houston", 29.76, -95.36)
    doubles = times_two.map(nums)
    print_nums(doubles)
    return doubles

if __name__ == "__main__":
    weather_flow([4,5,7])
