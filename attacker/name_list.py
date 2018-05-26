# -*- coding: utf-8 -*
'''
	A very simple raw socket implementation in Python
'''
import random
import sys, socket
from struct import *

RANDOM = True
using_pool = 'black'
ip_source = '127.0.0.1'
ip_dest = '127.0.0.1'
black_ip_pool = ('10.3.152.132','32.1.21.90')
white_ip_pool = ('231.213.20.12','98.123.21.54')
ip_pool = {'black':black_ip_pool,'white':white_ip_pool}

def ip_random():
    ip = ''
    for i in range(4):
        num = random.randint(0,255)
        ip += str(num)
        if i != 3:
            ip += '.'
    return ip

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (ord(msg[i]) << 8 ) + ord(msg[i+1])
        s = carry_around_add(s, w)
    return ~s & 0xffff

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
def icmp_pack(_ip_source):
    # ip_dest = '127.0.0.1'	#也可以用域名：socket.gethostbyname('www.microsoft.com')
    ip_source = _ip_source
    #填写ip header
    ip_ver = 4			# ipv4
    ip_ihl = 5			# Header Length =5, 表示无options部分
    ip_dscp = 0			# 以前叫tos，现在叫dscp
    ip_total_len = 0		# left for kernel to fill
    ip_id = 22222			# fragment相关，随便写个
    ip_frag_offset = 0		# fragment相关
    ip_ttl = 255			# *nix下TTL一般是255
    ip_protocol = socket.IPPROTO_ICMP	# 表示后面接的是icmp数据
    ip_checksum = 0			# left for kernel to fill
    ip_saddr = socket.inet_pton(socket.AF_INET, ip_source)	# 两边的ip地址
    ip_daddr = socket.inet_pton(socket.AF_INET, ip_dest)

    ip_ver_ihl = (ip_ver << 4) + ip_ihl	# 俩4-bit数据合并成一个字节

    # 按上面描述的结构，构建ip header。
    ip_header = pack('!BBHHHBBH4s4s' , ip_ver_ihl, ip_dscp, ip_total_len, ip_id, ip_frag_offset, ip_ttl, ip_protocol, ip_checksum, ip_saddr, ip_daddr)

    # 回显请求的icmp包构造
    icmp_type = 8
    icmp_code = 0
    icmp_cksum = 0

    icmp_id = 1232 # 一般是进程id
    icmp_seq = 1
    icmp_data = 'sdfd'

    # 继续合并small fields
    # 没有要合并的东西
    # tcp_offset_reserv = (tcp_data_offset << 4)
    # tcp_flags = tcp_flag_fin + (tcp_flag_syn << 1) + (tcp_flag_rst << 2) + (tcp_flag_psh <<3) + (tcp_flag_ack << 4) + (tcp_flag_urg << 5)

    # 按上面描述的结构，构建icmp header。icmp_type
    icmp_header = pack('!BBHHH4s' , icmp_type,icmp_code,icmp_cksum,icmp_id,icmp_seq,icmp_data)

    # 写点东西作为data部分(可选)
    # payload_data = 'wordpress.youran.me'

    # 构建pseudo ip header
    # 这是所谓的tcp伪头部
    # psh_saddr = ip_saddr
    # psh_daddr = ip_daddr
    # psh_reserved = 0
    # psh_protocol = ip_protocol
    # psh_tcp_len = len(icmp_header)
    # psh = pack('!4s4sBBH', psh_saddr, psh_daddr, psh_reserved, psh_protocol, psh_tcp_len)

    # 创建最终用于checksum的内容
    chk = icmp_header

    # 必要时追加1字节的padding
    if len(chk) % 2 != 0:
        chk += '\0'

    icmp_cksum = checksum(chk)

    # 重新构建icmp header，把checksum结果填进去

    icmp_header = pack('!BBHHH4s' , icmp_type,icmp_code,icmp_cksum,icmp_id,icmp_seq,icmp_data)
    # 最终的tcp/ip packet！
    packet = ip_header + icmp_header
    return packet
# 发送出去

def send(n):
    ip_source = ip_pool[using_pool][0]
    pack1 = icmp_pack(ip_source)
    ip_source = ip_pool[using_pool][1]
    pack2 = icmp_pack(ip_source)
    for i in range(n):
        if i%2:
            packet = pack1
        else:
            packet = pack2
        s.sendto(packet, (ip_dest, 0))

if __name__ == '__main__':
    send(12)