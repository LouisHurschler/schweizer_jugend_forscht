import paho.mqtt.client as mqtt
import time
import numpy as np

client = mqtt.Client()
client.connect(host="192.168.2.1", port=1883, keepalive=60)
# evtl close it to enable other programs to write?

while True:
    tempfile = open("/sys/bus/w1/devices/28-000000837d52/w1_slave", "r") # update this
    tempdata = tempfile.read()    
    tempfile.close()

    # print(tempdata)

    try:
        tempdata = tempdata.split("\n")[1].split(" ")[9] #?
        temperature = float(tempdata[2:]) / 1000.
    except :
        print("error")
        continue
    # print(temperature)
    client.publish(topic="temperature_device/measurements/1",payload=str(temperature), qos=0, retain=False)
    time.sleep(1)
