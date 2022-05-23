# Documentation: https://github.com/secdev/scapy
# More: https://scapy.readthedocs.io/en/latest/api/scapy.packet.html
# More: https://scapy.readthedocs.io/en/latest/api/scapy.layers.l2.html
# More: https://scapy.readthedocs.io/en/latest/build_dissect.html
# Page 49 of the IEEE 802.1CB standard

import time

from RedundancyTag import RedundancyTag
from scapy.layers.inet import IP
from scapy.packet import Raw
from scapy.sendrecv import AsyncSniffer

counter = None


def print_raw(pkt):
    global counter
    if pkt.haslayer(Raw) and pkt[IP].dst == "10.0.0.2":
        payload = pkt[Raw].load.decode("utf-8").rstrip('\x00')
        payload_counter = int(payload.split()[0])
        output = payload
        if counter is not None:
            if (counter + 1) != payload_counter or "Stop" in payload:
                output += " <- Possible attack detected!"
        counter = payload_counter
        print(output)


"""Sniff all incoming packets"""
sniffer = AsyncSniffer(iface="eth1", prn=print_raw)
sniffer.start()

while True:
    time.sleep(1)
