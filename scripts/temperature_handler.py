import pandas as pd
import time
import numpy as np
import paho.mqtt.client as mqtt


class TemperatureHandler:
    def __init__(self):
        # initialize client
        self.client = mqtt.Client()
        # set ip to listen
        self.host_ip = "192.168.2.1"
        # set username and password
        self.client.username_pw_set(username="admin", password="enflateHSLU2023!")
        # subscribe to topic
        self.sub_topic = (f"temperature_device/measurements/1", 0)
        # define what happens if client connects or gets a message
        self.client.on_message = self._on_message
        self.client.on_connect = self._on_connect
        # connect client to broker
        self.client.connect(host=self.host_ip, port=1883, keepalive=60)
        self.data = pd.DataFrame()
        # start listening loop of client
        self.client.loop_start()
        self.temp = None

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe(self.sub_topic)

    def _on_message(self, client, userdata, message):
        print("temperature message received")
        print(float(message.payload))
        self.temp = float(message.payload)

    def get_current_temperature(self) -> pd.DataFrame:
        if not self.temp:
            return pd.DataFrame()
        data = pd.DataFrame({"time": [time.time()], "temperature": [self.temp]})
        return data
