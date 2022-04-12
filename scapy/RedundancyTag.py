from scapy.data import ETHER_TYPES, ETH_P_IP
from scapy.fields import ShortField, XShortEnumField
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP
from scapy.packet import Packet, bind_layers
from scapy.compat import raw
import copy


class RedundancyTag(Packet):
    """Define the fields contained in the Redundancy Tag"""
    name = "RedundancyTag"
    fields_desc = [
        ShortField("sequence_number", 0),
        XShortEnumField("type", 0x0800, ETHER_TYPES)
    ]


def decap(orig_pkt):
    """Decapsulate a FRER frame."""
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


"""Bind the RedundancyTag layer to the Ether layer"""
bind_layers(Ether, RedundancyTag, type=0x2345)  # Should be 0xF1C1, but its 0x2345 on NXP
bind_layers(RedundancyTag, IP, type=ETH_P_IP)
