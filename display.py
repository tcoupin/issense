from sense_hat import SenseHat
from threading import Thread
import datetime
import time

class Display(SenseHat):

    def __init__(self):
        SenseHat.__init__(self)
        self.__rotation_delta = 0
        self.__autorotate = Autorotate(self)
        self.__autorotate.start()
        self.__autolight = Autolight(self)
        self.__autolight.start()
    
    def show_message(self, *args):
        self.__rotation_delta = 90
        SenseHat.show_message(self,*args)
        self.__rotation_delta = 0
    
    @property
    def global_rotation(self):
        gr = self.rotation+self.__rotation_delta
        if gr < 0:
            gr+=360
        if gr > 360:
            gr-=360
        return gr

    @global_rotation.setter
    def global_rotation(self,r):
        r = r-self.__rotation_delta
        if r < 0:
            r+=360
        if r > 360:
            r-=360
        self.rotation = r

    def stop(self):
        self.__autorotate.stop()
        self.__autolight.stop()

    def stop_autorotate(self):
        self.__autorotate.stop()
    def pause_autorotate(self):
        self.__autorotate.pause()
    def autorotate(self):
        self.__autorotate.unpause()


class Autorotate(Thread):
    def __init__(self, sense):
        Thread.__init__(self)
        self.__sense = sense
        self.__pausing = False
        self.__stop_now = False;

    def stop(self):
        self.__stop_now = True

    def pause(self):
        self.__pausing = True
    
    def unpause(self):
        self.__pausing = False

    def run(self):
        while self.__stop_now == False:
            if self.__pausing == False:
                acc = self.__sense.get_accelerometer_raw()
                if self.__sense.global_rotation != 0 and  acc['y'] > 0.5:
                    self.__sense.global_rotation = 0
                elif self.__sense.global_rotation != 180 and  acc['y'] < -0.5:
                    self.__sense.global_rotation = 180
                elif self.__sense.global_rotation != 90 and  acc['x'] < -0.5:
                    self.__sense.global_rotation = 90
                elif self.__sense.global_rotation != 270 and  acc['x'] > 0.5:
                    self.__sense.global_rotation = 270

            time.sleep(1)

class Autolight(Thread):
    def __init__(self, sense):
        Thread.__init__(self)
        self.__sense = sense
        self.__pausing = False;
        self.__stop_now = False;

    def stop(self):
        self.__stop_now = True

    def pause(self):
        self.__pausing = True
    
    def unpause(self):
        self.__pausing = False

    def run(self):
        while self.__stop_now == False:
            if self.__pausing == False:
                low_light = datetime.datetime.now().hour < 6 or datetime.datetime.now().hour > 18
                if self.__sense.low_light != low_light:
                    self.__sense.low_light = low_light

            time.sleep(1)