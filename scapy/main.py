from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether, Dot1Q
from scapy.sendrecv import sendp
import time

a = Ether(src="6c:5a:b0:b3:a2:c6", dst="61:64:72:69:61:6e") / IP(src="10.0.0.1", dst="10.0.0.2")

while True:
    sendp(a, iface="eth1")
    time.sleep(5)
