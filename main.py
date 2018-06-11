#
#   START MAIN
#
import os
import config
import xfClock.ClockApp


if __name__ == "__main__" :
    # Set up framebuffer env
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV','/dev/fb1')
    os.environ["SDL_FBDEV"] = '/dev/fb1'

    # Start the app
    theApp = xfClock.ClockApp.Clock()
    theApp.config = config.Config
    theApp.execute()    