import socket
import time

import pymodbus.exceptions
from pymodbus.client import ModbusTcpClient

# create udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# player settings
# repeat_mode - True/False
# repeat_value - animation repeat counter
file_path = 'Test_Color.ani'
repeat_mode = True
repeat_value = 3
frame_per_second = 40

# artnet devices config
artnet_device1 = ('192.168.0.1', 6454)
artnet_device2 = ('192.168.0.2', 6454)

# modbus devices config
modbus_device_id = 33
modbus_device1 = ModbusTcpClient('192.168.0.10', port=8234)


# modbus_relays_switch
def modbus_relays_switch(address, value, device_id):
    try:
        modbus_device1.connect()
        modbus_device1.write_coil(address, value, device_id)
        modbus_device1.close()
    except pymodbus.exceptions.ConnectionException as err:
        print(err)


# player
def player(file, repeat, value):
    count = 1
    try:
        with open(file, 'rb') as f:
            # switch on relays when animation start
            modbus_relays_switch(0, True, modbus_device_id)
            modbus_relays_switch(1, True, modbus_device_id)

            while True:
                packet = f.read(530)

                if not packet:
                    if not repeat:
                        # switch off relays when animation stop
                        modbus_relays_switch(0, False, modbus_device_id)
                        modbus_relays_switch(1, False, modbus_device_id)
                        break

                    if repeat and count < value:
                        count += 1
                        f.seek(0)
                        continue

                    # switch off relays when animation stop
                    modbus_relays_switch(0, False, modbus_device_id)
                    modbus_relays_switch(1, False, modbus_device_id)
                    break

                send_artnet_packets(frame_per_second, packet)

    except FileNotFoundError:
        print("Animation File not found")


def send_artnet_packets(fps, packet):
    universe = int(packet[14])

    if universe == 1:

        sock.sendto(packet, artnet_device1)
        time.sleep(1 / fps)

    else:
        sock.sendto(packet, artnet_device2)


player(file_path, repeat_mode, repeat_value)
