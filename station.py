import requests
import ephem
import datetime
from math import degrees

class StationList:
    URL_TLE = "https://www.celestrak.com/NORAD/elements/stations.txt"
    def __init__(self):
        self.update();

    def update(self):
        print("Update StationList")
        r = requests.get(self.URL_TLE)
        self.__tles = {}
        self.__stations = []
        lines = []
        for line in r.text.splitlines():
            lines.append(line)
            if len(lines)==3:
                name = str(lines[0]).strip()
                self.__tles[name]=(lines[1], lines[2])
                self.__stations.append(name)
                lines = []
        print("Found "+str(len(self.__stations))+" items")
    
    def list(self):
        return self.__stations

    def getStation(self, station):
        return Station(station,self.__tles[station])

class Station:
    def __init__(self, name, tle):
        self.__name = name
        self.__ephem = ephem.readtle(str(name), str(tle[0]), str(tle[1]))

    @property
    def name(self):
        return self.__name

    @property
    def position(self):
        now = datetime.datetime.utcnow()
        self.__ephem.compute(now)
        pos = {"lng": degrees(self.__ephem.sublong), "lat": degrees(self.__ephem.sublat)}
        print("Station ["+self.__name+"], Position["+str(pos)+"]")
        return pos

    @property
    def next_position(self):
        return {}