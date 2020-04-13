import json
import paho.mqtt.publish as mqttPublish
import paho.mqtt.client as mqttClient

#
#   Implementation of a hass device (MQTT)
#
class hassDevice:
    #
    #   Initialization - set default values based on name
    #
    def __init__(self, name, mqttConfig):
        self.config = mqttConfig
        self.name = name
        self.payload_on = "on"
        self.payload_off = "off"
        self.payload_online = "online"
        self.payload_offline = "offline"
        self.mqtt_prefix = self.config["mqttprefix"]
        self.availability_topic = self.mqtt_prefix + "/" + name
        self.state_topic = self.mqtt_prefix + "/" + name + "/state"
        self.devicetype = "switch"

    #
    # Create client and set last will
    #
    def setupMQTT(self):
        # Create Client
        self.client = mqttClient.Client()
        self.client.will_set(self.availability_topic, self.payload_offline, 0, True)
        usr = self.config["mqttusername"]
        pwd = self.config["mqttpassword"]
        if usr != "":
            self.client.username_pw_set(usr, pwd)
        host = self.config["mqtthost"]
        port = self.config["mqttport"]
        self.client.connect(host, port, 60)
        self.client.loop_start() 
        # Send discovery message
        self.publishDiscovery()

    #
    #   Discovery Message
    #
    def publishDiscovery(self):
        # Create topic <prefix>/switch/id/config
        topic = self.config["mqtt-discoveryprefix"]
        topic += "/" + self.devicetype + "/" 
        topic += self.name 
        topic += "/config"

        # create payload with all config
        payload = { 
            "name":                 self.name,
            "state_topic":          self.state_topic,
            "availability_topic":   self.availability_topic,
            "device":   {
                "identifiers": self.name,
                "manufacturer": "Santander",
                "model": "xfClock"
            }

        }

        self.client.publish(topic, json.dumps(payload), 0, True)
        pass

    #
    #   Change state
    #
    def setState(self, isOn):
        payload = self.payload_on if isOn else self.payload_off 
        self.client.publish(self.state_topic,payload, 0, False)
        pass



#
#   Testing of the hassDevice in module.
#   python Gesture.py
#
if __name__ == "__main__":
    config = {
                "mqtt-serialno":"FRH-CLOCK-DEV1",
                "mqtt-discoveryprefix":"test",
                "mqttprefix":"test",
                "mqtthost":"home",
                "mqttport":1883,
                "mqttusername":"",
                "mqttpassword":""
            }
    print("### Testing hassDevice ###")
    print("Publishing discovery")
    hadev = hassDevice("hassdevicetest", config)
    hadev.setupMQTT()
    hadev.publishDiscovery()
    print("Publishing sate changes")
    hadev.setState(True)
    hadev.setState(False)