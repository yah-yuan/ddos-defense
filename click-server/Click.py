import os

from Config import ConfigWriter
from ControlSocket import ControlSocket
from define import *

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
            listen_ether,net_controlPort,net_dataPort):
        if name == 'main_click':
            self.main_click = True
        if DEBUG:
            ipaddr = '192.168.3.136'
        self.name = name
        self.IPaddr = con_ipaddr
        self.controlPort = net_controlPort
        self.dataPort = net_dataPort
        self.using_port = 0
        self.controller = ControlSocket(con_ipaddr,net_controlPort[self.using_port])
        self.writer_controlPort = (8081,8082)
        self.writer_dataport = 8083
        self.writer = ConfigWriter(self.writer_controlPort,listen_ipaddr,app_server_ip,listen_broadcast,listen_device,listen_ether)
        self.datapipe = None
        self.online = True

    def ChangeConfig(self):
        config = open('./newconfig/'+self.name+'.click','r').read(-1)
        if self.using_port == 0:
            new_net_port = self.controlPort[1]
        else:
            new_net_port = self.controlPort[2]
        if self.controller.HotConfig(config,new_net_port):
            if self.using_port == 0:
                self.using_port = 1
            else:
                self.using_port = 0
            print(self.name,' hot swap succeed')
            return True
            # self.controlPort = self.newControlPort
            # return True
        else:
            return '更改配置失败'

    def CloseClick(self):
        self.controller.Close()
        os.remove('')

    def CreateConfig(self, strategy):
        if self.using_port == 0:
            controlPort = self.controlPort[1]
        else:
            controlPort = self.controlPort[0]
        newconfig = self.writer.NewConfig(controlPort,strategy,[],self.name)
        self.newconfig = newconfig
        file = open('./newconfig/'+self.name+'.click','w+')
        file.write(newconfig)
        file.close()
        return newconfig

# def main():
#     click = Click('test','192.168.4.130')
#     click.ChangeConfig()
    
# if __name__ == '__main__':
#     main()
