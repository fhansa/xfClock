#
#   Clock module
#
import xfClock.module
from math import *
import datetime

# TODO: Remove reference
import pygame

class moduleClock(xfClock.module.moduleBase):
    def __init__(self):
        pass

    def on_init(self, app):
        ## Load Clockbg
        self.clockbg = pygame.image.load("clw.png").convert_alpha()   
        self.clockWidth = self.clockbg.get_size()[0]
        self.clockHeight = self.clockbg.get_size()[1]
        self.clockLeft = (app.width - self.clockWidth) / 2
        self.clockTop = (app.height - self.clockHeight) / 2
        
    def on_render(self, app):
        ## Print background
        app.screen.blit(self.clockbg,(self.clockLeft,self.clockTop))
        ## Print clock
        now = datetime.datetime.now()

        # X,y = center of clock
        x = self.clockLeft + self.clockWidth / 2
        y = self.clockTop + self.clockHeight / 2

        ## Angles 
        secAng = 270 + 6 * now.second
        minAng = 270 + 6 * now.minute
        hourAng = 270 + 30 * (now.hour + now.minute/60)

        ## Calculate distance and draw
        secDX = x + int(cos(radians(-secAng))*self.clockWidth / 2)
        secDY = y - int(sin(radians(-secAng))*self.clockHeight / 2)
        pygame.draw.line(app.screen,(255,255,255), (x,y), (secDX, secDY), 1)

        minDX = x + int(cos(radians(-minAng))*self.clockWidth / 2) * 0.9
        minDY = y - int(sin(radians(-minAng))*self.clockHeight / 2) * 0.9 
        pygame.draw.line(app.screen,(255,255,255), (x,y), (minDX, minDY), 2)

        hourDX = x + int(cos(radians(-hourAng))*self.clockWidth / 2) * 0.6
        hourDY = y - int(sin(radians(-hourAng))*self.clockHeight / 2) * 0.6
        pygame.draw.line(app.screen,(255,255,255), (x,y), (hourDX, hourDY), 5)
        pass
    
    def on_cleanup(self, app):
        pass