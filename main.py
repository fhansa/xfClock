#
#   START MAIN
#
import os
import config
import xfClock.ClockApp

if __name__ == "__main__" :
    # Set up framebuffer display for pygame
    ##  - framebuffer for pitft (adafruit)

    screentype = config.Config.system["screentype"]
    if  screentype == "win":
        ## xfClock is running with a desktop 
        pass
    elif screentype == "fb":
        ## Framebuffer settings
        os.putenv('SDL_VIDEODRIVER', config.Config.system["SDL_VIDEODRIVER"])
        os.putenv('SDL_FBDEV',config.Config.system["SDL_FBDEV"])
        os.environ["SDL_FBDEV"] = config.Config.system["SDL_FBDEV"]
    else: 
        # Error 
        raise xfClock.ClockApp.ClockAppException("No valid screentype found in configuration. Please check config.py")

    print("*** STARTING xfClock ***")
    # Create the app
    theApp = xfClock.ClockApp.Clock()

    # Get config from config.py
    theApp.config = config.Config

    # Time to get going
    theApp.execute()    