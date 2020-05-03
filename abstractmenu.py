from threading import Thread
import logging


LOGGER = logging.getLogger("issense.amenu")

class AbstractMenu(Thread):
    def __init__(self, app, items, enable_waiting = False):
        Thread.__init__(self)
        LOGGER.debug("Create menu : "+str(items))
        self.app = app
        self.items = items
        self.current=0
        self._wainting = None
        self.enable_waiting = enable_waiting
        if self.enable_waiting:
            self.wait()

    
    def run(self):
        if not self.enable_waiting:
            self.show_current()
        while True:
            event = self.app.sense.stick.wait_for_event()
            if self.handleEvent(event):
                return
            

    def handleEvent(self, event):
        if event.action != "pressed":
            LOGGER.warning("Unhandled action "+event.action)
            return False
        if self._wainting is not None:
            LOGGER.debug("Wake up")
            self._wainting.stop()
            self._wainting = None
            self.show_current()
            return False
        
        rotation = self.app.sense.global_rotation

        if event.direction == "up":
            if rotation == 0:
                return self.prev()
            elif rotation == 90:
                return self.levelup()
            elif rotation == 180:
                return self.next()
            else:
                return self.leveldown()
        
        if event.direction == "down":
            if rotation == 0:
                return self.next()
            elif rotation == 90:
                return self.leveldown()
            elif rotation == 180:
                return self.prev()
            else:
                return self.levelup()

        if event.direction == "left":
            if rotation == 0:
                return self.levelup()
            elif rotation == 90:
                return self.next()
            elif rotation == 180:
                return self.leveldown()
            else:
                return self.prev()
        
        if event.direction == "right":
            if rotation == 0:
                return self.leveldown()
            elif rotation == 90:
                return self.prev()
            elif rotation == 180:
                return self.levelup()
            else:
                return self.next()

    def wait(self):
        self._wainting = self.app.sense.waiting()

    def show_current(self):
        LOGGER.debug("Current :" + str(self.current))
        if 'image' in self.items[self.current]:
            self.app.sense.load_image(self.items[self.current]['image'])
        elif 'text' in self.items[self.current]:
            self.app.sense.show_message(self.items[self.current]['text'])
            self.app.sense.show_letter(self.items[self.current]['text'][0])

    def prev(self):
        LOGGER.debug("Select previous item")
        self.current -= 1
        if self.current < 0:
            self.current = len(self.items)-1
        self.show_current()
        return False
    def next(self):
        LOGGER.debug("Select next item")
        self.current += 1
        if self.current >= len(self.items):
            self.current = 0
        self.show_current()
        return False

    def levelup(self):
        LOGGER.debug("Level up")
        if self.enable_waiting:
            self.wait()
            return False
        else:
            return True
    def leveldown(self):
        LOGGER.debug("Level down")
        if 'function' in self.items[self.current]:
            should_exit = self.items[self.current]['function'](self)
            if should_exit:
                return True
            if self.enable_waiting:
                self.wait()
                return False
            else:
                return True
        return False
