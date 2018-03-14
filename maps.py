import gmaps
import gmaps.datasets
from config import *

gmaps.configure(api_key=API_Gmaps)

def writeCSV(list, filename, radius = 0.005):
    """Write the list to csv file."""
    with open(filename, "w") as file:
        for lines in list:
            if lines[-2] <= radius and lines[-1] <= radius:
                file.write(str(lines[2])+","+str(lines[3])+"\n")

    return