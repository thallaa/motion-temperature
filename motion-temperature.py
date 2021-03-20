#!/usr/bin/python3

import paho.mqtt.client as mqtt
import time
import urllib3
from urllib.parse import quote
import signal
import sys

# Conf
broker = "10.0.0.1"
conf = {1 : "/etc/motioneye/camera-1.conf", 2: "/etc/motioneye/camera-2.conf", 3 : "/etc/motioneye/camera-3.conf", 4 : "/etc/motioneye/camera-4.conf"}
outdoortemptopic = "weather/tempnow"
garagetemptopic = "garage/temp"


def signal_handler(sig, frame):
    sys.exit(0)

def getname(conffile):
    try:
        # This cool one-liner from https://stackoverflow.com/a/52719066
        dict = {k:v for k, *v in (l.split(' ') for l in open(conffile))}
        return ''.join(dict.get("text_left")).strip()
    except:
        print("Error reading configuration file " + conffile)
        sys.exit(1)

# Outdoor temperature is updated to four cameras
def on_outdoortemp_message(client, userdata, message):
    val = str(message.payload.decode("utf-8"))
    update(1, val)
    update(3, val)
    update(4, val)

def on_garagetemp_message(client, userdata, message):
    val = str(message.payload.decode("utf-8"))
    update(2, val)

# This does the actual work of updating the overlay text
def update(camera, value):
    motioneyeurl = "http://localhost:7999/" + str(camera) + "/config/set?text_left=" + name[camera]
    url = motioneyeurl + quote("\\n" + value + "C")
    # print("Updating: " + url)
    try:
        http.request('GET', url)
    except:
        pass

# This catches INT signal for preventing ugly traces on exit
signal.signal(signal.SIGINT, signal_handler)

# Dig names for each camera
name = {1 : getname(conf[1]), 2 : getname(conf[2]), 3 : getname(conf[3]), 4 : getname(conf[4])}

http = urllib3.PoolManager()

outdoortempclient = mqtt.Client("motioneye1")
garagetempclient = mqtt.Client("motioneye2")

outdoortempclient.on_message=on_outdoortemp_message
garagetempclient.on_message=on_garagetemp_message

try:
    outdoortempclient.connect(broker)
    garagetempclient.connect(broker)
except:
    print("Error connecting to broker")
    sys.exit(1)

outdoortempclient.subscribe(outdoortemptopic)
garagetempclient.subscribe(garagetemptopic)

# First loop is started in the background
outdoortempclient.loop_start()
# Second loop blocks here
garagetempclient.loop_forever()

