import os

from Config import ConfigWriter
from ControlSocket import ControlSocket

DEBUG = False

class Click(object):
    '''A click object, including all the information
       about a remote click'''
    main_click = False
    online = False
    IPaddr = ''
    ddosservice = ['NAT','UDP','syn flood']
    config = 'default config'
    configPath = './config/'

    def __init__(self,name,con_ipaddr,listen_ipaddr,\
            app_server_ip,listen_broadcast,listen_device,\
            listen_ether,controlPort = 22222,dataPort = 33333):
        if name == 'main_click':
            self.main_click = True
        if DEBUG:
            ipaddr = '192.168.3.136'
        self.name = name
        self.IPaddr = con_ipaddr
        self.controlPort = controlPort
        self.dataPort = dataPort
        self.controller = ControlSocket(con_ipaddr,controlPort)
        self.writer = ConfigWriter(controlPort,listen_ipaddr,app_server_ip,listen_broadcast,listen_device,listen_ether)
        self.datapipe = None
        self.online = True

    def ChangeConfig(self):
        config = open('./newconfig/'+name+'_newconfig.click').read(-1)
        if self.controller.HotConfig(config,self.newControlPort):
            self.controlPort = self.newControlPort
            return True
        else:
            return '更改配置失败'

    def CloseClick(self):
        self.controller.Close()
        os.remove('')

    def CreateConfig(self, strategy):
        if self.controlPort != self.newControlPort:
            pass
        else:
            if self.controlPort == 22222:
                self.newControlPort = 22223
            else:
                self.newControlPort = 22222
        newconfig = self.writer.NewConfig(controlport,strategy,)
        self.newconfig = newconfig
        file = open('./newconfig/'+name+'_newconfig.click','wb+')
        file.write(newconfig)
        file.close()
        return newconfig
        pass

def main():
    click = Click('test','192.168.4.130')
    click.ChangeConfig()
    
if __name__ == '__main__':
    main()
