import pandas as pd
import numpy as np
import time
import paho.mqtt.client as mqtt
from data import TimeSpanLog_pb2


class BoxHandler:
    def __init__(self):
        # initialize the MQTT client
        self.client = mqtt.Client()

        # Set MQTT broker information
        self.host_ip = "192.168.2.1"
        self.client.username_pw_set(username="admin", password="enflateHSLU2023!")

        # Device-specific configurations
        self.device_id = "GSWIC023110015"
        self.sub_topic = (f"{self.device_id}/measurements/1/1", 0)

        # Define what happens if client connects or gets a new message
        self.client.on_message = self._on_message
        self.client.on_connect = self._on_connect

        # Connect client to the broker
        self.client.connect(host=self.host_ip, port=1883, keepalive=60)

        # Initialize data storage
        self.data = pd.DataFrame()

        # Start MQTT loop to listen for messages
        self.client.loop_start()

    # if user toggles the slider in the GUI, this function gets called
    # it should toggle the relay state, which can be done by sending a message
    # to device_id/relays/1 with text "0" or "1" depending on the relay state
    def toggle_device(self, state: int):
        """Publish a message to toggle the device's relay state.

        Args:
            state (int): Relay state (0 for off, 1 for on).
        """
        self.client.publish(
            topic=f"{self.device_id}/relays/1", payload=str(state), qos=0, retain=False
        )

    # return current data of the Box. Note that it will return the full dataframe
    def get_data(self) -> pd.DataFrame:
        return self.data

    # This function gets called when the client connects to the broker
    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe(self.sub_topic)

    # This function gets called when the client gets a message on a topic
    # it previously subscribed to.
    def _on_message(self, client, userdata, message):
        # the message is parsed such that it does not take that much space.
        # it can be encrypted with the function timespanLog.ParseFromString(text)
        timespanLog = TimeSpanLog_pb2.TimeSpanLog()
        timespanLog.ParseFromString(message.payload)

        data_tmp = {}
        data_tmp["current"] = timespanLog.L1_current_average / 1000  # current in ...
        data_tmp["voltage"] = timespanLog.L1_voltage_average / 1000  # voltage in ...
        data_tmp["apparent_energy"] = timespanLog.L1_apparent_energy / 10000
        data_tmp["power_factor"] = timespanLog.L1_power_factor_average / 1000
        data_tmp["power"] = (
            data_tmp["current"] * data_tmp["voltage"] * data_tmp["power_factor"]
        )

        # device measures time as UTC + 2
        # add Zeitumstellung in Winterzeit, 60 * 60 seconds
        data_tmp["time"] = timespanLog.timestamp_to.seconds + 60 * 60

        power_pd = pd.DataFrame(data_tmp, index=[0])

        if not self.data.empty:
            self.data = pd.concat([self.data, power_pd], ignore_index=True)
        else:
            self.data = power_pd
