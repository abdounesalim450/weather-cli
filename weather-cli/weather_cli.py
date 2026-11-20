"""Print current temperature and wind speed for a city via Open-Meteo.

Endpoints confirmed from the Open-Meteo docs:
- Geocoding: https://geocoding-api.open-meteo.com/v1/search
  params: name (required), count, format, language
  returns: {"results": [{"name", "latitude", "longitude", "country", ...}]}
- Forecast: https://api.open-meteo.com/v1/forecast
  params: latitude, longitude (required), current (string array)
  with current=temperature_2m,wind_speed_10m
  returns: {"current": {"temperature_2m": ..., "wind_speed_10m": ...},
            "current_units": {"temperature_2m": "°C", "wind_speed_10m": "km/h"}}
"""

import argparse
import sys

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 10


class CityNotFoundError(Exception):
    """Raised when the geocoding API returns no matching location."""


class WeatherError(Exception):
    """Raised when weather data cannot be retrieved or parsed."""


def parse_coordinates(payload):
    """Extract (latitude, longitude, name, country) from a geocoding payload."""
    results = payload.get("results") if isinstance(payload, dict) else None
    if not results:
        raise CityNotFoundError("city not found")
    first = results[0]
    try:
        latitude = float(first["latitude"])
        longitude = float(first["longitude"])
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherError("invalid coordinates in geocoding response") from exc
    name = first.get("name", "")
    country = first.get("country", "")
    return latitude, longitude, name, country


def parse_weather(payload):
    """Extract (temperature_c, wind_speed_kmh) from a forecast payload."""
    try:
        current = payload["current"]
        temperature = float(current["temperature_2m"])
        wind_speed = float(current["wind_speed_10m"])
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherError("invalid weather data in forecast response") from exc
    return temperature, wind_speed


def format_output(name, country, temperature, wind_speed):
    """Format the one-line result shown to the user."""
    location = f"{name}, {country}" if country else name
    return f"{location}: {temperature:.1f} °C, wind {wind_speed:.1f} km/h"


def get_coordinates(city):
    """Look up coordinates for *city* via the geocoding API."""
    params = {"name": city, "count": 1, "format": "json", "language": "en"}
    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise WeatherError(f"network failure while looking up '{city}': {exc}") from exc
    except ValueError as exc:
        raise WeatherError("invalid JSON from geocoding API") from exc
    return parse_coordinates(payload)


def get_weather(latitude, longitude):
    """Fetch current temperature and wind speed for the coordinates."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
    }
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise WeatherError(f"network failure while fetching weather: {exc}") from exc
    except ValueError as exc:
        raise WeatherError("invalid JSON from forecast API") from exc
    return parse_weather(payload)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="weather-cli",
        description="Print current temperature and wind speed for a city (Open-Meteo).",
    )
    parser.add_argument("city", nargs="+", help="City name, e.g. Algiers or 'New York'")
    args = parser.parse_args(argv)
    city = " ".join(args.city).strip()

    try:
        latitude, longitude, name, country = get_coordinates(city)
        temperature, wind_speed = get_weather(latitude, longitude)
    except CityNotFoundError:
        print(f"Error: unknown city '{city}'", file=sys.stderr)
        return 1
    except WeatherError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(format_output(name or city, country, temperature, wind_speed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
