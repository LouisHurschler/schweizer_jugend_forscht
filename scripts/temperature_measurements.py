import paho.mqtt.client as mqtt
import datetime as dt
import numpy as np
import struct
import time

client = mqtt.Client()
client.connect(host="192.168.2.1", port=1883, keepalive=60)
# evtl close it to enable other programs to write?

while True:
    # change this according to hardware
    tempfile = open("/sys/bus/w1/devices/28-000000837d52/w1_slave", "r")
    tempdata = tempfile.read()
    tempfile.close()

    # print(tempdata)

    try:
        tempdata = tempdata.split("\n")[1].split(" ")[9]  # ?
        temperature = float(tempdata[2:]) / 1000.0
    except:
        print("error")
        time.sleep(1)
        continue
    # print(temperature)
    curr_time = float(dt.datetime.now().timestamp())
    curr_data = struct.pack(">2d", temperature, curr_time)

    client.publish(
        topic="temperature_device/measurements/1",
        payload=curr_data,
        qos=0,
        retain=False,
    )
    time.sleep(1)
