"""Tests for coordinate parsing, weather parsing, and output formatting.

All HTTP calls are mocked; no network access is used.
"""

from unittest.mock import Mock, patch

import pytest
import requests

import weather_cli
from weather_cli import (
    CityNotFoundError,
    WeatherError,
    format_output,
    get_coordinates,
    get_weather,
    main,
    parse_coordinates,
    parse_weather,
)

GEOCODING_PAYLOAD = {
    "results": [
        {
            "name": "Algiers",
            "latitude": 36.752887,
            "longitude": 3.042048,
            "country": "Algeria",
        }
    ]
}

FORECAST_PAYLOAD = {
    "current_units": {"temperature_2m": "°C", "wind_speed_10m": "km/h"},
    "current": {"temperature_2m": 18.1, "wind_speed_10m": 3.7},
}


def mock_response(payload):
    response = Mock()
    response.json.return_value = payload
    response.raise_for_status.return_value = None
    return response


# --- coordinate parsing ---------------------------------------------------


def test_parse_coordinates_extracts_first_result():
    assert parse_coordinates(GEOCODING_PAYLOAD) == (
        36.752887,
        3.042048,
        "Algiers",
        "Algeria",
    )


def test_parse_coordinates_missing_results_raises_not_found():
    with pytest.raises(CityNotFoundError):
        parse_coordinates({})


def test_parse_coordinates_empty_results_raises_not_found():
    with pytest.raises(CityNotFoundError):
        parse_coordinates({"results": []})


def test_parse_coordinates_missing_latitude_raises_weather_error():
    payload = {"results": [{"name": "X", "longitude": 1.0}]}
    with pytest.raises(WeatherError):
        parse_coordinates(payload)


# --- weather parsing ------------------------------------------------------


def test_parse_weather_extracts_current_values():
    assert parse_weather(FORECAST_PAYLOAD) == (18.1, 3.7)


def test_parse_weather_missing_current_raises_weather_error():
    with pytest.raises(WeatherError):
        parse_weather({})


# --- output formatting ----------------------------------------------------


def test_format_output_with_country():
    assert format_output("Algiers", "Algeria", 18.1, 3.7) == (
        "Algiers, Algeria: 18.1 °C, wind 3.7 km/h"
    )


def test_format_output_without_country_and_rounding():
    assert format_output("Algiers", "", 18.14, 3.74) == (
        "Algiers: 18.1 °C, wind 3.7 km/h"
    )


# --- mocked HTTP ----------------------------------------------------------


@patch("weather_cli.requests.get")
def test_get_coordinates_uses_geocoding_endpoint_and_params(mock_get):
    mock_get.return_value = mock_response(GEOCODING_PAYLOAD)

    result = get_coordinates("Algiers")

    assert result == (36.752887, 3.042048, "Algiers", "Algeria")
    mock_get.assert_called_once_with(
        weather_cli.GEOCODING_URL,
        params={"name": "Algiers", "count": 1, "format": "json", "language": "en"},
        timeout=weather_cli.TIMEOUT,
    )


@patch("weather_cli.requests.get")
def test_get_coordinates_unknown_city(mock_get):
    mock_get.return_value = mock_response({})
    with pytest.raises(CityNotFoundError):
        get_coordinates("Notarealcity")


@patch("weather_cli.requests.get")
def test_get_coordinates_network_failure(mock_get):
    mock_get.side_effect = requests.ConnectionError("offline")
    with pytest.raises(WeatherError, match="network failure"):
        get_coordinates("Algiers")


@patch("weather_cli.requests.get")
def test_get_weather_uses_forecast_endpoint_and_params(mock_get):
    mock_get.return_value = mock_response(FORECAST_PAYLOAD)

    result = get_weather(36.752887, 3.042048)

    assert result == (18.1, 3.7)
    mock_get.assert_called_once_with(
        weather_cli.FORECAST_URL,
        params={
            "latitude": 36.752887,
            "longitude": 3.042048,
            "current": "temperature_2m,wind_speed_10m",
        },
        timeout=weather_cli.TIMEOUT,
    )


@patch("weather_cli.requests.get")
def test_get_weather_network_failure(mock_get):
    mock_get.side_effect = requests.Timeout("timed out")
    with pytest.raises(WeatherError, match="network failure"):
        get_weather(36.75, 3.04)


# --- CLI end to end (mocked HTTP) -----------------------------------------


@patch("weather_cli.requests.get")
def test_main_prints_formatted_output(mock_get, capsys):
    mock_get.side_effect = [
        mock_response(GEOCODING_PAYLOAD),
        mock_response(FORECAST_PAYLOAD),
    ]

    assert main(["Algiers"]) == 0
    assert capsys.readouterr().out == "Algiers, Algeria: 18.1 °C, wind 3.7 km/h\n"


@patch("weather_cli.requests.get")
def test_main_unknown_city_exits_1(mock_get, capsys):
    mock_get.return_value = mock_response({})

    assert main(["Notarealcity"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "unknown city" in captured.err


@patch("weather_cli.requests.get")
def test_main_network_failure_exits_1(mock_get, capsys):
    mock_get.side_effect = requests.ConnectionError("offline")

    assert main(["Algiers"]) == 1
    assert "network failure" in capsys.readouterr().err
