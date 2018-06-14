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
    print("Connect")
    client.subscribe("home/clock/screen")

def screenDisconnect(client, userdata, message):
    client.loop_stop()

class Screen(xfClock.module.moduleBase):

    def on_init(self, app):
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

    def on_message_print(self, client, userdata, message):
        print("%s %s" % (message.topic, message.payload))