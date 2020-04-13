class Config:

    system = {
        "executedelay":200,     # Delay in loop (milliseconds)  
        "platform":"pi",        # Not used - for information only
        "screentype":"win",     # What kind of screen (fb = Framebuffer, win = GUI (X or windows))
        "fb_settings": {        # Framebuffer settings (when screentype is fb)
            "SDL_VIDEODRIVER":"fbcon",
            "SDL_FBDEV":"/dev/fb1"    
        },
        "win_settings": {
            "display":"window", # Sets type of display (window, full_screen)
            "width":800,        # Set width of display (when window)
            "height":480,       # Set height of display (when window)
        },
        "mqtt":false,
        "mqttsettings": {
            "host": home,
            "port": 1883,
            "user": "",
            "password": "",
            "modules":[],

            "discoveryprefix":"test",
            "devicename":"test",
            "mqttprefix":"test"

        }
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


