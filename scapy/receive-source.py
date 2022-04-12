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


def print_raw(pkt):
    if pkt.haslayer(Raw) and pkt[IP].dst == "10.0.0.2":
        print(pkt[Raw].load.decode("utf-8").rstrip('\x00'))


"""Sniff all incoming packets"""
sniffer = AsyncSniffer(iface="eth1", prn=print_raw)
sniffer.start()

while True:
    time.sleep(1)
