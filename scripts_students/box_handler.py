import pandas as pd
import numpy as np
import time
import paho.mqtt.client as mqtt
import struct


class BoxHandler:
    def __init__(self):
        # initialize the MQTT client
        self.client = mqtt.Client()

        # state topic to subscribe to
        self.energy_measurement_topic = (..., 0)  # The 0 stands for QOS=0

        # Define what happens if client connects or gets a new message
        self.client.on_message = self._on_message
        self.client.on_connect = self._on_connect

        # Connect client to the broker
        # This works only if connected to enflate wlan
        self.client.connect(host=..., port=..., keepalive=60)

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
            topic=...,  # choose right topic
            payload=...,  # send a string of the desired state
            qos=0,
            retain=False,
        )

    # return current data of the Box. Note that it will return the full dataframe
    def get_data(self) -> pd.DataFrame:
        return ...

    # This function gets called when the client connects to the broker
    # You have to subscribe to the right topic here
    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe(...)

    # This function gets called when the client gets a message on a topic
    # it previously subscribed to.
    def _on_message(self, client, userdata, message):
        # the message is parsed such that it does not take that much space.
        # it can be encrypted with the function timespanLog.ParseFromString(text)
        current, voltage, power_factor, time = struct.unpack(
            ">4I", message.payload
        )
        # note that the current gets returned in 0.001 A, the voltage in 0.001 V,
        # the powerfactor as an int between -1000 and 1000 and the timestep as an
        # UNIX timestamp, which is defined as number of seconds passed since January 1st 1970 (UTC)

        data_tmp = {}
        data_tmp["current"] = ...  # current in A
        data_tmp["voltage"] = ...  # voltage in V
        data_tmp["power_factor"] = ...  # between -1 and 1
        data_tmp["power"] = ...  # in kW, make sure it is positive

        data_tmp["time"] = ...

        power_pd = pd.DataFrame(data_tmp, index=[0])

        # concatinate the new data to the box data
        if not self.data.empty:
            self.data = pd.concat([self.data, power_pd], ignore_index=True)
        else:
            self.data = power_pd
