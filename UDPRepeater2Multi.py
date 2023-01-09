#!/usr/bin/python3
import socket
import sys
import select
import sys, array
import struct

if sys.platform.startswith('win'):
  isWin32 = True
else:
  isWin32 = False
  import tty
  import termios   # for SetRawMode() and RemoveRawMode(), only for Linux
  import fcntl

OriginalTTYSettings = 0
MCAST_GRP = '224.0.0.1'
MCAST_PORT = 2237
RX_PORT2 = 55222

def SetRawMode():
  global OriginalTTYSettings

  fd = sys.stdin.fileno()
  OriginalTTYSettings = termios.tcgetattr(fd)
  tty.setcbreak(fd)
  #tty.setraw(fd)   # for my purpose there doesn't seem to be much difference between cbreak and raw mode


def RemoveRawMode():
  fd = sys.stdin.fileno()
  termios.tcsetattr(fd, termios.TCSANOW, OriginalTTYSettings)


#
#
#  Main program
#
#

#   The purpose of these four lines is to gather this computer's IP (not 127.0.0.1).
sss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sss.connect(("10.10.1.1", 80))    # ip address is not important.  It doesn't attempt to send any data
myIP = sss.getsockname()[0]
sss.close()
print("Starting up on "+myIP)

rxAddress = (MCAST_GRP, MCAST_PORT)
rxAddress2 = (myIP, RX_PORT2)

txAddress1 = ('192.168.1.57', 2237)     # <---- PLACE YOUR FIRST phone's IP address here, replacing 192.168.1.57.
txAddress2 = ('192.168.1.211', 2237)    # <---- PLACE YOUR SECOND phone's IP address here, replacing 192.168.1.57.
#txAddress3 = ('192.168.1.163', 9090)    # Other
#txAddress4 = ('192.168.1.131', 2237)    #   programs
#txAddress5 = ('192.168.1.209', 2237)    #     or
#txAddress6 = ('192.168.1.196', 9090)    #       devices

totalPackets=0

# Create the UDP sockets

# sockTx is for sending data to anyplace except myIP
sockTx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockTx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockTx.bind( ('0.0.0.0',RX_PORT2))                            # do this to force the source port to be RX_PORT2

# sock is for listening to WSJT-X
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# sock2 is for listening to messages coming back from any Android device.
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to the port
print('listening on %s port %s' % rxAddress)
sock.bind(('', MCAST_PORT))
# Tell the operating system to add the socket to the multicast group on all interfaces.
group = socket.inet_aton(MCAST_GRP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print('listening on %s port %s' % rxAddress2)
sock2.bind(rxAddress2)

if (isWin32):
    inputs = [ sock, sock2 ]
else:
    SetRawMode()
    inputs = [ sock, sock2, sys.stdin ]

running = 1
while running == 1:
    print('\nwaiting to receive message')
    readfds, writefds, errorfds = select.select( inputs, [], inputs )

    if errorfds != []:      # abort on any error
        print("Error on select()")
        running = 0
        continue

    for s in readfds:
        buf = array.array('I',[0])
        if s == sys.stdin:
            #fcntl.ioctl( sys.stdin, termios.TIOCINQ, buf, True)  # This line works in Linux but not in Cygwin.  It doesn't work at all in Win32 (command window).
            ch = sys.stdin.read(buf[0])
            running = 0
            break
        elif s == sock:
            data, addressWSJT = sock.recvfrom(4096)

            totalPackets+=1
            print('received %s bytes from %s ... packet #%d' % (len(data), addressWSJT, totalPackets))

            if data:
                sent = sockTx.sendto(data, txAddress1)
                print('sent %s bytes back to %s' % (sent, txAddress1))
                sent = sockTx.sendto(data, txAddress2)
                print('sent %s bytes back to %s' % (sent, txAddress2))
                #sent = sockTx.sendto(data, txAddress3)
                #print('sent %s bytes back to %s' % (sent, txAddress3))
                #sent = sockTx.sendto(data, txAddress4)
                #print('sent %s bytes back to %s' % (sent, txAddress4))
                #sent = sockTx.sendto(data, txAddress5)
                #print('sent %s bytes back to %s' % (sent, txAddress5))
                #sent = sockTx.sendto(data, txAddress6)
                #print('sent %s bytes back to %s' % (sent, txAddress6))

        elif s == sock2:
            data, addressAndroid = sock2.recvfrom(4096)
            print('    received %s bytes from %s ... packet #%d' % (len(data), addressAndroid, totalPackets))

            if data:
                sent = sockTx.sendto(data, addressWSJT)
                print('    Reply sent %s bytes back to %s' % (sent, addressWSJT))

if (isWin32 == False):
    RemoveRawMode()

sys.exit()

