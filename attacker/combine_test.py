from echo_test import * 
from icmp_test import * 
from rst_test import * 
import random

IP_RANDOM = True
SRC_PORT_RANDOM = True
ip_dest = '127.0.0.1'
ip_source = '127.0.0.1'
SEND_TIMES = 100000

def send_pack():
    ip_pool = '10.3.152.132','32.1.21.90','231.213.20.12','98.123.21.54'

    for _ in range(SEND_TIMES):
        roll = random.randint(0,2)
        if roll == 0:
            pack = echo_test.udp_pack()
        elif roll == 1:
            pack = echo_test.udp_pack()
        elif roll == 2:
            pack = echo_test.udp_pack()