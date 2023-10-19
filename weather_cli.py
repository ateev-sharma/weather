# weather_cli.py

import click
import requests

API_KEY = "507ae97f859e6a55d9be4d273919fa73"

'''
USAGE:
python weather_cli.py <city_name>
'''
def get_weather(city_name):
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={API_KEY}")
    response.raise_for_status()

    geodata = response.json()
    lat = geodata[0]['lat']
    lon = geodata[0]['lon']

    response = requests.get(f"http://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,windspeed_10m&hourly=temperature_2m,relativehumidity_2m,windspeed_10m")
    data = response.json()
    return {
        'city': geodata[0]['name'],
        'temperature': data['current']['temperature_2m'],
        'windspeed': data['current']['windspeed_10m'],
        'humidity': data['hourly']['relativehumidity_2m'][0]
    }

@click.command()
@click.argument('city_name')
def main(city_name):
    try:
        weather_info = get_weather(city_name)
        click.echo(f"Weather in {weather_info['city']}:\n")
        click.echo(f"Temperature: {weather_info['temperature']}°C")
        click.echo(f"Wind Speed: {weather_info['windspeed']}km/h")
        click.echo(f"Humidity: {weather_info['humidity']}%")
    except requests.RequestException:
        click.echo("Failed to fetch weather information. Please check your network connection or city name.")

if __name__ == "__main__":
    main()
