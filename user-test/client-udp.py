import socket 
import time 
    
address = ('192.168.3.128', 33333)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    
while True: 
    s.sendto(b'Hey there, this is a UDP flow', address)  
    time.sleep(1)