# Documentation: https://github.com/secdev/scapy
# More: https://scapy.readthedocs.io/en/latest/api/scapy.packet.html
# More: https://scapy.readthedocs.io/en/latest/api/scapy.layers.l2.html
# More: https://scapy.readthedocs.io/en/latest/build_dissect.html
# Page 49 of the IEEE 802.1CB standard

import copy

from scapy.compat import raw
from scapy.data import ETHER_TYPES, ETH_P_IP
from scapy.fields import ShortField, XShortEnumField
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP
from scapy.packet import Packet, bind_layers
from scapy.sendrecv import sniff


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


# Should be 0xF1C1, but its 0x2345 on NXP
class RedundancyTag(Packet):
    name = "RedundancyTag"
    fields_desc = [
        ShortField("SequenceNumber", 0),
        XShortEnumField("type", 0x0800, ETHER_TYPES)
    ]


bind_layers(Ether, RedundancyTag, type=0x2345)
bind_layers(RedundancyTag, IP, type=ETH_P_IP)

sniff(iface="eth1", prn=Ether.show)
