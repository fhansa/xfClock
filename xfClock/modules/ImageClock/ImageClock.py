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

    def on_init(self):
        ## Load Clockbg
        imageDir = os.path.join(self.path, "images/default/")
        self.loadImages(imageDir)

    #
    # Draw the clock
    #   
    def on_render(self, surface):
        ## Print clock
        now = datetime.datetime.now()
        pass
    
    def on_cleanup(self):
        pass