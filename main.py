
from escpos import printer as escpos_printer
import datetime
import requests

# Printer configuration
printer_vendor_id = 0x1a86
printer_product_id = 0x7584
printer_profile = 'TM-T88IV'
printer_timeout = 3000

# Coordinates
latitude = 52.516667
longitude = 13.388889

# DarkSky API Key (https://darksky.net/dev)
key = ''

# Number of characters that fit into a row
paper_width = 43

# Request weather report
weather_response = requests.request('GET',
  'https://api.darksky.net/forecast/{}/{},{}?lang=en&units=si'.format(
    key, latitude, longitude))

if not weather_response.ok:
  print('DarkSky API responded with code', weather_response.status_code)
  exit()

# Request location data
location_response = requests.request('GET',
  'https://geocode.xyz/{},{}?geoit=json'.format(latitude, longitude))

if not location_response.ok:
  print('Geocode.xyz API responded with code', location_response.status_code)
  exit()

# Read API responses
weather = weather_response.json()
location = location_response.json()

# Configure printer
printer = escpos_printer.Dummy(profile=printer_profile)
printer.line_spacing(40)
printer.set(align='left')

# Compose header
# 03.01.2019 (13 chars) <- 19 (spaces) -> 12:00:00 (11 chars)
now = datetime.datetime.now()
printer.text('   ' + now.strftime('%d.%m.%Y') + (' ' * (paper_width - 13 - 11)) + now.strftime('%H:%M:%S'))
printer.text('\n\n\n')

# Location
printer.set(align='center', double_width=True, double_height=True)
printer.text('{}\n{}'.format(location['country'], location['city']))
printer.text('\n\n\n')

# Current weather condition icon
printer.set(align='center', double_width=False, double_height=False)
printer.image('icons/weather-' + weather['currently']['icon'] + '.png')

# Current temperature
printer.set(align='center', double_width=True, double_height=True)
temperature = weather['currently']['temperature']
printer.text('\n{:0.0f}°C\n'.format(temperature))
printer.set(align='center', double_width=False, double_height=False)
printer.text('\n')
printer.text('Feels like: {:0.0f}°C\n'.format(weather['currently']['apparentTemperature']))
printer.text(weather['currently']['summary'])
printer.text('\n\n\n')

# Daily report
days = weather['daily']['data']

# Remove today from daily forecast
del days[0]

# Print each day from the daily forecasts
for day in days:
  date = datetime.datetime.fromtimestamp(day['time'])
  icon = day['icon']
  temperature = day['temperatureHigh']
  printer.image('icons/weather-' + icon + '-small.png')
  printer.text('\n{} {:0.0f}°C\n'.format(date.strftime('%A'), temperature))
  printer.text('\n\n')

# Finish paper tape and cut
printer.text('\n\n\n')
printer.cut()

# Print
usb_printer = escpos_printer.Usb(
  printer_vendor_id,
  printer_product_id,
  profile=printer_profile,
  timeout=printer_timeout)
usb_printer._raw(printer.output)
