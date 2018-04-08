from ControlSocket import ControlSocket
from Config import ConfigWriter

DEBUG = True

class Click(object):
    '''A click object, including all the information
       about a remote click'''
    main_click = False
    online = False
    IPaddr = ''
    controlPort = 11111
    dataPort = 33333
    ddosservice = ['NAT','UDP','syn flood']
    config = 'default config'
    configPath = './config/'

    def __init__(self,name,ipaddr,controlPort = 22222,dataPort = 33333):
        if name == 'main_click':
            self.main_click = True
        if DEBUG == True:
            ipaddr = '192.168.3.135'
        self.ipaddr = ipaddr
        self.controller = ControlSocket(self)
        self.writer = ConfigWriter(self)
        self.datapipe = None
        self.online = True

    def ChangeConfig(self):
        if DEBUG:
            self.controller.HotConfig('config/ddos.click')
            self.controller.Close()
        # path = self.writer.write_new_config(controlPort,ddosservice)
        # if self.controller.HotConfig(path):
        #     return False
        # elif:
        #     return False
        # self.controller.Close()

    def CloseClick(self):
        pass

def main():
    click = Click('test','192.168.4.130')
    click.ChangeConfig()
    