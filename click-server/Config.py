import re
import Click

class ConfigWriter(object):
    '''Create a .click config file according to
       using router service and ddos defence strategy'''
    def __init__(self,click):
        pass

class ConfigObj(object):
    pass

basic = ''
udp = '-> '
flood = ''
config = udp + flood

def test():
    config = ''
    config += 'CONTROL :: ControlSocket(tcp,8888)\n'
    config += 'define($REMOTEIP 192.168.3.1)\n'
    config += 'out :: Queue(1024) -> ToDevice($IFACENAME);\n'
    config += 'FromDevice($IFACENAME)-> is_ip :: Classifier(12/0800, -);\n'
    config += 'is_ip[0]-> etc0 -> etc1->..... ->etci;'
    config += '-> flood1->flood2-> .... -> out;'
    out;'
    file = open('config/ddos.click','w')
    file.write(config)
    file.close()

if __name__ == '__main__':
    test()
