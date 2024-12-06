# General Information
The code from this repo was used for the enflate project of the schweizer jugend forscht event TechXperience at HSLU 2024.
The goal of the project was to setup a connection to some device and control it using python code.
a lot of projects, for example the enflate project, are based on this or similar technologies.

# instructions to setup the student project for schweizer jugend forscht
To set up the student project as of 2024, you need following hardware:
- an "enflate box" (swisbox device with SU100 measurement device)
- something which is able to measure temperature, connect to a broker and send mqtt messages (raspberry pi with temperature measurement device)
- an mqtt broker which is accessible from external laptops, the enflate box and the temperature measurement device
- some devices which enable some temperature control (electric heaters, cooking plates etc.)

## enflate box:
The enflate box is a device, which is able to measure energy data and switch some relays according to mqtt messages.
It is able to connect to a broker and send the data and receive instructions using mqtt messages.
The swisbox cofiguration can be changed using the swisbox-explorer application, where the Broker IP-address can be set.
The Swisbox has to be able to reach this IP address.
I have done this by simpy connect the LAN cable to my laptop and start a broker on my laptop at an address reachable with this connection.

It is also possible to use the setup used for the enflate project and access the broker (which is currently hosted at florians home) by using the wifi provided by the router.
The drawback of this method is that it enforces the students to connect to the router of the enflate-projet and possibly use a lot of networking data, which is restricted for the whole project.

## temperature measurement device
To carry out the project similarly to the one of 2024, you will need some temperature sensor.
I used a raspberry pi with a DS18B20 temperature sensor. To send the temperature data, you can use the script in scripts/temperature_measurements.py, which is written for a rasperry pi 5 with the right setup of the sensor 
https://cbrell.de/blog/raspilab-wetterstation-dritte-mission-temperatur-messen-mit-dem-bs18b20/

## mqtt broker
You can run a mqtt broker using mosquitto.
For this project, you should change the configuration file and add following lines:
```
listener 1883 0.0.0.0
allow_anonymous true
persistence true
```
This enables the broker to listen to any IP address and allow anonymous requests, which makes it less secure but reduces possible errors.
This should only be done because the data here is not sensitive and this is a test project.

Then you have to make sure that people can connect to this broker. For this, you have to be on a wlan with a shared ip space, for example an open network.
It is not enough to be on the same network as for example the hslu network because there you probably cannot accesss the ip space of other devices.
I did this by creating a own network using dnsmasq as dns server and hostapd to turn the wlan card of my laptop to access card, which allows external devices to connect to it (similar as hotspot, but self-managed).
Additionaly, I created port-forwarding from this own network output to the lan-network of hslu to enable internet access. Then, other devices can connect to my laptop using this new internet, enabling connections to the broker as well as connections to the internet.
But I am using a linux laptop, with windows this could be far more difficult.
Another method to do something similar could be to use a open network.

If this does not work, you can use the broker and network of the enflate project by connecting the devices to the wland of the enflate box.
If you do it like this, do not forget to ask florian or some other enflate employees if this is okay and how much internet can be used.


## simulation
The final task for the students is to connect to the broker, be able to receive and send data and to write a script which controls the temperature.
You can find a master solution in the scripts folder.
The students should modify the python files in the scripts_students folder, containing a skeleton code with blank spaces.
Then, they should write a code in the update_plot function in the simulation script. This function is called recursively every second (if the program runs inefficiently, it gets called less frequently)
Note to change the topics in the box- and temperature handlers according to the topics sent to the broker.


good luck!
