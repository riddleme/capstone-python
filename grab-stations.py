import csv
import requests

from bs4 import BeautifulSoup
from io import StringIO

STN = 1
ST = -3
LAT = -2
LON = -1

def nwpm(direction):
	""" North West to Plus Minus. """
	heading = direction[-1]
	coordinate = direction[:-1]

	assert float(coordinate) >= 0
	if heading == 'N' or heading == 'E':
		return '+' + direction[:-1]

	if heading == 'S' or heading == 'W':
		return '-' + direction[:-1]

	raise Exception('Bad data: no heading found')

resp = requests.get('https://www.nws.noaa.gov/mdl/gfslamp/docs/stations_info.shtml')
soup = BeautifulSoup(resp.content, 'html.parser')

for element in soup.find_all('pre'):
	# Strip empty lines
	table = '\n'.join([line for line in element.text.splitlines() if line.strip()])

	f = StringIO(table)
	state = csv.reader(f, delimiter=' ', skipinitialspace=True)
	for station in state:
		if station[0] != '#CYC':  # Skip headers
			assert station[STN].isupper() == True

			if station[ST] == 'IL':
				print(station[STN], nwpm(station[LON]), nwpm(station[LAT]))
