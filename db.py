import urllib
import xmltodict
from collections import defaultdict
from datetime import datetime

def get_plant_data() -> list:
    return [
        {'id': 'plant1',
         'moisture_level': 1,
        }
    ]

def get_indoor_data() -> list:
    return [
        {'id': 'living_room',
         'temperature': 1,
         'humidity': 3,
         'gas_level': 4
        }
    ]


def read_forecast_api_key():
    data = None
    with open('/home/pi/forecast_key') as f:
        data = f.readline()
    return data.strip()


def get_forecast_data() -> list:
    key = read_forecast_api_key()
    url = "http://data.fmi.fi/fmi-apikey/{}/wfs?request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::simple&place=jyvaskyla&timestep=180&parameters=temperature,Weathersymbol3,humidity,windspeedms".format(key)
    xml_data = urllib.request.urlopen(url).read()
    data = xmltodict.parse(xml_data)

    members = data['wfs:FeatureCollection']['wfs:member']
    result = defaultdict(list)

    for member in members:
        name = member['BsWfs:BsWfsElement']['BsWfs:ParameterName']
        value = member['BsWfs:BsWfsElement']['BsWfs:ParameterValue']
        time = member['BsWfs:BsWfsElement']['BsWfs:Time']

        result[name].append((time, value))

    return result
