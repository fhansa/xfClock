#
#   Module for xfClock - Calendar
#
#       Simple calendar - show start date and summary for the most recent events
#       Use case: 
#           Show next two or three appointments for the day.
#           Show tomorrows items the evening before but today's when you 
#           wake up in the morning.
#
#
import xfClock.module
from urllib.request import urlopen
import icalendar
import datetime
import dateutil
from threading import Thread
from time import sleep
import os
import pygame

class Calendar(xfClock.module.moduleBase):
    def __init__(self, app):
        super().__init__(app)
        ## Internal propertied        
        self._events = []                                   # List of event from calendar
        self._lastFetch = datetime.datetime.now()           # timestamp for last fetch
        self.retries = 0
        self.maxRetries = 20

        ## Default configurations TODO
        self._config["font"] = "fonts/roboto-condensed/RobotoCondensed-Regular.ttf"
        self._config["fontsize"] = 14
        self._config["maxwidth"] = "auto"
        self._config["maxrows"] = "auto"
        self._config["padding"] = 20
        self._config["fetchinterval"] = 30
        self._config["timetoswitchdate"] = "23:59"
        self._config["url"] = ""
    
    def on_init(self):
        ## trigger initial fecth of calendar
        self.fetchCalendar()
        pass       

    def on_loop(self):
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
    
    ##
    ##  Render the calendar
    ##
    def on_render(self, surface):
        ## Setup font - TODO: store globally
        path = os.path.join(self.modulePath, self.config["font"])
        font = pygame.font.Font(path, self.config["fontsize"])

        ## Calculate some boundries, 
        rowHeight = font.get_linesize()
        maxRows = int((self.height - self.config["padding"] * 3) / (rowHeight   * 2 + 15)) - 1   
        maxWidth = self.width - self.config["padding"] * 2

        ## Draw max maxRows 
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

            ## Separator line
            pygame.draw.line(surface,(128,128,128), (x,y+rowHeight*2+5), (x + maxWidth, y+rowHeight*2+5), 1)
            y = y + rowHeight * 2 + rowHeight / 2
    
    #
    #   Get calendar into events-list
    #
    def fetchCalendar(self):
        try:
            if self.retries > self.maxRetries:
                exit
            url = self.config["url"]
            cal = urlopen(url).read().decode("UTF-8")
            gcal = icalendar.Calendar.from_ical(cal)
            self._events = []
            for component in gcal.walk():
                if component.name == "VEVENT":

                    eventdate = component.get('dtstart').dt.astimezone(dateutil.tz.gettz('Sweden/Stockholm'))
                    now = datetime.datetime.now(dateutil.tz.gettz('Sweden/Stockholm'))
                    ## If now > 18:00 then show tomorrows events otherwise show todays events.
                    if datetime.datetime.now().strftime("%H:%M") > self.config["timetoswitchdate"]:
                        comparedate = datetime.datetime(year=now.year, month=now.month, day=now.day) + datetime.timedelta(days=1)
                    else:
                        comparedate = datetime.datetime(year=now.year, month=now.month, day=now.day) 
                    comparedate = comparedate.astimezone(dateutil.tz.gettz('Sweden/Stockholm'))
                    if eventdate < comparedate:
                        continue

                    event = {}
                    event["summary"] = component.get('summary')
                    event["description"] = component.get('description')
                    event["location"] = component.get('location')
                    event["dtstart"] = component.get('dtstart').dt.astimezone(dateutil.tz.gettz('Sweden/Stockholm')).strftime("%d %b - %H:%M") 
                    event["dtend"] = component.get('dtend').dt.astimezone(dateutil.tz.gettz('Sweden/Stockholm')).strftime("%d %b - %H:%M") 
                    event["exdate"] = component.get('exdate')
                    event["startdate"] = component.get('dtstart').dt
                    self._events.append(event)
            self._events = sorted(self._events, key=lambda k: k["startdate"])
            self._lastFetch = datetime.datetime.now()
            self.retries = 0
        except Exception as e:
            print("Calendar fetch error {}".format(e))
            self.retries = self.retries + 1

