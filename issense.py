#!/usr/bin/python

import os
import logging
import sys

logger = logging.getLogger("issense")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)



import time
from display import *
import location
from station import *
import signal
from menu import *
        
DARKBLUE = [0,0,200]
SPEED = 0.05

logger.info("starting")

class App:
    def __init__(self,sense):
        self.sense = sense
        self.sense.load_image("iss.png")
        self.position = location.locate()
        self.position_str = location.geocode(self.position)
        self.stationList = StationList()
        self.station = self.stationList.getStation('ISS (ZARYA)', self.position)
        self.station.next_transits()
        #self.printAll()
        self.menu = Menu0(self)
        self.menu.start()
        self.menu.join()


    def stop(self):
        self.sense.show_message('Byebye', SPEED, DARKBLUE)
        self.sense.stop()
        sys.exit(0)

    def printAll(self):
        self.clear()
        self.printDate()
        self.printLoc()
        self.printStation()
        self.printStationLoc()
        self.printNextTransit()
        
    def clear(self):
        self.sense.clear()

    def printDate(self):
        date_str = now().strftime('%Y-%m-%d %H:%M')
        self.sense.show_message("Date: "+date_str,SPEED,DARKBLUE)

    def printLoc(self):
        self.sense.show_message("Loc: "+self.position_str,SPEED,DARKBLUE)

    def printStation(self):
        self.sense.show_message("Station: "+self.station.name,SPEED,DARKBLUE)

    def printStationLoc(self):
        self.sense.show_message("Is over: "+location.geocode(self.station.position,"country"),SPEED,DARKBLUE)

    def printNextTransit(self):
        next = (self.station.next_transits()[0].start - utcnow())
        self.sense.show_message("Next transit in "+str(next.seconds//3600)+"h"+str((next.seconds//60)%60)+"min"+str(next.seconds%60)+"s",SPEED,DARKBLUE)


def main():
    app = App(Display())
    app.stop()

# Menu
## next transit
## current position
## config
### select station
### view pos
### local time


if __name__ == "__main__":
    main()