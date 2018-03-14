import json, requests, datetime

from math import sqrt

import gmaps
import numpy as np
from config import *
from subway import *

filename = 'data/yellow_tripdata_2014-04.csv'


# Open yellow cab file
def openfile(filename, limit=1000000):
    file = open(filename)
    data = []
    count = 0
    file.next()
    file.next()
    for i in file:
        trip = i.split(',')
        # PUTime, DOTime, PULat, PULng, DOLat, DOLng, Distance
        data.append([trip[1], trip[2], float(trip[6]), float(trip[5]), float(trip[10]), float(trip[9]), float(trip[4]),
                    -1., -1.])
        count += 1
        if count > limit:
            break
    return data


def lineDis(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def nearestSub(data, stations):
    for trip in data:
        minPU = lineDis(stations[0][0], stations[0][1], trip[2], trip[3])
        minDO = lineDis(stations[0][0], stations[0][1], trip[4], trip[5])
        for station in stations:
            curPUDis = lineDis(station[0], station[1], trip[2], trip[3])
            curDODis = lineDis(station[0], station[1], trip[4], trip[5])
            minPU = min(curPUDis, minPU)
            minDO = min(curDODis, minDO)
        trip[-2] = minPU
        trip[-1] = minDO
    return data

def plotData(distanceData,radius = 0.005):
    valid = []
    for trip in distanceData:
        if trip[-1] <= radius and trip[-2] <= radius:
            valid.append([trip[2],trip[3]])
    valid = np.array(valid)
    fig = gmaps.figure()
    fig.add_layer(gmaps.heatmap_layer(valid))
    return fig

def useSubway(data, radius):
    sum = 0
    for trip in data:
        if trip[-1] == 0. or trip[-1] > radius:  # haven't calculated or current in a higer range
            if isNearby(trip[2], trip[3], radius=radius) and isNearby(trip[4], trip[5], radius=radius):
                sum += 1
    return float(sum) / float(len(data))


def radiusStep(step=0.001, radius=0.005):
    curRadius = 0
    res = []
    while curRadius <= radius:
        print('Calculate radius = ' + str(curRadius))
        res.append([curRadius, useSubway(data, curRadius)])
        curRadius += step
    return res


def calDif(trip):
    # origins = Lat,Lng
    URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + trip[2] + ',' + trip[
        3] + '&destinations=' + trip[4] + ',' + trip[5] + '&key=' + API_Distance
    response = requests.get(URL)
    if response.status_code == 200:
        jsonfile = json.loads(response.content)
        if jsonfile['rows'][0]['elements'][0]['status'] != 'ZERO_RESULTS':
            estDis = jsonfile['rows'][0]['elements'][0]['distance']['value']  # in meter
            estTime = jsonfile['rows'][0]['elements'][0]['duration']['value']  # in seconds
            actDis = float(trip[6]) * 1609
            FMT = '%Y-%m-%d %H:%M:%S'
            actTime = (datetime.datetime.strptime(trip[1], FMT) - datetime.datetime.strptime(trip[0], FMT)).seconds
            timeDif = actTime - estTime
            disDif = actDis - estDis
            trip.append(timeDif)
            trip.append(disDif)


# else:
# Wait for secs

data = openfile('data/yellow_tripdata_2014-04.csv',10000)
stations = openStation(filename='data/subway.csv')
distanceData = nearestSub(data,stations)
fig = plotData(distanceData,radius = 0.005)