import socket
import threading
import re

class Backends(object):
    '''提供前端可用的数据接口,通过socket通信'''
    def __init__(self,manager):
        addr = ('127.0.0.1', 54545)
        socket = socket.socket()
        socket.connect(addr)
        socket.send(b'Con succeed!\n')
        recv = socket.recv(1024)
        if b'Con succeed' in recv:
            self.socket = socket
            threading.Thread(target=self.Listener)
    def Listener(self):
        while True:
            recv = self.socket.recv()
            recv = recv.decode('utf8')
            if 'flow data' in recv:
                # eg: 'flow data interval: 1, amount: 100' 间隔(s),数据个数
                interval = int(re.search('\d+',re.search('interval:.+?\d+',recv).group()).group())
                amount = int(re.search('\d+',re.search('amount:.+?\d+',recv).group()).group())
                self.Readflow(interval,amount)

    def Readflow(self,interval, amount):
        pass