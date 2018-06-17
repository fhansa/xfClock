#
#   Module for xfClock - Calendar
#
import xfClock.module
from urllib.request import urlopen
import icalendar
import datetime
from threading import Thread
from time import sleep
import os
import pygame

class Calendar(xfClock.module.moduleBase):
    def __init__(self):
        super().__init__()

        ## Internal propertied        
        self._events = []                                   # List of event from calendar
        self._lastFetch = datetime.datetime.now()           # timestamp for last fetch

        ## Default configurations
        self._config["font"] = "fonts/roboto-condensed/RobotoCondensed-Regular.ttf"
        self._config["fontsize"] = 14
        self._config["maxwidth"] = "auto"
        self._config["maxrows"] = "auto"
        self._config["padding"] = 20
        self._config["fetchinterval"] = 30
    
    def on_init(self, app):
        ## trigger fecth of calendar
        self.fetchCalendar()
        pass       

    def on_loop(self, app):
        ## Check time - start update if time has passed
        if self._lastFetch + datetime.timedelta(seconds=self._config["fetchinterval"]) < datetime.datetime.now():
            self._events.clear()
            self.fetchCalendar()

    ##
    ##  fitText - will adopt text to fit maxWidth and cut the text with ... if neccessary
    ##
    def fitText(self, font, text, maxWidth):
        w, h = font.size(text)
        if w > maxWidth:
            margin = font.size("...")
            while w > maxWidth - margin[0]:
                text = text[:-1]
                w, h = font.size(text)
            text = text + "..."
        return text

    def on_render(self, app, surface):
        ## Setup font - TODO: store globally
        path = os.path.join(self.modulePath, self.config["font"])
        font = pygame.font.Font(path, self.config["fontsize"])

        ## Calculate some boundries, 
        rowHeight = font.get_linesize()
        maxRows = int((self.height - self.config["padding"] * 3) / (rowHeight   * 2 + 15)) - 1   
        maxWidth = self.width - self.config["padding"] * 2

        y = x = self.config["padding"]
        for idx, e in enumerate(self._events):
            if idx > maxRows: 
                break
            ## Row 1 is the date
            text = self.fitText(font, e["dtstart"], maxWidth)
            tSurface = font.render(text, True, [255,255,255])
            surface.blit(tSurface, (x, y))

            ## Row 2 is the summary (header)
            text = self.fitText(font, e["summary"], maxWidth)
            tSurface = font.render(text, True, [255,255,255])
            surface.blit(tSurface, (x + 20, y+rowHeight))

            pygame.draw.line(surface,(128,128,128), (x,y+rowHeight*2+5), (x + maxWidth, y+rowHeight*2+5), 1)

            y = y + rowHeight * 2 + 15
    
    def fetchCalendar(self):
        url = "https://calendar.google.com/calendar/ical/fhan770@gmail.com/private-741b1432f7197e14cd5538cccac41a25/basic.ics"
        cal = urlopen(url).read().decode("UTF-8")
        gcal = icalendar.Calendar.from_ical(cal)
        self._events = []
        for component in gcal.walk():
            if component.name == "VEVENT":
                event = {}
                event["summary"] = component.get('summary')
                event["description"] = component.get('description')
                event["location"] = component.get('location')
                event["dtstart"] = component.get('dtstart').dt.strftime("%d %b - %H:%M") 
                event["dtend"] = component.get('dtend').dt.strftime("%d %b - %H:%M") 
                event["exdate"] = component.get('exdate')

                self._events.append(event)
        self._lastFetch = datetime.datetime.now()