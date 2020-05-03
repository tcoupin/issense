import datetime
from location import Location
from skyfield.api import Loader, utc, Topos
import logging

LOGGER = logging.getLogger("issense.station")

URL_TLE = "https://www.celestrak.com/NORAD/elements/stations.txt"
DATA_PATH = "./data"

def now():
    return datetime.datetime.now()

def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=utc)

class StationList:

    def __init__(self):
        self._loader = Loader(DATA_PATH)
        self.update()

    def update(self):
        self._tles = {}
        for es in self._loader.tle_file(URL_TLE, True):
            self._tles[es.name] = es
        self._ts = self._loader.timescale()
        self._stations = self._tles.keys()
        LOGGER.info("Update StationList, found "+str(len(self._stations))+" items")
    
    def list(self):
        return self._stations

    def getStation(self, station, from_position):
        return Station(self._tles[station],self._ts, from_position)

class Station:
    def __init__(self, sat, ts, from_position):
        self._sat = sat
        self._ts = ts
        self._last_transit_compute = None
        self.from_position = from_position


    @property
    def name(self):
        return self._sat.name

    @property
    def position(self):
        geographic_loc = self._sat.at(self._ts.now()).subpoint()
        
        pos = Location(geographic_loc.longitude.degrees,geographic_loc.latitude.degrees, geographic_loc.elevation.m)
  
        LOGGER.debug("Station ["+self.name+"] is at "+str(pos))
        return pos

    def next_transits(self, delay_minutes=1440):
        if self._last_transit_compute is None or (datetime.datetime.now()-self._last_transit_compute > datetime.timedelta(hours=6)):
            self._next_transits(delay_minutes)
        
        for transit in self._transits:
            LOGGER.debug(transit)

        return self._transits

    def _next_transits(self, delay_minutes):
        self._last_transit_compute = datetime.datetime.now()
        now = datetime.datetime.utcnow().replace(tzinfo=utc, second=0, microsecond=0)

        diff = self._sat - Topos(longitude_degrees=self.from_position.lng,latitude_degrees=self.from_position.lat, elevation_m=self.from_position.alt)
        was_visible = False
        visible = False
        self._transits = []
        tmp_transit = Transit()

        delta_m=-1
        while delta_m <= delay_minutes:
            delta_m += 1
            time = now + datetime.timedelta(minutes=delta_m)
            alt, az, distance = diff.at(self._ts.utc(time)).altaz()
            
            # Is above horrizon
            visible = alt.degrees > 0
            
            #if visible:
                # sun on iss ?

            
            if visible:
                if not was_visible:
                    tmp_transit.start = time
                was_visible = True
            else:
                if was_visible:
                    tmp_transit.end = time
                    self._transits.append(tmp_transit)
                    tmp_transit = Transit()
                    delta_m+=80 #minimum orbite duration = 1h24, so use 1h20
                    ## TODO determine minimum duration based on station altitude
                was_visible = False

        if tmp_transit.start is not None and tmp_transit is None:
            tmp_transit.end = tmp_transit.start
            self._transits.append(tmp_transit)
            
    
class Transit:

    def __init__(self):
        self._start = None
        self._end = None

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end
        
    @start.setter
    def set_start(self, time):
        self._start = time
    
    @end.setter
    def set_end(self, time):
        self._end = time
        
    def __str__(self):
        return "From "+self.start.strftime('%Y-%m-%d %H:%M %Z')+" to "+self.end.strftime('%Y-%m-%d %H:%M')
    
    
        
        
        
    
        
        
