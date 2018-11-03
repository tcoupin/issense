import requests

class Stations:
    URL_TLE = "https://www.celestrak.com/NORAD/elements/stations.txt"
    def __init__(self):
        self.update();

    def update(self):
        r = requests.get(self.URL_TLE)
        self.__tles = {}
        self.__stations = []
        lines = []
        for line in r.text.splitlines():
            lines.append(line)
            if len(lines)==3:
                self.__tles[lines[0]]=(lines[1], lines[2])
                self.__stations.append(lines[0])
                lines = []
    
    def list(self):
        return self.__stations

    def getStation(self, station):
        return Station(station,self.__tles[station])

class Station:
    def __init__(self, name, tle):
        self.__name = name
        self.__tle = tle

    @property
    def name(self):
        return self.__name