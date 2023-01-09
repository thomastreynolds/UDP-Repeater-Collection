#!/usr/bin/python3
import socket
import sys

rxAddress = ('127.0.0.1', 2237)
txAddress1 = ('192.168.1.57', 2237)         # <--- enter the IP address of your android devices here.
txAddress2 = ('192.168.1.211', 2237)        #    in these four lines (the four numbers in single quotes,
txAddress3 = ('192.168.1.197', 2237)        #    separated by column).  The 2237 is the port number.  No
txAddress4 = ('192.168.1.104', 2237)        #    need to change it unless you changed it in WSJT-X Monitor.

totalPackets=0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # socket for receiving UDP data
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # for sending UDP data

print('starting up on %s port %s' % rxAddress)              # Bind the rx socket to the rx port
sock.bind(rxAddress)

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    totalPackets+=1
    print('received %s bytes from %s ... packet #%d' % (len(data), address, totalPackets))
    if data:
        sent = sock2.sendto(data, txAddress1)
        print('sent %s bytes back to %s' % (sent, txAddress1) )
        sent = sock2.sendto(data, txAddress2)
        print('sent %s bytes back to %s' % (sent, txAddress2) )
        sent = sock2.sendto(data, txAddress3)
        print('sent %s bytes back to %s' % (sent, txAddress3) )
        sent = sock2.sendto(data, txAddress4)
        print('sent %s bytes back to %s' % (sent, txAddress4) )
