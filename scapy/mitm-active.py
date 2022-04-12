# Documentation: https://github.com/secdev/scapy
# More: https://scapy.readthedocs.io/en/latest/api/scapy.packet.html
# More: https://scapy.readthedocs.io/en/latest/api/scapy.layers.l2.html
# More: https://scapy.readthedocs.io/en/latest/build_dissect.html
# Page 49 of the IEEE 802.1CB standard

import time
import sys

from RedundancyTag import RedundancyTag
from scapy.sendrecv import bridge_and_sniff


def determine_attack():
    """
    This function determines the attack that will be performed.
    """
    attack = 0
    if len(sys.argv) > 1:
        try:
            attack = int(sys.argv[1])
        except ValueError:
            print("Invalid attack number. Defaulting to passive mode.")
    else:
        print("No attack number provided. Defaulting to passive mode.")

    if attack == 1:
        return passive
    else:
        print("Passive mode is enabled.")
        return passive


def determine_redundancy_tag(pkt):
    """
    This function determines the redundancy tag of the packet.
    """
    if pkt.haslayer(RedundancyTag):
        return True
    else:
        return False


def passive(pkt):
    """
    This function is the passive mode.
    """
    pkt.show()
    return determine_redundancy_tag(pkt)


attack_method = determine_attack()
time.sleep(1)

bridge_and_sniff(if1="eth0", if2="eth1", xfrm12=attack_method)
