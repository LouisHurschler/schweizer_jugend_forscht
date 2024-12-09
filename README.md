# General Information
This repository contains the code used for the Energy consumption optimisation project, part of the Schweizer Jugend Forscht event **TechXperience** at HSLU 2024.
The project aimed to establish a connection with devices and control them using Python code.
Many other projects, for example the _Enflate Strompilot_ project, rely on similar technologies as a foundation.

# Setup Instructions for the Student Project
To replicate the 2024 student project setup, you will need the following hardware:

- **Enflate Box**: A Swisbox device equipped with an SU100 energy measurement unit.
- **Temperature Measurement Device**: A Device capable of measuring temperature and send this to the broker (For example raspberry pi with DS18B20 temperature sensor)
- **MQTT Broker**: Accessible by external laptops, the Enflate Box, and the temperature measurement device.
- **Heating Devices**: Such as electric heaters or cooking plates.

## Enflate Box:
The Enflate box is a device capable of measuring energy data and switching relays based on MQTT messages.

It is able to connect to a broker and send the data and receive instructions using MQTT messages.

The Swisbox cofiguration can be modified using the Swisbox-explorer application, where the broker's IP-address can be set.
The Swisbox must be able to reach this IP address.
One way to achieve this is by connecting the Swisbox’s LAN cable to your laptop and starting a broker on your laptop at an accessible address.


Alternatively, you can use the setup from the Enflate project and access the broker (currently hosted at Florian's home) via the wlan of the router inside the Enflate Box.
However, this method requires students to connect to the Enflate project's router and may consume a significant amount of network data, which is limited for the project.

## Temperature Measurement Device
To replicate the 2024 project, you will need a temperature sensor.
I used a Raspberry Pi with a DS18B20 temperature sensor. To send the temperature data, you can use [this](scripts/temperature_measurements.py) script, which is designed for a Rasperry Pi 5.
The sensor was connected as described in [this guide](https://cbrell.de/blog/raspilab-wetterstation-dritte-mission-temperatur-messen-mit-dem-bs18b20/)

## MQTT Broker
You can run a MQTT broker using mosquitto.
For this project, you should change the configuration file and add following lines:
```
listener 1883 0.0.0.0
allow_anonymous true
persistence true
```
This enables the broker to listen to any IP address and accept anonymous requests, which makes it less secure but reduces possible errors.
This should only be done because the data here is not sensitive and this is a test project.


Ensure that the devices can connect to this broker. To achieve this, they must be on a shared IP space, such as an open network.
In environments like HSLU's network, devices might not have access to other devices IP spaces.

To overcome this, I created a private network using **dnsmasq** as a DNS server and **hostapd** to turn my laptop’s wlan card into an access point. This setup allowed external devices to connect (similar to a hotspot but self-managed).

Additionally, I enabled port forwarding from this private network to HSLU's LAN network to provide internet access.
This allowed other devices to connect to my laptop for both broker communication and internet access.

**Note:** This setup was implemented using a Linux OS. Achieving similar functionality on Windows may be more complex.
Another option is to use an open network for connectivity.

If this method fails, you can use the broker and network of the Enflate project by connecting the devices to the wlan of the Enflate box.
If you do it like this, do not forget to ask Florian or some other Enflate team member if this is okay and how much internet can be used.


# Tasks for the students
The final task for the students is to connect to the broker, be able to receive and send data and to write a script which controls the temperature.
You can find a master solution in the _scripts_ folder.

The students should modify the python files in the _scripts_students_ folder, containing a skeleton code with blank spaces.
Then, they should write a code in the _update_plot_ function in the simulation script. This function is called recursively every second (if the program runs inefficiently, it gets called less frequently)

Don't forget to clarify if the students have some python environment available and if not, borrow a laptop for the week with pycharm installed.

Don't forget to change the topics in the box- and temperature handlers according to the topics sent to the broker.

The goal of their script should be to control a device. For example, we heated water in a plate on an electric cooking plate whilst measuring the temperature of the water.
Then their script turned the cooking plate on and off, with the goal to reach a constant temperature of the water (60 C°). The difficulties is to add the temperature of the cooking plate to your computations / script.

Good luck!
