import logging

from abstractmenu import *

LOGGER = logging.getLogger("issense.menu")

def Menu0(app):
    def clock(self):
        self.app.printNextTransit()

    def pos(self):
        self.app.printStationLoc()
    
    def close(self):
        return True

    def settings(self):
        self.app.choiceStation() 

    return AbstractMenu(app,[
        {
            "image": "img/clock.png",
            "function": clock
        },
        {
            "image": "img/pos.png",
            "function": pos
        },
        {
            "image": "img/setting.png",
            "function": settings
        },
        {
            "image": "img/close.png",
            "function": close
        }
    ], True)

