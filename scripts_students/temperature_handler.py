import pandas as pd
import datetime as dt
import numpy as np
import paho.mqtt.client as mqtt

# setup temperature handler.
# it should work very similar to the box handler


class TemperatureHandler:
    def __init__(self):
        # initialize the MQTT client
        ...

        # state topic to subscribe to
        ...

        # Define what happens if client connects or gets a new message
        ...

        # Connect client to the broker
        # This works only if connected to enflate wlan
        ...

        # Initialize data storage
        ...

        # Start MQTT loop to listen for messages
        ...

    # This function gets called when the client connects to the broker
    def _on_connect(self, client, userdata, flags, rc): ...

    def _on_message(self, client, userdata, message):
        # temp and time are floating point values, temp in C° and time in UNIX timestamp
        temp, time = struct.unpack(">2d", ...)
        # add current datapoint to self.data
        ...

    def get_current_temperature(self) -> pd.DataFrame: ...
