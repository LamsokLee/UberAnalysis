# Division,Line,Station Name,Station Latitude,Station Longitude,Route1,Route2,Route3,Route4,Route5,Route6,Route7,Route8,Route9,Route10,Route11,Entrance Type,Entry,Exit Only,Vending,Staffing,Staff Hours,ADA,ADA Notes,Free Crossover,North South Street,East West Street,Corner,Entrance Latitude,Entrance Longitude,Station Location,Entrance Location
import json


import requests

from config import *


# Store all the stations into list
def openStation(filename='data/subway.csv'):
    file = open(filename)
    file.next()
    stations = []  # Lat, Lng
    for line in file:
        temp = line.split(',')
        stations.append([float(temp[28]), float(temp[29]),temp[2]])
    return stations


def isNearby(Lat, Lng, stations, radius=0.005):
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


def stationFrequency(distanceData, radius = 0.005):
    from collections import Counter
    valid = []
    for trip in distanceData:
        if trip[7] <= radius and trip[8] <= radius:
            valid.append(trip[12] + ' to ' + trip[13])
    return Counter(valid).most_common(10)

def laziness(distanceData):
    import numpy as np
    import matplotlib.pyplot as plt
    hours = []
    for i in range(24):
        time = str(i).zfill(2) + ':00 - ' + str(i + 1).zfill(2) + ':00'
        hours.append(time)
    totalPUDistance = [0. for i in range(24)]
    countPUDistance = [0 for i in range(24)]
    for trip in distanceData:
        PUHour = trip[0].hour
        # DOHour = trip[1].hour
        if trip[7] < 0.1 and trip[8] < 0.1:
            totalPUDistance[PUHour] = totalPUDistance[PUHour] + trip[7] + trip[8]
            countPUDistance[PUHour] += 1
    res = []
    for i in range(24):
        res.append(totalPUDistance[i]/float(countPUDistance[i]))
    objects = tuple(hours) # x axis value
    y_pos = np.arange(len(objects)) # x axis names
    plt.bar(y_pos, res, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation=90)
    plt.ylabel('Avg Distance to Station')
    plt.title('Distance to Stations of all Taxi Trips')
    plt.show()