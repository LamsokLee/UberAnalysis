import json, requests, datetime

APIKey = 'AIzaSyDfm2e-u_gX1LWaZiLf_PrReCR51ddHpB8'


# Open yellow cab file
def openfile(filename):
    file = open(filename)
    data = []
    # length = len(file.readlines())
    count = 0
    # file = open(filename)
    file.next()
    file.next()
    for i in file:
        trip = i.split(',')
        # PUTime, DOTime, PULat, PULng, DOLat, DOLng, Distance
        data.append([trip[1], trip[2], trip[6], trip[5], trip[10], trip[9], trip[4]])
        count += 1
        # print str(float(count) / float(length) * 100) + '%'
        if count > 50000:
            break
    return data


def calDif(trip):
    URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + trip[2] + ',' + trip[
        3] + '&destinations=' + trip[4] + ',' + trip[5] + '&key=' + APIKey
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

data = openfile('data/yellow_tripdata_2014-04.csv')
for i in data:
    calDif(i)
    print i
