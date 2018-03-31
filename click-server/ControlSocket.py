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

class ControlSocket(object):
    '''Operate a remote click by its handlers.
       This class will create a socket connect to the click.'''

    def __init__(self, click = None):
        # addr = (click.ipaddr, click.controlPort)
        addr = ('192.168.3.128', 8888)
        self.con = socket.socket()
        try:
            self.con.connect(addr)
        except ConnectionRefusedError as e:
            raise ControlSocketError('remote click is currently not online')
        recvMessage = self.con.recv(1024)
        print(recvMessage)
        if b'Click::ControlSocket/1.3' in recvMessage:
            # return self
            pass
        else:
            raise ControlSocketError('Remote click ERROR')
        self.con.send(b'READ config\n')
        recv = self.con.recv(51231)
        print(recv.decode('utf8'))

    def HotConfig(self, configfile):
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
        try:
            file = open(configfile)
        except Exception as e:
            raise ControlSocketError(e)
        config ='WRITE hotconfig ' + file.read()
        file.close()
        config =config.encode('utf8')

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

class ControlSocketError(Exception):
    def __init__(self,e):
        if isinstance(e,str):
            self.value = e
        else:
            self.value = repr(e)
    def __str__(self):
        return self.value

if __name__ == '__main__':
    con = ControlSocket()
    