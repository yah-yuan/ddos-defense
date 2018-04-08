import pymysql
import socket

DEBUG = True

class DataOperator(object):
    port = 0
    IPaddr = ''
    status = False

    def __init__(self,click:Click.Click = ''):
        if DEBUG:
            self.port = 33333
            self.IPaddr = '192.168.3.128'
        else:
            self.port = click.dataPort
            self.IPaddr = click.IPaddr
        self.socket = socket.socket()
        self.socket.connect((self.IPaddr,self.port))
        recvMessage = self.socket.recv(1024)
        if b'Click::ControlSocket/1.3' in recvMessage:
            print(recvMessage)
    
    def GetData(self):
        self.socket.send(b'CHECKREAD')
        recvMessage = self.socket.recv(65535)
        print(recvMessage.decode('utf8'))

if __name__ == '__main__':
    data = DataOperator()
    data.GetData()