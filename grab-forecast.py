import csv
import re
import requests
import sys

from io import StringIO

resp = requests.get('https://www.nws.noaa.gov/mdl/gfslamp/bull/lavlamp.txt')
stations = re.sub('\n +\n', '\n\n', resp.text).split('\n\n')[1:]
temp = {}

for station_data in stations:
	if station_data != '':
		data = [line.split() for line in station_data.splitlines()]
		station = data[0][0]
		temperature = data[2][1]

	if data[2][0] !='TMP':
		continue

	temp[station] = temperature

for station in sys.stdin:
	stn, lon, lat = station.split()

	try:
		print(stn, lon, lat, temp[stn])
	except KeyError as e:
		print(f'No temperature data found for station {e}!', file=sys.stderr)
