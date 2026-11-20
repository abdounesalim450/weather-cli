# weather-cli

**Current temperature and wind speed for any city, from your terminal — free, with no API key.**

```console
$ weather-cli Algiers
Algiers, Algeria: 16.8 °C, wind 1.8 km/h
```

![Terminal demo of weather-cli](assets/demo.gif)

`weather-cli` is a small, readable Python command-line tool (~120 lines) built
on the free [Open-Meteo](https://open-meteo.com/) APIs and the
[`requests`](https://requests.readthedocs.io/) library. Give it a city name and
it prints one script-friendly line with the current air temperature and wind
speed. No account, no API key, no tracking.

## Install

With [pipx](https://pipx.pypa.io/) (recommended — installs the command in an
isolated environment):

```sh
pipx install "git+https://github.com/abdounesalim450/weather-cli.git#subdirectory=weather-cli"
```

Then run it from anywhere:

```console
$ weather-cli Algiers
Algiers, Algeria: 16.8 °C, wind 1.8 km/h

$ weather-cli "New York"
New York, United States: 8.5 °C, wind 14.8 km/h
```

Sample outputs illustrate the format; values are live and will differ.
Requires Python 3.10+ and an internet connection.

From a local clone, either of these also works:

```sh
pipx install ./weather-cli
# or, for development:
cd weather-cli && uv sync --group dev && uv run python weather_cli.py Algiers
```

## Why not just `curl wttr.in`?

`wttr.in` is great for a full ASCII forecast. `weather-cli` is for the other
job: a **single, predictable line** you can drop into shell prompts, status
bars, and scripts — with an explicit city (no IP-based guessing of your
location), a 10-second timeout, clear errors on stderr, and offline tests.
It is also small enough to read in one sitting, which makes it a friendly
example of working with real APIs in Python.

## How it works

1. Geocode the city: `GET https://geocoding-api.open-meteo.com/v1/search?name=<city>&count=1`
2. Fetch current weather: `GET https://api.open-meteo.com/v1/forecast?latitude=…&longitude=…&current=temperature_2m,wind_speed_10m`
3. Print: `<City>, <Country>: <temperature> °C, wind <speed> km/h`

Unknown cities and network failures print an error to stderr and exit with
code 1. Full details are in the [tool README](weather-cli/README.md).

## Tests

All HTTP calls are mocked, so the suite runs offline:

```sh
cd weather-cli
uv run pytest   # 16 passed
```

## Repository layout

```
.
├── README.md          # this file
├── LICENSE            # MIT
├── assets/demo.gif    # terminal demo above
├── weather-cli/       # the installable package: code, tests, docs
│   ├── weather_cli.py
│   ├── pyproject.toml
│   ├── README.md
│   └── tests/
├── demo_requests.py   # small `requests` learning demo
└── demo_httpx.py      # small `httpx` learning demo
```

## Feedback

Issues and suggestions are welcome at
https://github.com/abdounesalim450/weather-cli/issues — especially ideas for
useful flags (units, forecast days, JSON output) that keep the tool simple.

## License

[MIT](LICENSE). Weather data from [Open-Meteo](https://open-meteo.com/);
location data based on [GeoNames](https://www.geonames.org/).
