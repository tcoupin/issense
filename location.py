import requests
import logging

LOGGER = logging.getLogger("issense.location")

def locate():
    r = requests.post("https://location.services.mozilla.com/v1/geolocate?key=test")
    LOGGER.debug("Locate response: "+r.text)
    loc = Location(r.json()['location']['lng'],r.json()['location']['lat'])
    r = requests.post("http://api.geonames.org/srtm1JSON?formatted=true&lat="+str(loc.lat)+"&lng="+str(loc.lng)+"&username=tcoupin&style=full")
    loc.alt = r.json()['srtm1']
    LOGGER.info("Found location "+str(loc))
    return loc

def geocode(loc, level="city"):    
    if level == "country":
        loc_str = _find_country(loc)
        if loc_str == None:
            loc_str = _find_ocean(loc)
        return loc_str
    else:
        return _find_city(loc)

def _find_city(loc):
    url="http://api.geonames.org/findNearbyPostalCodesJSON?lat="+str(loc.lat)+"&lng="+str(loc.lng)+"&username=tcoupin&maxRows=1"
    r = requests.get(url)
    LOGGER.debug("Find city ["+url+"]: "+r.text)
    if len(r.json()['postalCodes']) == 0:
        LOGGER.warning("No city found for location "+str(loc))
        return None
    city = r.json()['postalCodes'][0]['placeName']+" ("+r.json()['postalCodes'][0]['countryCode']+")"
    LOGGER.info("Found city '"+city+"' for location "+str(loc))
    return city

        

def _find_country(loc):
    url="http://api.geonames.org/countryCodeJSON?lat="+str(loc.lat)+"&lng="+str(loc.lng)+"&username=tcoupin"
    r = requests.get(url)
    LOGGER.debug("Find country ["+url+"]: "+r.text)
    if r.json().has_key('countryName'):
        LOGGER.info("Found country '"+r.json()['countryName']+"' for location "+str(loc))
        return r.json()['countryName']
    LOGGER.warning("No country found for location "+str(loc))
    return None

def _find_ocean(loc):
    url="http://api.geonames.org/oceanJSON?formatted=true&lat="+str(loc.lat)+"&lng="+str(loc.lng)+"&username=tcoupin&style=full"
    r = requests.get(url)
    LOGGER.debug("Find ocean ["+url+"]: "+r.text)
    if r.json().has_key('ocean'):
        LOGGER.info("Found ocean '"+r.json()['ocean']['name']+"' for location "+str(loc))
        return r.json()['ocean']['name']
    LOGGER.warning("No ocean found for location "+str(loc))
    return None

class Location:
    def __init__(self, lng, lat, alt=0):
        self.lng = lng
        self.lat = lat
        self.alt = alt
    
    @property
    def lng(self):
        return self.lng
    
    @property
    def lat(self):
        return self.lat
    
    @property
    def alt(self):
        return self.alt

    @lng.setter
    def lng(self, lng):
        self.lng = lng
    
    @lat.setter
    def lat(self, lat):
        self.lat = lat
    
    @alt.setter
    def alt(self, alt):
        self.alt = alt

    def __str__(self):
        return "Pos[lng:"+str(self.lng)+", lat:"+str(self.lat)+", alt:"+str(self.alt)+"]"
