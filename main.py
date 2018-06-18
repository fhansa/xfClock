#
#   START MAIN
#
import os
import config
import xfClock.ClockApp

if __name__ == "__main__" :
    # Set up framebuffer display for pygame
    ##  - framebuffer for pitft (adafruit)

    if config.Config.system["display"] == "simulated":
        ## Use simulated dimensions
        ## This setting is primarily used to run the clock on development computer
        pass
    else:
        ## This scenario is RaspberryPi using a pitft-screen 
        ## Framebuffer settings
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        os.putenv('SDL_FBDEV','/dev/fb1')
        os.environ["SDL_FBDEV"] = '/dev/fb1'

    print("*** STARTING xfClock ***")
    # Create the app
    theApp = xfClock.ClockApp.Clock()

    # Get config from config.py
    theApp.config = config.Config

    # Time to get going
    theApp.execute()    