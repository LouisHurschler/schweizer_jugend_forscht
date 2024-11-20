from pymodbus.client import ModbusTcpClient, AsyncModbusTcpClient
import time
import paho.mqtt.client as mqtt
import struct
import datetime as dt


# to connect, run:
# sudo ip addr add 169.254.10.0/24 dev eth0
# wait long


def get_register_values(registers, len):
    res = 0
    for i in range(len):
        res += registers[i] << (len - 1 - i) * 16
    return res


def handle_response(client, address, name, unit_id, len=2):
    response = client.read_holding_registers(address, len, unit_id)
    if response.isError():
        print(f"Error reading from SU100: {response}")
        return None
    else:
        # Process data (example: print raw register values)
        res = get_register_values(response.registers, len)

    return res
    # return response.registers[1]


def run_modbus_forever():
    # Configuration
    device_ip = "169.254.10.12"  # Replace with the SU100's IP address
    device_port = 502  # Default Modbus TCP port
    unit_id = 121  # Modbus unit ID (often 1, check your device's manual)
    address_current = (
        0xF004  # Replace with the actual register address you want to read
    )
    address_voltage = 0xF006
    address_power_factor = 40104
    register_count = 2  # Number of registers to read (depends on data format)

    # Initialize Modbus TCP client
    client = ModbusTcpClient(device_ip, port=device_port)

    # setup mqtt connection
    mqttclient = mqtt.Client()
    mqttclient.connect(host="192.168.2.1", port=1883, keepalive=60)

    # Connect to the device
    if client.connect():
        print("Connected to SU100")

        while True:
            # Read registers
            res_current = handle_response(
                client, address_current, "current", unit_id
            )
            res_voltage = handle_response(
                client, address_voltage, "voltage", unit_id
            )
            res_power_factor = handle_response(
                client, address_power_factor, "powerfactor", unit_id, len=1
            )

            if not (res_current and res_voltage and res_power_factor):
                continue

            curr_data = struct.pack(
                ">4I",
                res_current,
                res_voltage,
                res_power_factor,
                int(dt.datetime.now().timestamp()),
            )

            mqttclient.publish(
                topic="energy_measurements/1",
                payload=curr_data,
                qos=0,
                retain=False,
            )
            time.sleep(1)

        # Close the connection
        client.close()
    else:
        print("Failed to connect to SU100")


if __name__ == "__main__":
    run_modbus_forever()
