#
#   Module to control screen (ON/OFF) using mqtt
#
import xfClock.module

import os
import paho.mqtt.publish as mqttPublish
import paho.mqtt.client as mqttClient


def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

def screenMessage(client, userdata, message):
    msg = message.payload.decode("UTF-8")
    if msg == "off":
        os.system("sudo sh -c 'echo \"0\" > /sys/class/backlight/soc\:backlight/brightness'")
    elif msg == "on":
        os.system("sudo sh -c 'echo \"1\" > /sys/class/backlight/soc\:backlight/brightness'")
    else:
        print(message.payload)

def screenConnect(client, userdata, message, rc):
    if rc == 0:
        print("Connected ok")
        client.subscribe("home/clock/screen")
    else:
        print("Connect failes")
        print(message)

def screenDisconnect(client, userdata, message, rc):
    if rc != 0:
        print("unexpected disconnect, trying to reconnect in 30 seconds")
    else:
        print("Dicsonnected")
    client.loop_stop()

class Screen(xfClock.module.moduleBase):

    def on_init(self, app):
        #   Config settings
        self.payload_on = "on"
        self.payload_off = "off"


        # Start mqtt subscribe
        self.client = mqttClient.Client()
        self.client.on_connect = screenConnect
        self.client.on_disconnect = screenDisconnect
        self.client.on_message = screenMessage 
        usr = self.config["mqttusername"]
        pwd = self.config["mqttpassword"]
        if usr != "":
            self.client.username_pw_set("fhan", "194242!")
        host = self.config["mqtthost"]
        port = self.config["mqttport"]
        self.client.connect(host, port, 60)
        self.client.loop_start()  

    ## MQTT Callbacks
    def screenMessage(self, client, userdata, message):
        ## 
        msg = message.payload.decode("UTF-8")
        if msg == self.payload_off:
            os.system("sudo sh -c 'echo \"0\" > /sys/class/backlight/soc\:backlight/brightness'")
        elif msg == self.payload_off:
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

    def screenDisconnect(self, client, userdata, message, rc):
        if rc != 0:
            print("unexpected disconnect, trying to reconnect in 30 seconds")
        else:
            print("Dicsonnected")
        client.loop_stop()
