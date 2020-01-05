
# pos-weather-printer

Given the coordinates of a geographical location this script fetches the current weather forecast from the [Dark Sky API](https://darksky.net/dev) and prints it using via the ESC/POS protocol onto thermal paper. It has been developed in a coding session by Jessie and Fränz in January 2020. We are using the [Climacons](http://adamwhitcroft.com/climacons/) icon set to show weather conditions.

## Prerequisites

- Epson TM-T88IV ESC/POS printer
- Raspberry Pi (connected to the printer via USB)
- Python & Pip

## Setup

- Create a [Dark Sky account](https://darksky.net/dev) to retrieve an API key.
- Configure constants at the top of `main.py`.
- Install Python dependencies: `pip install requests python-escpos`
