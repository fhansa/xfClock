#
#   Clock module
#
import xfClock.module
import os
import math
import datetime

# TODO: Remove reference
import pygame


class Clock(xfClock.module.moduleBase):
    def __init__(self, app):
        super().__init__(app)
        self.path = os.path.dirname(__file__)
        pass

    def on_init(self):
        ## Load Clockbg
        print(self.path)
        imgPath = os.path.join(self.path, "images/clw.png")
        self.clockbg = pygame.image.load(imgPath).convert_alpha()   

        ## If clock don't fit frame then resize
        if self.clockbg.get_size()[0] > self.width or self.clockbg.get_size()[1] > self.height:
            ## Resize
            self.clockbg = self.aspect_scale(self.clockbg, self.width, self.height)

        self.clockWidth = self.clockbg.get_size()[0]
        self.clockHeight = self.clockbg.get_size()[1]
        self.clockLeft = (self.width - self.clockWidth) / 2
        self.clockTop = (self.height - self.clockHeight) / 2

    #
    # Draw the clock
    #   
    def on_render(self, surface):
        ## Print background
        surface.blit(self.clockbg,(self.clockLeft,self.clockTop))
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
        secDX = x + int(math.cos(math.radians(-secAng))*self.clockWidth / 2)
        secDY = y - int(math.sin(math.radians(-secAng))*self.clockHeight / 2)
        pygame.draw.line(surface,(255,255,255), (x,y), (secDX, secDY), 1)

        minDX = x + int(math.cos(math.radians(-minAng))*self.clockWidth / 2) * 0.9
        minDY = y - int(math.sin(math.radians(-minAng))*self.clockHeight / 2) * 0.9 
        pygame.draw.line(surface,(255,255,255), (x,y), (minDX, minDY), 2)

        hourDX = x + int(math.cos(math.radians(-hourAng))*self.clockWidth / 2) * 0.6
        hourDY = y - int(math.sin(math.radians(-hourAng))*self.clockHeight / 2) * 0.6
        pygame.draw.line(surface,(255,255,255), (x,y), (hourDX, hourDY), 5)
        pass
    
    def on_cleanup(self):
        pass