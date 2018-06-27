#
#   Module for xfClock - GestureRecognizer
#
import xfClock.module
import config

from threading import Thread
import apds9960
import smbus

import paho.mqtt.publish as mqttPublish
import paho.mqtt.client as mqttClient
from time import sleep

class Gesture(xfClock.module.moduleBase):
    def __init__(self, app):
        super().__init__(app)
        #self.lastShowed
        pass
    
    def on_init(self):
        self.t = Thread(target=self.worker)
        self.t.daemon = True
        self.t.start()
        self.gesture = ""
        pass       


    def worker(self):
        # 
        #   Map gesture to MQTT-payloads
        #
        dirs = {
            apds9960.const.APDS9960_DIR_NONE: "none",
            apds9960.const.APDS9960_DIR_LEFT: "left",
            apds9960.const.APDS9960_DIR_RIGHT: "right",
            apds9960.const.APDS9960_DIR_UP: "up",
            apds9960.const.APDS9960_DIR_DOWN: "down",
            apds9960.const.APDS9960_DIR_NEAR: "near",
            apds9960.const.APDS9960_DIR_FAR: "far",
        }

        #
        # INIT i2C
        port = 1
        bus = smbus.SMBus(port)
        apds = apds9960.device.APDS9960(bus)

        # Settings
        #apds.setProximityIntLowThreshold(50)

        # Enable Gesture
        apds.enableGestureSensor()
        # Forever loop
        try:
            while True:
                sleep(0.25)
                if apds.isGestureAvailable():
                    motion = apds.readGesture()
                    gestval = dirs.get(motion, "unknown")
                    #lock.aquire()
                    #try:
                    #    self.gesture = gestval
                    #finally:
                    #    lock.release()

                    mqttPublish.single("home/clock/gesture", gestval,  qos=0,hostname="home", port=1883, client_id="clock", auth={ "username":"fhan", "password":"194242!" })
                    print("Gesture={}".format(dirs.get(motion, "unknown")))


        finally:
            print("Leaving Gesture")
