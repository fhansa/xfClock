#
#   Module to control screen (ON/OFF) using mqtt
#
#   Implements mqtt-discovery   
#
#
import xfClock.module

import os
import json
import paho.mqtt.publish as mqttPublish
import paho.mqtt.client as mqttClient

class Screen(xfClock.module.moduleBase):
    def __init__(self, app):
        super().__init__(app)

    def on_init(self):
        #   Config settings
        self.payload_on = "ON"
        self.payload_off = "OFF"
        self.payload_online = "online"
        self.payload_offline = "offline"
        self.mqtt_prefix = self.config["mqtt-discoveryprefix"]
        self.availability_topic = self.mqtt_prefix + "/clock/screen"
        self.state_topic = self.mqtt_prefix + "/clock/screen/state"
        self.command_topic = self.mqtt_prefix + "/clock/screen/set"


        # Start mqtt subscribe
        self.client = mqttClient.Client()
        self.client.will_set(self.availability_topic, self.payload_offline, 0, True)
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
        self.publishDiscovery()
        self.client.loop_start()  

    #
    # Publish MQTT-discovery message as retain
    #
    def publishDiscovery(self):
        # Create topic <prefix>/switch/id/config
        topic = self.config["mqtt-discoveryprefix"]
        topic += "/switch/" 
        topic += self.config["mqtt-serialno"]
        topic += "/config"

        # create payload with all config
        payload = { 
            "name":                 "Clock",
            "state_topic":          self.state_topic,
            "command_topic":        self.command_topic,
            "availability_topic":   self.availability_topic,
            "device":   {
                "identifiers": self.config["mqtt-serialno"],
                "manufacturer": "Santander",
                "model": "xfClock"
            }

        }

        self.client.publish(topic, json.dumps(payload), 0, True)

    #
    #   Publish Availability message
    #
    def publishAvailability(self, available):
        if available:
            payload = self.payload_online
        else:
            payload = self.payload_offline
        self.client.publish(self.availability_topic, payload, 0, True)

    #
    #   Publish State
    #
    def publishState(self, isOn):
        if isOn:
            payload = self.payload_on
        else:
            payload = self.payload_off
        self.client.publish(self.state_topic, payload)


    ## MQTT Callbacks
    def screenMessage(self, client, userdata, message):
        ## 
        msg = message.payload.decode("UTF-8")
        print(msg)
        if msg == self.payload_off:
            self.setScreen(False)
        elif msg == self.payload_on:
            self.setScreen(True)
        else:
            print(message.payload)


    def setScreen(self, isOn):
        if isOn:
            os.system("sudo sh -c 'echo \"1\" > /sys/class/backlight/soc\:backlight/brightness'")
        else:
            os.system("sudo sh -c 'echo \"0\" > /sys/class/backlight/soc\:backlight/brightness'")
        self.publishState(isOn)


    def screenConnect(self, client, userdata, message, rc):
        if rc == 0:
            print("Connected ok")
            self.publishAvailability(True)
            self.publishState(True)
            client.subscribe(self.command_topic)
        else:
            print("Connect failes")
            print(message)

    def screenDisconnect(self, client, userdata, rc):
        if rc != 0:
            print("unexpected disconnect, trying to reconnect in 30 seconds")
        else:
            print("Dicsonnected")
        client.loop_stop()
