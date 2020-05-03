import logging

from abstractmenu import *

LOGGER = logging.getLogger("issense.stationchoice")

def MenuStationChoice(app):


    def select(station):
        def local(self):
            self.app.selectStation(station)
            return True
        return local

    list = []
    for station in app.stationList.list():
        list.append({
            "text": station,
            "function": select(station)
        })

    return AbstractMenu(app,list)

