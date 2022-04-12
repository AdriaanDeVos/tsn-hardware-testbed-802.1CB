# Documentation: https://github.com/secdev/scapy
# More: https://scapy.readthedocs.io/en/latest/api/scapy.packet.html
# More: https://scapy.readthedocs.io/en/latest/api/scapy.layers.l2.html
# More: https://scapy.readthedocs.io/en/latest/build_dissect.html
# Page 49 of the IEEE 802.1CB standard

import copy
import time

from RedundancyTag import RedundancyTag
from scapy.compat import raw
from scapy.layers.l2 import Ether
from scapy.sendrecv import AsyncSniffer


def decap(orig_pkt):
    """decapsulate a FRER frame (WIP NEEDS TESTING)"""
    if not isinstance(orig_pkt, Ether) or \
            not isinstance(orig_pkt.payload, RedundancyTag):
        raise TypeError(
            'cannot decapsulate FRER packet, must be Ethernet/FRER'
        )
    packet = copy.deepcopy(orig_pkt)
    prev_layer = packet[RedundancyTag].underlayer
    prev_layer.type = packet[RedundancyTag].type
    next_layer = packet[RedundancyTag].payload
    del prev_layer.payload
    if prev_layer.name == Ether().name:
        return Ether(raw(prev_layer / next_layer))
    return prev_layer / next_layer


"""Sniff all incoming packets"""
sniffer = AsyncSniffer(iface="eth1", prn=Ether.show)
sniffer.start()

while True:
    time.sleep(1)
