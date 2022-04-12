# Documentation: https://github.com/secdev/scapy
# More: https://scapy.readthedocs.io/en/latest/api/scapy.packet.html
# More: https://scapy.readthedocs.io/en/latest/api/scapy.layers.l2.html
# More: https://scapy.readthedocs.io/en/latest/build_dissect.html
# Page 49 of the IEEE 802.1CB standard

import time

from RedundancyTag import RedundancyTag
from scapy.layers.l2 import Ether
from scapy.sendrecv import AsyncSniffer

"""Sniff all incoming packets"""
sniffer = AsyncSniffer(iface="eth1", prn=Ether.show)
sniffer.start()

while True:
    time.sleep(1)
