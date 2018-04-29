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
            # threading.Thread(target=self.Listener)
            self.Listener()
    def Listener(self):
        while True:
            recv = self.socket.recv()
            recv = recv.decode('utf8')
            if 'flow data' in recv:
                # eg: 'flow data interval: 1, amount: 100' 间隔(s),数据个数
                interval = int(re.search('\d+',re.search('interval:.+?\d+',recv).group()).group())
                amount = int(re.search('\d+',re.search('amount:.+?\d+',recv).group()).group())
                self.Readflow(interval,amount)
            elif 'new strategy' in recv:
                pass
                # 商定数据结构
            elif 'submmit config' in recv:
                

    def Readflow(self,interval, amount):
        '''json'''
        pass

    def CreateConfig(self,strategy):
        '''根据选择的策略创建config文件'''
        newConfig = self.manager.Create_config(strategy)
        self.socket.send(newConfig.encode('utf8'))

    def Submit(self):
        '''提交更改'''
        res = self.manager.Change_config()
        if res != 'SUCCESS':
            self.socket.send(b'error')
            # 应将config恢复到之前的状态
        else:
            self.socket.send(b'success')