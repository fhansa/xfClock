#
#   xfClock is the application for xfClock
#
#
##  TODO: Add better logging
##
import os
import sys
import datetime
import pygame
from pygame.locals import *
from pygame.time import *
from math import *
from threading import Thread

# modules
import importlib 

#
#   Clock is the main App-CLass
#
#
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
    #   Published methodsfrom the application
    #   These can be used by modules
    #
    def hideModule(self, module):
        pass
    def showModule(self, module):
        pass


    # ----------------------------------------------------------------------
    #   Application methods - internal methods
    #

    ## Create rect from position 
    def rectFromPosition(self, position):
        rect = (0,0)
        if position == "full_screen":
            rect = (self.width, self.height)
        elif position in ("top_left", "top_right", "top_middle", "bottom_left", "bottom_right", "bottom_middle"::
            rect = (self.width / 3, self.height / 2)
        return rect

    ## Create modules from config
    def createModules(self):
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
                if "position" in modItem:
                    modObj.rect = self.rectFromPosition(modItem["position"])
                else:
                    modObj.rect = (0,0)
                self.modules.append(modObj)
            except:
                print("Error when creating module {}. Error: {}".format(mod), sys.exc_info()[0])
                print("This error does not halt xfClock. Only the affected module is not loaded")

    def initializeModules(self):
        ## Iterate and init all modules
        for mod in self.modules:
            try:
                mod.on_init(self)
            except:
                print("on_init failed for {}".format(mod.__class__.__name__))
                print("Message: {}".format(sys.exc_info()[0]))

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
        
        ## Create rects in screen

        ## Handle modules
        self.createModules()
        self.initializeModules()

        ## All is ok 
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
    ##
    ##  +---+---+---+
    ##  | A | B | C |
    ##  +---+---+---+
    ##  | E | F | G |
    ##  +---+---+---+
    ##
    ##  Available rects:
    ##      top_left, top_middle, top_right, bottom_left, bottom_middle, bottom_right
    ##      top_half (A+B+C=), bottom_half (E+F+G)
    ##      full_screen
    ##
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