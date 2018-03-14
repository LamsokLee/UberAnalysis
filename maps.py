import gmaps
import gmaps.datasets
from config import *

gmaps.configure(api_key=API_Gmaps)


def writeCSV(list, filename):
    """Write the list to csv file."""
    with open(filename, "w") as file:
        for row in list:
            for i in range(len(row)):
                file.write(str(row[i]))
                if i != len(row) - 1:
                    file.write(",")
                else:
                    file.write("\n")
    return

