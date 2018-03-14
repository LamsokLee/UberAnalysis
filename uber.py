import urllib2
import re
import time


# Read data for 2014
def readfile(filename):
    file = open(filename)
    data = []
    for i in file:
        if re.match('.+csv$', i):
            csv = urllib2.urlopen(i)
            print('Reading file for ' + csv.geturl()[-9:-4])
            next(csv)  # Skip the first line
            for j in csv:
                record = j.split(',')
                # record[0] = (time.strptime(record[0], '"%m/%d/%Y %H:%M:%S"'))
                # record[1] = float(record[1])
                # record[2] = float(record[2])
                data.append(time.strptime(record[0], '"%m/%d/%Y %H:%M:%S"'))
    # Time format: '"4/1/2014 0:11:00"'
    return data


# Read data for 2015

# # Sample: B02617,2015-05-17 09:47:00,B02617,141
# file = open('uber-raw-data-janjune-15.csv')
# file.next()
# for i in file:
#     data.append(time.strptime(i.split(',')[1],'%Y-%m-%d %H:%M:%S'))

def timeRange(data):
    mon = [[0 for i in range(24)] for i in range(12)]
    for i in data:
        month = i.tm_mon - 1
        hour = i.tm_hour
        mon[month][hour] += 1
    return mon


def monthRange(data):
    # [time.struct_time(tm_year=2014, tm_mon=4, tm_mday=1, tm_hour=0, tm_min=17, tm_sec=0, tm_wday=1, tm_yday=91, tm_isdst=-1), 40.7267, -74.0345, '"B02512"\n']
    res = [0 for i in range(12)]
    for i in data:
        res[i[0].tm_mon - 1] += 1
    return res


def dayPlot(month, mon):
    import numpy as np
    import matplotlib.pyplot as plt
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    hours = []
    for i in range(24):
        time = str(i).zfill(2) + ':00 - ' + str(i + 1).zfill(2) + ':00'
        hours.append(time)
    ydata = np.array(mon[month - 1])
    sum = 0
    for i in range(24):
        sum = sum + ydata[i]
    if sum != 0:
        percentage = [float(i) / float(sum) for i in ydata]
        objects = tuple(hours)
        y_pos = np.arange(len(objects))
        plt.bar(y_pos, percentage, align='center', alpha=0.5)
        plt.ylim(0, 0.09)
        plt.xticks(y_pos, objects, rotation=90)
        plt.ylabel('Numbers of Trips')
        plt.title('Trips Frequency by time in ' + months[month])
        plt.show()

d
data = readfile('raw_uber_data_urls.txt')
mon = timeRange(data)
for i in range(12):
    dayPlot(i, mon)
