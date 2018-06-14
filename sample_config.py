class Config:
    clock = {
        #
        "test":"test"
    }

    modules = [
        {
            "name" : "Clock"
        },
        {
            "name" : "Gesture"
        },
        {
            "name" : "Screen",
            "config" : {
                "mqtthost":"xxx",
                "mqttport":1883,
                "mqttusername":"xx",
                "mqttpassword":"xx"
            }

        }

    ]


