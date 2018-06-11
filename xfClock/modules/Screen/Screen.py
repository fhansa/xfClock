#
#   Module to control screen (ON/OFF) using mqtt
#
import xfClock.module

import paho.mqtt.publish as mqttPublish
import paho.mqtt.client as mqttClient


def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

def screenMessage(client, userdata, message):
    msg = message.payload.decode("UTF-8")
    if msg == "off":
        print("Turn off screen")
    elif msg == "on":
        print("Turn on screen")
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
        self.client.username_pw_set("fhan", "194242!")
        self.client.connect("home", 1883, 60)
        self.client.loop_start()  

    def on_message_print(self, client, userdata, message):
        print("%s %s" % (message.topic, message.payload))