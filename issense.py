#!/usr/bin/python

import time
import datetime
from display import *
from location import *
from station import *
import signal
        
darkblue = [0,0,200]

sense = Display()
sense.load_image("iss.png")

# Loads
position = Location.locate()
position_str = Location.geocode(position)
stationList = StationList()
station = stationList.getStation(stationList.list()[0])

sense.clear()

# Display
sense.show_message(datetime.datetime.now().strftime('Now: %Y-%m-%d %H:%M'),0.06,darkblue)
sense.show_message("Pos: "+position_str,0.06,darkblue)
sense.show_message("Station: "+station.name,0.06,darkblue)
sense.show_message("Over: "+Location.geocode(station.position,"country"),0.06,darkblue)

# Next transit date

# Menu
## next transit
## current position
## config
### select station
### view pos
### local time

sense.stop()
