# weather-cli

A small Python command-line tool that prints the **current temperature and
wind speed for a city**, using the free [Open-Meteo](https://open-meteo.com/)
APIs. No API key or account is required.

Example:

```console
$ python weather_cli.py Algiers
Algiers, Algeria: 17.0 °C, wind 1.6 km/h
```

The values are live weather data, so your output will differ depending on
when and where you run the tool.

## Purpose

`weather-cli` answers one question from the terminal — "what is the weather
like in this city right now?" — without opening a browser or signing up for
a weather service. You give it a city name, and it prints a single line with
the current air temperature (at 2 m above ground) and wind speed (at 10 m
above ground) for that city.

## How it works

1. **Geocoding** — the city name is sent to the Open-Meteo Geocoding API to
   find its latitude and longitude:

   ```
   GET https://geocoding-api.open-meteo.com/v1/search
       ?name=<city>&count=1&format=json&language=en
   ```

   The first matching result is used, including its display name and country.

2. **Forecast** — those coordinates are sent to the Open-Meteo Forecast API
   to get the current conditions:

   ```
   GET https://api.open-meteo.com/v1/forecast
       ?latitude=<lat>&longitude=<lon>&current=temperature_2m,wind_speed_10m
   ```

3. **Output** — the `temperature_2m` and `wind_speed_10m` values from the
   response are printed in this format:

   ```
   <City>, <Country>: <temperature> °C, wind <wind speed> km/h
   ```

Both API calls use the [`requests`](https://requests.readthedocs.io/)
library with a 10-second timeout. Units are fixed to degrees Celsius (°C)
for temperature and kilometres per hour (km/h) for wind speed, and values
are shown with one decimal place.

## Requirements

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/) (used below to create the project
  environment and install dependencies)
- An internet connection (for real runs; the tests run offline)

The only runtime dependency is `requests`; `pytest` is installed as a
development dependency for the tests. Both are declared in
[`pyproject.toml`](pyproject.toml).

## Installation

From the directory containing this README:

```sh
cd weather-cli
uv venv
uv sync --group dev
```

This creates a virtual environment in `weather-cli/.venv` and installs the
tool and its dependencies into it.

## Usage

```sh
uv run python weather_cli.py <city>
```

Or, with the virtual environment activated, use the installed
`weather-cli` command:

```sh
source .venv/bin/activate
weather-cli <city>
```

### Examples

Sample outputs below illustrate the format; actual values are live and will
differ.

```console
$ uv run python weather_cli.py Algiers
Algiers, Algeria: 17.0 °C, wind 1.6 km/h

$ uv run python weather_cli.py Paris
Paris, France: 11.2 °C, wind 9.4 km/h

$ uv run python weather_cli.py "New York"
New York, United States: 8.5 °C, wind 14.8 km/h
```

City names with spaces can be quoted (`"New York"`) or typed as separate
words (`New York`); both work. To narrow down a common name, add a country
after a comma, for example `"Paris, France"`.

Show the built-in help with:

```sh
uv run python weather_cli.py --help
```

## Errors and exit codes

Errors are printed to standard error (stderr), never mixed into the normal
output, and the tool exits with a non-zero code:

| Situation | Example message | Exit code |
|---|---|---|
| Unknown city | `Error: unknown city 'Notarealcity'` | 1 |
| Network failure (offline, timeout, HTTP error) | `Error: network failure while looking up 'Algiers': ...` | 1 |
| No city argument given | usage message from the argument parser | 2 |

A successful run prints one line to stdout and exits with code 0.

## Running the tests

The test suite covers coordinate parsing, weather parsing, and output
formatting. All HTTP calls are mocked, so the tests need no network access.

```sh
uv run pytest
```

Expected result: `16 passed`.

## Project structure

```
weather-cli/
├── weather_cli.py            # the CLI tool (single module)
├── pyproject.toml            # project metadata and dependencies
├── conftest.py               # makes weather_cli importable in tests
├── tests/
│   └── test_weather_cli.py   # pytest tests with mocked HTTP calls
└── README.md                 # this file
```

## Notes and limitations

- Only the first geocoding result is used, so an ambiguous name resolves to
  Open-Meteo's top match; add a country qualifier (e.g. `"Paris, France"`)
  to disambiguate.
- Units are fixed: °C for temperature and km/h for wind speed.
- Weather values come from Open-Meteo's forecast models, not from a weather
  station in the city, so they are an estimate for the area.
- Data sources: [Open-Meteo](https://open-meteo.com/) (weather) and
  [GeoNames](https://www.geonames.org/) (location names, via the geocoding
  API).
