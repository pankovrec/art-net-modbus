
import socket
import time

from pymodbus.client import ModbusTcpClient

# create udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# artnet device config
server_address1 = ('127.0.0.1', 6454)
server_address2 = ("127.0.0.1", 6455)

# modbus device config
client = ModbusTcpClient('127.0.0.1', port=8234)
client.connect()
client.write_coil(0, True, 33)
client.write_coil(1, True, 33)


#result = client.read


# send packet from file
with open('Test_Color.ani', 'rb') as f:
    while True:
        packet = f.read(530)

        if not packet:
            #f.seek(0)
            #continue
            client.write_coil(0, False, 33)
            client.write_coil(1, False, 33)
            break

        universe = int(packet[14])

        if universe == 1:

            sock.sendto(packet, server_address1)
            time.sleep(1/40)

        else:
            sock.sendto(packet, server_address2)
