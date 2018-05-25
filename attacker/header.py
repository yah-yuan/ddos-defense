import socket
import random

SEND_BUF_SIZE = 4096  
RECV_BUF_SIZE = 4096

def modify_buff_size():  
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )  
        
    # Get the size of the socket's send buffer  
    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)  
    print( "Buffer size [Before]:%d" %bufsize  )
        
    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)  
    sock.setsockopt(  
            socket.SOL_SOCKET,  
            socket.SO_SNDBUF,  
            SEND_BUF_SIZE)  
    sock.setsockopt(  
            socket.SOL_SOCKET,  
            socket.SO_RCVBUF,  
            RECV_BUF_SIZE)  
    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)  
    print( "Buffer size [After]:%d" %bufsize  )

def ip_random():
    ip = ''
    for i in range(4):
        num = random.randint(0,255)
        ip += str(num)
        if i != 3:
            ip += '.'
    return ip

def port_random():
    return random.randint(0,65535)