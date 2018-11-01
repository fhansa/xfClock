#
#   Module to control screen (ON/OFF) using mqtt
#
#       Module will subscribe to 
#
#
import xfClock.module

import os
import paho.mqtt.publish as mqttPublish
import paho.mqtt.client as mqttClient

class Screen(xfClock.module.moduleBase):
    def __init__(self, app):
        super().__init__(app)

    def on_init(self):
        #   Config settings
        self.payload_on = "on"
        self.payload_off = "off"

        # Start mqtt subscribe
        self.client = mqttClient.Client()
        self.client.on_connect = self.screenConnect
        self.client.on_disconnect = self.screenDisconnect
        self.client.on_message = self.screenMessage 
        #usr = self.config["mqttusername"]
        #pwd = self.config["mqttpassword"]
        #if usr != "":
        #self.client.username_pw_set(usr, pwd)
        host = "mini" #self.config["mqtthost"]
        port = 1883 #self.config["mqttport"]
        self.client.connect(host, port, 60)
        self.client.loop_start()  

    ## MQTT Callbacks
    def screenMessage(self, client, userdata, message):
        ## 
        msg = message.payload.decode("UTF-8")
        if msg == self.payload_off:
            os.system("sudo sh -c 'echo \"0\" > /sys/class/backlight/soc\:backlight/brightness'")
        elif msg == self.payload_on:
            os.system("sudo sh -c 'echo \"1\" > /sys/class/backlight/soc\:backlight/brightness'")
        else:
            print(message.payload)

    def screenConnect(self, client, userdata, message, rc):
        if rc == 0:
            print("Connected ok")
            client.subscribe("home/clock/screen")
        else:
            print("Connect failes")
            print(message)

    def screenDisconnect(self, client, userdata, rc):
        if rc != 0:
            print("unexpected disconnect, trying to reconnect in 30 seconds")
        else:
            print("Dicsonnected")
        client.loop_stop()
