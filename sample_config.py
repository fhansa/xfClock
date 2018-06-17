class Config:
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


