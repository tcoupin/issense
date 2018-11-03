import requests

class Location:
    @staticmethod
    def locate():
        r = requests.post("https://location.services.mozilla.com/v1/geolocate?key=test")
        return r.json()['location']

    @staticmethod
    def geocode(position):
        r = requests.get("https://nominatim.openstreetmap.org/reverse?format=json&lon="+str(position['lng'])+"&lat="+str(position['lat']))
        return r.json()['address']['city']+" ("+r.json()['address']['country']+")"