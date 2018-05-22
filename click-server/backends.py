import json
import re
import socket as sock
import threading

DEBUG = True
TYPE = {
    0:'REQUEST_GLOBLE_FLOW',
    1:'REQUEST_STRATEGY_LIST',
    2:'REQUEST_DETAILED_CONFIG',
    3:'REQUEST_IP_FLOW',
    4:'SUBMMIT_STRATEGY_LIST',
    5:'REQUEST_CLICK_LIST',
    6:'REQUEST_CLICK_DETAIL',
    7:'SUBMMIT_ADD_NEW_CLICK',
    8:'SUBMMIT_DEL_OLD_CLICK'
}

def json_unpack(packet):
    json_out = json.loads(packet)
    return json_out

def json_pack(messege):
    json_out = json.dumps(messege)
    return json_out

class Backends(object):
    '''提供前端可用的数据接口,通过socket通信'''
    def __init__(self,manager):
        addr = ('127.0.0.1', 54545)
        socket = sock.socket()
        socket.bind(addr)
        socket.listen(5)
        self.socket = socket
        self.manager = manager

    def run(self):
        while True:
            con,addr = self.socket.accept()
            self.Listener(con)
        
        # recv = socket.recv(1024)
        # if b'Con succeed' in recv:
        #     self.socket = socket
        #     # threading.Thread(target=self.Listener)
        #     self.Listener()
    def Listener(con):
        socket = con
        while True:
            recv = socket.recv()
            recv = recv.decode('utf8')
            request = json_pack(recv)
            requst_type = request['type']
            if request == 0:
                # 'REQUEST_GLOBLE_FLOW'
                pass
            if request == 1:
                # 'REQUEST_STRATEGY_LIST'
            if request == 2:
                # 'REQUEST_DETAILED_CONFIG'
            if request == 3:
                # 'REQUEST_IP_FLOW'
            if request == 4:
                # 'SUBMMIT_STRATEGY_LIST'
            if request == 5:
                # 'REQUEST_CLICK_LIST'
            if request == 6:
                # 'REQUEST_CLICK_DETAIL'
            if request == 7:
                # 'SUBMMIT_ADD_NEW_CLICK'
            if request == 8:
                # 'SUBMMIT_DEL_OLD_CLICK'


    def Readflow(self,interval, amount):
        '''json'''
        data = self.manager.Readflow(interval, amount)
        json_text = json.dump(data)
        if DEBUG:
            print(json_te)
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

if __name__ == '__main__':
    file = open('test.json')
    content = file.read(-1)
    out = json_unpack(content)
    print(type(out['type']))