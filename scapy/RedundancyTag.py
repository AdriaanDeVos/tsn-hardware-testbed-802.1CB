from scapy.data import ETHER_TYPES, ETH_P_IP
from scapy.fields import ShortField, XShortEnumField
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP
from scapy.packet import Packet, bind_layers


class RedundancyTag(Packet):
    """Define the fields contained in the Redundancy Tag"""
    name = "RedundancyTag"
    fields_desc = [
        ShortField("SequenceNumber", 0),
        XShortEnumField("type", 0x0800, ETHER_TYPES)
    ]


"""Bind the RedundancyTag layer to the Ether layer"""
bind_layers(Ether, RedundancyTag, type=0x2345)  # Should be 0xF1C1, but its 0x2345 on NXP
bind_layers(RedundancyTag, IP, type=ETH_P_IP)
