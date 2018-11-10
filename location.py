import requests

class Location:
    @staticmethod
    def locate():
        r = requests.post("https://location.services.mozilla.com/v1/geolocate?key=test")
        print("Found location "+str(r.text))
        loc = r.json()['location']
        r = requests.post("http://api.geonames.org/srtm1JSON?formatted=true&lat="+str(loc['lat'])+"&lng="+str(loc['lng'])+"&username=tcoupin&style=full")
        loc['alt'] = r.json()['srtm1']
        return loc

    @staticmethod
    def geocode(position, level="city"):
        
        if level == "country":
            loc = Location.find_country(position)
            if loc == "?":
                loc = Location.find_ocean(position)
            return loc
        else:
            return Location.find_city(position)

    @staticmethod
    def find_city(position):
        url="http://api.geonames.org/findNearbyPostalCodesJSON?lat="+str(position['lat'])+"&lng="+str(position['lng'])+"&username=tcoupin&maxRows=1"
        r = requests.get(url)
        print("FindCity "+str(position)+": "+url)
        print(r.text)
        if len(r.json()['postalCodes']) == 0:
            return "?"
        return r.json()['postalCodes'][0]['placeName']+" ("+r.json()['postalCodes'][0]['countryCode']+")"

        

    @staticmethod
    def find_country(position):
        url="http://api.geonames.org/countryCodeJSON?lat="+str(position['lat'])+"&lng="+str(position['lng'])+"&username=tcoupin"
        r = requests.get(url)
        print("FindCountry "+str(position)+": "+url)
        print(r.text)
        if r.json().has_key('countryName'):
            return r.json()['countryName']
        return "?"

    @staticmethod
    def find_ocean(position):
        url="http://api.geonames.org/oceanJSON?formatted=true&lat="+str(position['lat'])+"&lng="+str(position['lng'])+"&username=tcoupin&style=full"
        r = requests.get(url)
        print("FindOcean "+str(position)+": "+url)
        print(r.text)
        if r.json().has_key('ocean'):
            return r.json()['ocean']['name']
        return "?"