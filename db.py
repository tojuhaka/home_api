import urllib
import xmltodict
import json
from collections import defaultdict
from datetime import datetime

weather_symbols = {
    "1.0": "selkeää",
    "2.0": "puolipilvistä",
    "21.0": "heikkoja sadekuuroja",
    "22.0": "sadekuuroja",
    "23.0": "voimakkaita sadekuuroja",
    "3.0": "pilvistä",
    "31.0": "heikkoa vesisadetta",
    "32.0": "vesisadetta",
    "33.0": "voimakasta vesisadetta",
    "41.0": "heikkoja lumikuuroja",
    "42.0": "lumikuuroja",
    "43.0": "voimakkaita lumikuuroja",
    "51.0": "heikkoa lumisadetta",
    "52.0": "lumisadetta",
    "53.0": "voimakasta lumisadetta",
    "61.0": "ukkoskuuroja",
    "62.0": "voimakkaita ukkoskuuroja",
    "64.0": "voimakasta ukkosta",
    "71.0": "heikkoja räntäkuuroja",
    "72.0": "räntäkuuroja",
    "73.0": "vomakkaita räntäkuuroja",
    "81.0": "heikkoa räntäsadetta",
    "82.0": "räntäsadetta",
    "83.0": "voimakasta räntäsadetta",
    "91.0": "utua",
    "92.0": "sumua"
}

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
        if name == "Weathersymbol3":
            value = weather_symbols[value]
        time = member['BsWfs:BsWfsElement']['BsWfs:Time']

        result[name].append((time, value))
    return result


def get_holdings():
    with open('/home/pi/holdings.json') as f:
        return json.load(f)

def get_spent_amount():
    with open('/home/pi/holdings.json') as f:
        return json.load(f)['spent_eur']

def filter_crypto(data, holding_amount):
    return {
        "id": data['id'],
        "amount": holding_amount * float(data['price_eur'])
    }

def get_crypto_data():
    url = "https://api.coinmarketcap.com/v1/ticker/?convert=EUR&limit=100"
    json_data = urllib.request.urlopen(url).read()
    data = json.loads(json_data)

    # filter out coin data based on holdings file
    holdings = get_holdings()
    return [filter_crypto(coin, holdings[coin['id']]) for coin in data if coin['id'] in holdings.keys()]
