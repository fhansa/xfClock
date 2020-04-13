#
#   Clock module
#
import xfClock.module
import os
import math
import datetime

# TODO: Remove reference
import pygame

class ImageClock(xfClock.module.moduleBase):
    def __init__(self, app):
        super().__init__(app)
        self.path = os.path.dirname(__file__)
        self.images = [None]*10
        pass

    def loadImages(self, imageDir):
        for i in range(9):
            imgPath = imageDir + str(i) + ".png"
            self.images[i] = pygame.image.load(imgPath).convert_alpha()

    def initClock(self):
        pass    

    def on_init(self):
        
        # Theme and read images 
        theme = "default/"
        if "theme" in self.config:
            theme = self.config["theme"] + "/"

        imageDir = os.path.join(self.path, "images/", theme)
        self.loadImages(imageDir)

        # Timepart (i.e Hour or minutes)
        self.timepart = "h"
        if "timepart" in self.config:
            self.timepart = self.config["timepart"]

        # Padding around images
        self.padding = 0
        if "padding" in self.config:
            self.padding = self.config["padding"]

        # Calculate rects and pad them if neccessary
        self.leftRect  = pygame.Rect(0,0, int(self.width / 2), self.height)
        self.rightRect = pygame.Rect(int(self.width / 2), 0, int(self.width / 2), self.height)
        
        if self.padding > 0:
            padding = self.padding
            self.leftRect.top += padding
            self.leftRect.left += padding
            self.leftRect.width -= padding * 2
            self.leftRect.height -= padding * 2
            self.rightRect.top += padding
            self.rightRect.left += padding
            self.rightRect.width -= padding * 2
            self.rightRect.height -= padding * 2        


    def on_render(self, surface):
        ## Print clock
        now = datetime.datetime.now()
        
        number = 0
        if self.timepart == "h":
            number = now.hour
        else:
            number = now.minute

        firstDigit = number // 10
        secondDigit = number % 10


        self.drawImage(surface, self.images[firstDigit], self.leftRect)
        self.drawImage(surface, self.images[secondDigit], self.rightRect)
        pass

    #
    # Draw the clock
    #   
    def drawImage(self, surface, img, rect):
        img = self.aspect_scale(img, rect.width, rect.height)
        
        # Center image in rect
        left = rect.left + int((rect.width - img.get_size()[0]) / 2)
        top = rect.top + int((rect.height - img.get_size()[1]) / 2)


        surface.blit(img,(left, top))


    def on_cleanup(self):
        pass