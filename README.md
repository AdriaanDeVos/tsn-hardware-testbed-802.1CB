# tsn-hardware-testbed-802.1CB
Contains configuration files and scripts to perform Time-Sensitive Networking tests on a hardware testbed. Specifically the IEEE 802.1CB specification.

## TCPDUMP
tcpdump -i eth0 -vv -e -nn

## Crontab to find the rPi
The hardware testbed is remotely accessible while running in the TU Delft building. It does not have a hostname and therefore the IP address might change. I have used the following cronjob to always be able to find it:

```* * * * * /usr/bin/curl -I https://adriaandevos.nl/here-i-am/$(/usr/bin/curl ifconfig.me) >/dev/null 2>&1```
