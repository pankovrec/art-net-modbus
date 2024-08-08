
import socket
import time

# create udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# artnet device config
server_address1 = ('localhost', 6454)
server_address2 = ("localhost", 6455)
fps = 40

# send packet from file
with open('Test_Color.ani', 'rb') as f:
    while True:
        packet = f.read(530)
    #    print(packet)
      #
        if not packet:
            f.seek(0)
            continue
        universe = int(packet[14])

        print(universe)

        if universe == 1:

            sock.sendto(packet, server_address1)
            time.sleep(1 / fps)

        else:
            sock.sendto(packet, server_address2)
            time.sleep(1 / fps)
