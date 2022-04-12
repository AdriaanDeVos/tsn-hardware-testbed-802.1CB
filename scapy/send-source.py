from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp
import time

a = Ether(src="6c:5a:b0:b3:a2:c6", dst="61:64:72:69:61:6e") / IP(src="10.0.0.1", dst="10.0.0.2") / "Keep On Driving..."

while True:
    sendp(a, iface="eth2")
    time.sleep(1)


# SOURCE pi-eth2 -> switch-swp2
# DESTINATION pi-eth1 -> siwtch-swp2
