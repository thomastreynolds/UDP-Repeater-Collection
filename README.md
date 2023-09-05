# UDP Repeater Collection
Python scripts to receive UDP packets and sends them to multiple destinations.  These are intended primarily to work with WSJT-X.

There are three branches:
1) UDP-Repeater-Basic - receives a packet and sends it out to multiple destination.
2) UDP-Repeater-SendRx - same as -Base but also receives packets from destination and routes them back to the source.
3) UDP-Repeater-SendRx-Multicast - same as -SendRx but workes when WSJT-X is configured for multicast.

