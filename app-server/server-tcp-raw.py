import socket
import struct
import binascii

rawSocket = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
# while True:
#     pkt = rawSocket.recvfrom(2048)

#     ethernetHeader = pkt[0][0:14]   #提取以太网帧头
#     eth_hdr = struct.unpack("!6s6s2s",ethernetHeader) #6字节目的mac地址，6字节源mac地址，2字节协议类型
#     print(eth_hdr[0],eth_hdr[1],eth_hdr[2])
#     binascii.hexlify(eth_hdr[0])
#     binascii.hexlify(eth_hdr[1])
#     binascii.hexlify(eth_hdr[2])

#     ipHeader = pkt[0][14:34]        #提取IP协议头，不包含option和padding字段。
#     ip_hdr = struct.unpack("!12s4s4s",ipHeader)         # ！标示转换网络字节序，前12字节为版本、头部长度、服务类型、总长度、标志等其他选项，后面的两个四字节依次为源IP地址和目的IP地址。

#     print("source IP address: " + socket.inet_ntoa(ip_hdr[1]))

#     print("destination IP address: " + socket.inet_ntoa(ip_hdr[2]))

#     tcpHeader = pkt[0][34:54]
#     tcp_hdr = struct.unpack("!HH16s",tcpHeader)

#     print( tcp_hdr)
#     if tcp_hdr[0] != 33333:
#         continue

#     socket.