#
#   xfClock is the application for xfClock
#
#
##  TODO: Add better logging
##
import os
import datetime
import pygame
from pygame.locals import *
from pygame.time import *
from math import *
from threading import Thread

# modules
import importlib 


class Clock:
    def __init__(self):
        self._running = True
        self.modules = []
        self._executedelay = 200        # ms delay in main loop. use to free upp processing time for threading 
    
    # ----------------------------------------------------------------------
    #   Defined properties exposed from the application
    #   These properties can be used by modules
    #

    ## Width and Height of screen
    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height
    
    ## Reference to Screen (surface)
    @property 
    def screen(self):
        return self._screen

    @property 
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    # ----------------------------------------------------------------------
    #   Application lifecycle
    #

    ## on_init - called once when initialization is done
    def on_init(self):

        ## SETUP Screen, full screen and no mouse
        ## TODO: customizeable background??
        pygame.init()
        self.size = self._width, self._height = pygame.display.Info().current_w, pygame.display.Info().current_h 
        self._screen = pygame.display.set_mode( self.size, pygame.FULLSCREEN )
        pygame.mouse.set_visible(0)
        self.bgColor = (0,0,0)

        ## Add modules from config
        modules = self.config.modules
        for modItem in modules:
            try:
                mod = modItem["name"]
                m = importlib.import_module("xfClock.modules." + mod + "." + mod)
                modClass = getattr(m, mod)
                modObj = modClass()
                if "config" in modItem:
                    modObj.config = modItem["config"]
                self.modules.append(modObj)
            except, e:
                print("Error when creating module {}. Error: {}".format(mod), str(e))
                print("This error does not halt xfClock. Only the affected module is not loaded")


        ## Iterate and init all modules
        for mod in self.modules:
            try:
                mod.on_init(self)
            except, e:
                print("on_init failed for {}".format(mod.__class__.__name__))
                print("Message: {}".format(str(e))

        self._running = True
 
    ## on_event - called whenever an event occurs
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    ##
    ## on_loop - "game-loop" called pretty often
    def on_loop(self):
        pass

    ##
    ## on_render - called when its time to draw  
    def on_render(self):
        ## BACKGROUND
        self.screen.fill( self.bgColor )

        ## Modules
        for mod in self.modules:
            mod.on_render(self)

        ## done
        pygame.display.flip()

    ##
    ## on_cleanup - is called when the fun is over and its time to quit
    def on_cleanup(self):
        pygame.quit()
 
    ##
    ## execute - main loop of the program
    def execute(self):
        try:
            if self.on_init() == False:
                self._running = False
    
            while( self._running ):
                for event in pygame.event.get():
                    self.on_event(event)
                self.on_loop()
                self.on_render()
                pygame.time.wait(200)
        finally:
            self.on_cleanup()