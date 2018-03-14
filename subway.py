# Division,Line,Station Name,Station Latitude,Station Longitude,Route1,Route2,Route3,Route4,Route5,Route6,Route7,Route8,Route9,Route10,Route11,Entrance Type,Entry,Exit Only,Vending,Staffing,Staff Hours,ADA,ADA Notes,Free Crossover,North South Street,East West Street,Corner,Entrance Latitude,Entrance Longitude,Station Location,Entrance Location
import json
import requests

from config import *

# Store all the stations into list
file = open('data/subway.csv')
file.next()
stations = []  # Lat, Lng
for line in file:
    data = line.split(',')
    stations.append([float(data[28]), float(data[29])])
stations.sort()


def isNearby(Lat, Lng, radius=0.005):
    LatRange = (Lat - radius, Lat + radius)
    LngRange = (Lng - radius, Lng + radius)
    for station in stations:
        if station[0] >= LatRange[0] and station[0] <= LatRange[1] and station[1] >= LngRange[0] and station[1] <= \
                LngRange[1]:
            return True
    return False


def calDirection(fromLoc, toLoc, mode='walking', units='metric'):
    URL = 'https://maps.googleapis.com/maps/api/directions/json?units=' + units + '&mode=' + mode + '&origin=' + str(
        fromLoc[0]) + ',' + str(fromLoc[1]) + '&destination=' + str(toLoc[0]) + ',' + str(
        toLoc[1]) + '&key=' + API_Direction
    response = requests.get(URL)
    if response.status_code == 200:
        jsonfile = json.loads(response.content)
        if jsonfile['rows'][0]['elements'][0]['status'] == 'OK':
            estDis = jsonfile['rows'][0]['elements'][0]['distance']['value']  # in meter
            # estTime = jsonfile['rows'][0]['elements'][0]['duration']['value']  # in seconds
    return estDis


def calDis(fromLoc, toLoc, mode='walking', units='metric'):
    URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=' + units + '&mode=' + mode + '&origins=' + str(
        fromLoc[0]) + ',' + str(fromLoc[1]) + '&destinations=' + str(toLoc[0]) + ',' + str(
        toLoc[1]) + '&key=' + API_Distance
    response = requests.get(URL)
    if response.status_code == 200:
        jsonfile = json.loads(response.content)
        if jsonfile['rows'][0]['elements'][0]['status'] == 'OK':
            estDis = jsonfile['rows'][0]['elements'][0]['distance']['value']  # in meter
            # estTime = jsonfile['rows'][0]['elements'][0]['duration']['value']  # in seconds
    return estDis
