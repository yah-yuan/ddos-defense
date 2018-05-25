from echo_test import * 
from icmp_test import * 
from rst_test import * 
from random import * 

IP_RANDOM = True
SRC_PORT_RANDOM = True
ip_dest = '127.0.0.1'
ip_source = '127.0.0.1'
SEND_TIMES = 100000

def send_pack():
    echo = echo_test.udp_pack()
    icmp = icmp_test.icmp_pack()
    rst = rst_test.rst_pack()

    for _ in range(SEND_TIMES):
        