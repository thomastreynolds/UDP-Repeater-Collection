# UDP Repeater Collection
Python scripts to receive UDP packets and sends them to multiple destinations.  These are intended primarily to work with WSJT-X.

## UDP Repeater SendRx Multicast
A Python script to receive UDP packets from WSJT-X and "repeat" them to multiple destinations.  It will also receive messages coming back from that destination and forward them back to WSJT-X.

This version will work with WSJT-X when configured in Multicast mode.  The default multicast group is 224.0.0.1.  Others can be used by editing MCAST_GRP value.  Edit the values for txAddress1 to txAddress5 to reflect the IP of the destinations.
