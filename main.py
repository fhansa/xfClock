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
        ## Use dsimulated dimensions
        pass
    else:
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