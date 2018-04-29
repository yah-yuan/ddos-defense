import socket

CODE_OK = b'200'
CODE_OK_WARN = b'220'
CODE_SYNTAX_ERR = b'500'
CODE_UNIMPLEMENTED = b'501'
CODE_NO_ELEMENT = b'510'
CODE_NO_HANDLER = b'511'
CODE_HANDLER_ERR = b'520'
CODE_PERMISSION = b'530'
CODE_NO_ROUTER = b'540'

DEBUG = True

class ControlSocket(object):
    '''Operate a remote click by its handlers.
       This class will create a socket connect to the click.'''

    def __init__(self, click):
        if DEBUG:
            self.IPaddr = '192.168.2.129'
            self.port = 22222
        else:
            self.IPaddr = click.IPaddr
            self.port = click.controlPort
        addr = (self.IPaddr,self.port)
        self.con = socket.socket()
        try:
            self.con.connect(addr)
        except ConnectionRefusedError as e:
            raise ControlSocketError('remote click is currently not online')
        recvMessage = self.con.recv(1024)
        print(recvMessage.decode('utf8'))
        if b'Click::ControlSocket/1.3' in recvMessage:
            return None
        else:
            raise ControlSocketError('Remote click ERROR')
        # self.con.send(b'READ config\n')
        # recv = self.con.recv(51231)
        # print(recv.decode('utf8'))

    def HotConfig(self, configfile, newPort):
        '''Hot swap the config of the remote click device,
           only when -R param is usable and the new click file can
           be initialed correctly.'''

        # check hot-swap
        try:
            self.con.send(b'CHECKWRITE hotconfig\n')
        except Exception as e:
            raise ControlSocketError(e)
        recvMessage = self.con.recv(65535)
        if CODE_OK not in recvMessage:
            raise ControlSocketError(recvMessage.decode('utf8'))

        # open a click config file
        # try:
        #     file = open(configfile)
        # except Exception as e:
        #     raise ControlSocketError(e)
        # config ='WRITE hotconfig ' + file.read()
        # file.close()
        # config =config.encode('utf8')
        # 直接作为字符串输入
        config = configfile

        # send config
        try:
            self.con.send(config)
        except Exception as e:
            raise ControlSocketError(e)
        recvMessage = self.con.recv(65535)
        if CODE_HANDLER_ERR in recvMessage:
            raise ControlSocketError('Config file can not be initialized!')
        elif CODE_OK not in recvMessage:
            raise ControlSocketError(recvMessage.decode('utf8'))
        else:
            print('Hot-swap succeed')

        self.NewConnect(newPort)

    def NewConnect(self,newPort):
        addr = (self.IPaddr, newPort)
        self.con = socket.socket()
        try:
            self.con.connect(addr)
        except ConnectionRefusedError as e:
            raise ControlSocketError('remote click is currently not online')
        recvMessage = self.con.recv(1024)
        print(recvMessage.decode('utf8'))
        if b'Click::ControlSocket/1.3' in recvMessage:
            print('新connect连接至',str(newPort))
            self.port = newPort
            return None
        else:
            raise ControlSocketError('Remote click ERROR')

    
    def Close(self):
        '''Close this control socket'''
        try:
            self.con.send(b'QUIT\n')
        except Exception as e:
            raise ControlSocketError(e)
        
        recvMessage = self.con.recv(65535)
        if CODE_OK not in recvMessage:
            try:
                self.con.close()
            except Exception as e:
                raise ControlSocketError(e)
            print('Connect is closed successfully')
        else:
            print('Connect is closed successfully')
    
    def WriteHandler(self, name:'[element:]handler',args = ''):
        '''使用任意的handler'''
        self.con.send(b'WRITE '+ name.encode('utf8'))
        recvMessage = self.con.recv(65535)
        print(recvMessage)

    def CheckOnline(self):
        pass
    
    def CheckHandler(self):
        pass

class ControlSocketError(Exception):
    def __init__(self,e):
        if isinstance(e,str):
            self.value = e
        else:
            self.value = repr(e)
    def __str__(self):
        return self.value

if __name__ == '__main__':
    con = ControlSocket('')
    con.WriteHandler('LOG.flush\n')

def test():
    controller = ControlSocket(None)
    controller.Close()

if __name__ == '__main__':
    if DEBUG:
        test()
    else:
        pass