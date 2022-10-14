from prefect import flow, task
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
    #print(weather.json())
    return most_recent_temperature

@task
def save_weather(temp):
    with open("weather.csv", "w+") as w:
        w.write(str(temp))
    return "Wrote temp"


@flow
def weather_flow():
    fetch_weather("Vienna", 48.2092, 16.3728)
    fetch_weather("Athens", 37.9792, 23.7166)
    fetch_weather("Houston", 29.76, -95.36)

if __name__ == "__main__":
    weather_flow()
