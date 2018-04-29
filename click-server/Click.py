from ControlSocket import ControlSocket
from Config import ConfigWriter
import os

DEBUG = True

class Click(object):
    '''A click object, including all the information
       about a remote click'''
    main_click = False
    online = False
    IPaddr = ''
    ddosservice = ['NAT','UDP','syn flood']
    config = 'default config'
    configPath = './config/'

    def __init__(self,name,ipaddr,controlPort = 22222,dataPort = 33333):
        if name == 'main_click':
            self.main_click = True
        if DEBUG:
            ipaddr = '192.168.3.136'
        self.IPaddr = ipaddr
        self.controlPort = controlPort
        self.dataPort = dataPort
        self.controller = ControlSocket(self)
        self.writer = ConfigWriter(self)
        self.datapipe = None
        self.online = True

    def ChangeConfig(self):
        if DEBUG:
            self.controller.HotConfig('config/router.click',22223)
            self.controller.Close()
        else:
            if self.controlPort == 22222:
                newPort = self.controlPort + 1
            else:
                newPort = self.controlPort - 1
            if self.controller.HotConfig(name+'_newconfig.click'):
                return True
            elif:
                return False
            self.controller.Close()

    def CloseClick(self):
        pass

    def CreateConfig(self, strategy):
        if self.controlPort == 22222:
            port = self.controlPort + 1
        else:
            port = self.controlPort - 1
        newconfig = self.writer.NewConfig(strategy,controlport)
        self.newconfig = newconfig
        file = open(name+'_newconfig.click','wb+')
        file.write(newconfig)
        file.close()
        return newconfig
        pass

def main():
    click = Click('test','192.168.4.130')
    click.ChangeConfig()
    
if __name__ == '__main__':
    main()