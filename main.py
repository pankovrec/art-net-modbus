
import socket


# create udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# artnet device config
server_address1 = ('192.168.0.99', 6454)
server_address2 = ("192.168.0.100", 6454)


# send packet from file
with open('Test_Color.ani', 'rb') as f:
    while True:
        packet = f.read(1000)
      #
        if not packet:
            f.seek(0)
            continue
        universe = int(packet[14])

        if universe == 1:

            sock.sendto(packet, server_address1)

        else:
            sock.sendto(packet, server_address2)
