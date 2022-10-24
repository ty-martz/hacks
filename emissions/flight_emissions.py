import requests
import pandas as pd
import math
from config import APIInfo


def api_fetch_airport_data(api_key=APIInfo.MY_KEY):

    call = f'https://airlabs.co/api/v9/airports?api_key={api_key}'
    api_result = requests.get(call)
    api_response = api_result.json()
    df = pd.json_normalize(api_response)
    airports = df[['iata_code', 'lat', 'lng']]

    return airports


def deg_to_rad(deg):

    return deg*(math.pi/180)


def calculate_distance(origin, destination):
    '''
    parameters
        origin: iata code of departure airport
        destination: iata code of arrival airport
    returns distance in miles between coordinates
    '''
    print('Calculating Aiport Distance...')
    # load airport data
    try:
        print('Pulling Airport data from API')
        airp = api_fetch_airport_data()
    except:
        print('API call failed, reverting to local airport data')
        airports = pd.read_csv('../emissions/airports.csv')
        airp = airports[['iata_code', 'latitude_deg', 'longitude_deg']]
        airp.columns = ['iata_code', 'lat', 'lng']
        airp = airp.dropna(axis=0)

    # using airports get the lat/long from iata_codes
    from_airp = tuple(airp[airp['iata_code'] == origin][['lat', 'lng']].values[0])
    to_airp = tuple(airp[airp['iata_code'] == destination][['lat', 'lng']].values[0])

    #distance calculation according to Haversine formula
    R = 6371 # radius of Earth in miles
    dis_lat = deg_to_rad(to_airp[0] - from_airp[0])
    dis_lon = deg_to_rad(to_airp[1] - from_airp[1])
    a = math.sin(dis_lat/2)**2 + math.cos(deg_to_rad(from_airp[0]) * math.cos(deg_to_rad(to_airp[0]))) * math.sin(dis_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    d = R * c
    return d


def calculate_emissions(origin, destination, round_trip=True, radiative_forcing=True,
                        num_passengers=1.0, tonnes_per_pax=0.35):
    print(f'Calculating Emissions from Flight: {origin} --> {destination} ...')
    # variables
    distance = calculate_distance(origin, destination)
    lbs_to_metr_tons=1/2204.62
    rf_factor = 1.0
    two_way = 1.0

    if radiative_forcing:
        rf_factor = 1.981
    if round_trip:
        two_way = 2.0

    return round(distance * float(num_passengers) * tonnes_per_pax * lbs_to_metr_tons * rf_factor * two_way, 2)

