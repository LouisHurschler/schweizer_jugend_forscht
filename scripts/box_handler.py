import pandas as pd
import numpy as np
import time
import paho.mqtt.client as mqtt
from data import TimeSpanLog_pb2

class BoxHandler:
    def __init__(self):
        self.client = mqtt.Client()
        # self.host_ip = "10.8.0.1"
        self.host_ip = "192.168.2.1"
        self.client.username_pw_set(username="admin", password="enflateHSLU2023!")
        self.device_id = "GSWIC023110015"
        self.sub_topic = (f'{self.device_id}/measurements/1/1', 0)
        self.client.on_message = self._on_message
        self.client.connect(host=self.host_ip,
                            port=1883,
                            keepalive=60)
        self.data = pd.DataFrame()
        self.client.on_connect = self._on_connect
        self.client.loop_start()

    def toggle_device(self, state: int):
        self.client.publish(topic=f"{self.device_id}/relays/1", payload=str(state), qos=0,
                            retain=False)
    def get_data(self) -> pd.DataFrame:
        return self.data

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe(self.sub_topic)

    def _on_message(self, client, userdata, message):
        timespanLog = TimeSpanLog_pb2.TimeSpanLog()
        timespanLog.ParseFromString(message.payload)
        print("message received")
        # TODO: convert message to datapoints
        def calc_power(current: list, voltage: list, energy: list,
                       power_factor: list, timestamp) -> pd.DataFrame:
            data_tmp = {}
            for i in range(3):
                data_tmp[f'L{i + 1}_current'] = current[i]
                data_tmp[f'L{i + 1}_voltage'] = voltage[i]
                data_tmp[f'L{i + 1}_power'] = current[i] * voltage[i]
                data_tmp[f'L{i + 1}_apparent_energy'] = energy[i] * 0.0001
                data_tmp[f'L{i + 1}_power_factor'] = power_factor[i]
            data_tmp["time"] = timestamp

            power_pd = pd.DataFrame(data_tmp, index=[0])
            # print(f'Current[A]: {current[0]}')
            # print(f'Voltage[V]: {voltage[0]}')
            # print(f'Power[W]: {current[i] * voltage[i]}')

            return power_pd

        current_list = [timespanLog.L1_current_average / 1000,
                        timespanLog.L2_current_average / 1000,
                        timespanLog.L3_current_average / 1000]
        voltage_list = [timespanLog.L1_voltage_average / 1000,
                        timespanLog.L2_voltage_average / 1000,
                        timespanLog.L3_voltage_average / 1000]
        energy_list = [timespanLog.L1_apparent_energy, timespanLog.L2_apparent_energy,
                       timespanLog.L3_apparent_energy]
        power_factor_list = [timespanLog.L1_power_factor_average / 1000,
                             timespanLog.L2_power_factor_average / 1000,
                             timespanLog.L3_power_factor_average / 1000]

        power_pd = calc_power(current=current_list,
                              voltage=voltage_list,
                              energy=energy_list,
                              power_factor=power_factor_list,
                              timestamp = timespanLog.timestamp_to.seconds)
        if not self.data.empty:
            self.data = pd.concat([self.data, power_pd], ignore_index=True)
        else:
            self.data = power_pd

