# UDP Repeater Collection
Python scripts to receive UDP packets and sends them to multiple destinations.  These are intended primarily to work with WSJT-X.

## UDP Repeater SendRx
A Python script to receive UDP packets from WSJT-X and "repeat" them to multiple destinations.  It will also receive messages coming back from that destination and forward them back to WSJT-X.

This version will work with WSJT-X with default configuration (127.0.0.1 port 2237).  Others can be used by editing rxAddress value.  Edit the values for txAddress1 to txAddress5 to reflect the IP of the desired destinations.
