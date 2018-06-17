class Config:

    system = {
        "platform": "mac",       # PI
        "display": "simulated",
        "display_width": 480,
        "display_height": 320,
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


