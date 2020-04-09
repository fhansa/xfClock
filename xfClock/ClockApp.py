#
#   xfClock is the application for xfClock
#
#   
##  TODO: Add better logging
##
import os
import traceback
import sys
import datetime
import pygame 
import pygame.locals
import math
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
        self.modules = []                           # List of modules
        self._executedelay = 200                    # ms delay in main loop. use to free upp processing time for threading 
        self._app_dir = os.path.dirname(__file__)   #<-- absolute dir the script is in
        self.config = None                          # The configuration (from config.py)
        self.width = 0                              # Screen Width
        self.height = 0                             # Screen height
        self.screen = None                          # Screen surface

    ## ----------------------------------------------------
    #   Properties - for ease
    #
    @property
    def size(self):
        return (self.width, self.height)


    ## ----------------------------------------------------
    #   Published methodsf rom the application
    #   These can be used by modules
    #
    def hideModule(self, module):
        pass
    def showModule(self, module):
        pass


    # ----------------------------------------------------------------------
    #   Application methods - internal methods
    #
    ##  +---+---+---+       +-----+-----+
    ##  | A | B | C |       |     |     |
    ##  +---+---+---+       |  H  |  I  |
    ##  | E | F | G |       |     |     |
    ##  +---+---+---+       +-----+-----+
    ##
    ##  Available rects:
    ##      top_left, top_middle, top_right, bottom_left, bottom_middle, bottom_right
    ##      top_half (A+B+C=), bottom_half (E+F+G)
    ##      full_screen
    ##
    ##      big_left (A+B+E+F), big_right (B+C+F+G)
    ##
    ##      col_left, col_middle, col_right (A+E, B+F, C+G)
    ##
    ##      top_row, bottom_row (A+B+C, E+F+G)
    ##
    ##      left_half (H) right_half (I)

    ## Create rect from position 
    def rectFromPosition(self, position):
        rect = ( (0,0), (0,0) ) ## (x,y), (w,h)

        dimension = (0,0)
        if position == "full_screen":
            dimension = (self.width, self.height)
        elif position in ("top_left", "top_right", "top_middle", "bottom_left", "bottom_right", "bottom_middle"):
            dimension = (int(self.width / 3), int(self.height / 2))
        elif position in ("col_left", "col_right", "col_middle"):
            dimension =  (int(self.width / 3), int(self.height))
        elif position in ("big_left", "big_right"):
            dimension = (int(self.width / 3 * 2), int(self.height))
        elif position in ("top_row", "bottom_row"):
            dimension = (int(self.width), int(self.height / 2))
        elif position in ("left_half", "right_helf"):
            dimension = (int(self.width / 2), int(self.height))

        x = 0
        y = 0
        if position == "full_screen":
            x, y = (0,0)
        else:
            ypos, xpos = position.split("_")
            if ypos == "top" or ypos == "col" or ypos == "big":
                y = 0
            elif ypos == "bottom":
                y = int(self.height / 2)
            else:
                y = 0

            if xpos == "half":
                if ypos == "left":
                    x = 0
                if ypos == "right":
                    x = (int(self.width / 2))
            elif ypos == "big":
                if xpos == "left":
                    x = 0
                else:
                    x = int(self.width/3)
            elif xpos == "left" or xpos == "row":
                x = 0
            elif xpos == "middle":
                x = int(self.width / 3) * 1
            elif xpos == "right":
                x = int(self.width / 3 * 2)
            else:   
                x = 0

        rect = ( (x,y), dimension )
        return rect

    ##
    ## Create modules from config
    ##
    def createModules(self):
        ## Add modules from config
        modules = self.config.modules
        for modItem in modules:
            try:
                ## Dynamically import the module and create an instance of it
                mod = modItem["name"]
                m = importlib.import_module("xfClock.modules." + mod + "." + mod)
                modClass = getattr(m, mod)
                modObj = modClass(self)

                ## Set some good to have properties
                ## Path to module 
                modObj.modulePath = os.path.join(self._app_dir, "modules", mod)
                ## Module Configuration 
                if "config" in modItem:
                    modObj.config = modItem["config"]
                ## Module position 
                if "position" in modItem:
                    modObj.rect = self.rectFromPosition(modItem["position"])
                else:
                    modObj.rect = ((0,0), (0,0))
                self.modules.append(modObj)

            except Exception as e:
                ##
                ##  Notify in case of error but don't stop Clock from running
                ##
                print("**** CREATE MODULE ERROR - THIS WILL NOT HALT THE APPLICATION ***")
                print("Error when creating module ** {} **  . Error:{}".format(modItem["name"],e))
                traceback.print_tb(e.__traceback__)
                print("---")

    ##
    ##  Execute all modules on_init
    ##
    def initializeModules(self):
        ## Iterate and init all modules
        for mod in self.modules:
            try:
                mod.on_init()
            except Exception as e:
                ##
                ##  Notify in case of error but don't stop Clock from running
                ##
                print("on_init failed for {}".format(mod.__class__.__name__))
                print("Message: {}".format(e))

    # ----------------------------------------------------------------------
    #   Application lifecycle
    #       TODO: customizeable background??

    ## on_init - called once when initialization is done
    def on_init(self):

        pygame.init()

        ## SETUP Screen - calculate size
        if self.config.system["display"] == "simulated":
            ## App is running on dev machine - create window from configuration sizes
            self.width, self.height = self.config.system["display_width"],self.config.system["display_height"]
            displayOptions = pygame.RESIZABLE
        else:
            ## App is running on pi with pitft - Set size to whole screen
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h 
            displayOptions = pygame.FULLSCREEN

        # Create screen surface and make it black w/o mouse
        self.screen = pygame.display.set_mode( self.size, displayOptions )
        pygame.mouse.set_visible(0)
        self.bgColor = (0,0,0)
        
        ## Handle modules - create and initialize
        self.createModules()
        self.initializeModules()

        ## All is ok 
        self._running = True

    ## on_event - called whenever an event occurs
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    ## on_loop - "game-loop" called pretty often
    def on_loop(self):
        ## Modules
        for mod in self.modules:
            mod.on_loop()

    ## on_render - called when its time to draw, render all modules  
    def on_render(self):
        self.screen.fill( self.bgColor )
        for mod in self.modules:
            surface = pygame.Surface(mod.size, pygame.SRCALPHA)
            mod.on_render(surface)
            self.screen.blit(surface, mod.position)

        ## done
        pygame.display.flip()

    ## on_cleanup - is called when the fun is over and its time to quit
    def on_cleanup(self):
        for mod in self.modules:
            mod.on_cleanup()
        pygame.quit()
 
    ##
    ## execute - main loop of the program
    ##
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