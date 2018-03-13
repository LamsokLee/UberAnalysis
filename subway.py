# Division,Line,Station Name,Station Latitude,Station Longitude,Route1,Route2,Route3,Route4,Route5,Route6,Route7,Route8,Route9,Route10,Route11,Entrance Type,Entry,Exit Only,Vending,Staffing,Staff Hours,ADA,ADA Notes,Free Crossover,North South Street,East West Street,Corner,Entrance Latitude,Entrance Longitude,Station Location,Entrance Location

# Store all the stations into list
file = open('data/subway.csv')
file.next()
stations = []  # Lat, Lng
for line in file:
    data = line.split(',')
    station = [float(data[28]), float(data[29])]
    stations.append(station)
stations.sort()


def matchRoute(Lat, Lng, radius = 50):
    leftLat = 40.575499
    rightLat = 40.903597
    midLat = (leftLat + rightLat) / 2
    while midLat != Lat:
        if Lat <= midLat:
            rightLat = midLat
        else:
            leftLat = midLat
        midLat = (leftLat + rightLat) / 2
