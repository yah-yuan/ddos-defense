from ControlSocket import ControlSocket
from Config import ConfigWriter

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
            ipaddr = '192.168.3.135'
        self.IPaddr = ipaddr
        self.controlPort = controlPort
        self.dataPort = dataPort
        self.controller = ControlSocket(self)
        self.writer = ConfigWriter(self)
        self.datapipe = None
        self.online = True

    def ChangeConfig(self):
        if DEBUG:
            self.controller.HotConfig('config/ddos.click',22223)
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
    
if __name__ == '__main__':
    main()