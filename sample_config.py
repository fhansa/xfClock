class Config:

    system = {
        "platform":"pi",       # Not used - for information only
        "screentype":"FB"       # What kind of screen (FB = Framebuffer, X = X)
        "fb_settings": {        # Framebuffer settings
            "SDL_VIDEODRIVER":"fbcon",
            "SDL_FBDEV":"/dev/fb1"    
        }
        "display":"full_screen",  # Sets type of display (simulated, full_screen)
        "display_width":480,    # Set width of display (when simulated)
        "display_height":320,   # Set height of display (when simulated)
    }

    clock = {
        #
        "test":"test"
    }

    modules = [
        {
            "name" : "Clock",
            "position":"full_screen",
            "config": {
                
            }
        },
        {
            "name" : "Gesture",
            "position":"hidden",
            "config": {
                "mqtthost":"xxx",
                "mqttport":1883,
                "mqttusername":"xx",
                "mqttpassword":"xx"
            }
        },
        {
            "name" : "Screen",
            "position":"hidden",
            "config" : {
                "mqtthost":"xxx",
                "mqttport":1883,
                "mqttusername":"xx",
                "mqttpassword":"xx"
            }

        }

    ]


