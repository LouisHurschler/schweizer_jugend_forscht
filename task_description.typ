
= Task description Schweizer Jugend forscht enflate-box projekt

== Overall tasks:

- Create a Python script to connect to an MQTT broker, receive data, and send commands to the device.
- Develop a Python script that controls an electrical heater, turning it on and off to maintain a specific constant temperature.

== Connecting to the Enflate-Box

The connection to the Enflate-Box is established using the MQTT protocol, which efficiently transmits data with minimal network bandwidth.

=== MQTT Broker Setup:
The MQTT broker is hosted on an external laptop, accessible through the enflate_network wireless network.
Network Password: enflate2023! (use this for any required passwords).
Broker IP: 192.168.2.1:1883

=== Python Library:
Use the Python package paho-mqtt to connect to the MQTT broker.

=== Topics:
Data Measurements: Subscribe to the topic *GSWIC023110015/measurements/1/1* to receive measurements every second (note that data may come in bursts with some delay).
Relay Control: Change the relay state of the device by publishing to *GSWIC023110015/relays/1*. Send "1" to enable power and "0" to disable it.


== Task details
=== Experiment with Relay State:
Your first excercise is to fill out the script such that the GUI can be started to manually control the relay state and get the power information.

=== Automated Temperature Control

- Implement Temperature Control Script:\
A base script is provided that connects to the device and monitors temperature in a loop.
Use this script to maintain the target temperature by checking the current temperature and adjusting the relay state.
Remember to look at the time needed to receive all the information.



- Optimize Power Usage:\
Measure the total power consumption required to maintain a constant temperature.
Try to adjust your implementation to minimize the total energy consumption.

=== Data Analysis and Interpretation

- Energy Calculation:\
Calculate the energy required to maintain a constant temperature.
Estimate the energy needed to heat the water initially and evaluate the device’s efficiency (considering the fixed energy required to heat water).

- Efficiency Optimization:\
Explore alternative strategies for heating the water more efficiently.
Consider the effects of tighter or more relaxed temperature tolerances on energy consumption.


