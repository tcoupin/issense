#!/usr/bin/python
#from sense_hat import SenseHat
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
stations = Stations()
station = stations.getStation(stations.list()[0])

sense.clear()

# Display
sense.show_message(datetime.datetime.now().strftime('Now: %Y-%m-%d %H:%M'),0.06,darkblue)
sense.show_message("Pos: "+position_str,0.06,darkblue)
sense.show_message("Station: "+station.name,0.06,darkblue)

# Next transit date

# Menu
## next transit
## select station

sense.stop()
