'''
'rst_attack'
'echo_attack'
'smuf_attack'
'land_attack'
'red'
'''

class ConfigWriter(object):
    def __init__(self,ControlPort,IpDst,IpSrc:list,IpBrodCast):
    #basic
        self.Control = 'CONTROL :: ControlSocket(tcp,'+str(ControlPort)+')\n'
        self.Out_default   = 'out :: Queue(1024) -> ToDevice(ens33)\n'
        self.Out_red = 'out :: RED(768,1024,0.02)->Queue(1024) -> ToDevice('+IpDst+')\n'
        self.Is_ip   ='FromDevice(ens37)-> is_ip :: Classifier(12/0800, -)\n'
        self.Not_ip  ='is_ip[1]->out\n'
        self.Set_IPAddr ='SetIPAddress('+IpDst+')'
        self.Ip_strip = 'is_ip[0]->Strip(14)-> CheckIPHeader(CHECKSUM false) -> CheckLength(65535) -> IPReassembler() \n->\n'
        self.red_flag =0

        #strategy
        self.rst_attack  = 'rst,'
        self.echo_attack ='dst udp port 7 or 19,'
        self.smuf_attack ='dst '+IpBrodCast+' and icmp,'
        self.land_attack = 'dst '+IpDst+' and src '+IpDst+','

    def ChangePort(self,newPort):
        self.Control = 'CONTROL :: ControlSocket(tcp,'+newPort+')\n'

    def strategy_init(self,Strategy):
        self.Strategy_build=''
        self.length =len(Strategy)
        for i in Strategy:
            if i == 'rst_attack':
                self.Strategy_build+= self.rst_attack
            elif i =='echo_attack':
                self.Strategy_build += self.echo_attack
            elif i =='smuf_attack':
                self.Strategy_build += self.smuf_attack
            elif i =='land_attack':
                self.Strategy_build += self.land_attack
            elif i =='red':
                self.red_flag = 1
                self.length -= 1
            else:
                print('ERROR')

        #IpClassfier
        self.Ip_Classfier = 'ic :: IPClassifier( '+self.Strategy_build+ '-)'

        port = ''
        for i in range(self.length):
            port +='ic['+str(i)+']->discard\n'
        port +='ic['+str(self.length)+']->'+self.Set_IPAddr+'->out\n'

        if self.red_flag == 0:
           basic =self.Control + self.Out_default + self.Is_ip + self.Not_ip + self.Ip_strip
           self.basic = basic
        else:
           basic = self.Control + self.Out_red + self.Is_ip + self.Not_ip + self.Ip_strip
           self.basic =basic

        self.port = port

    def NewConfig(self,Strategy,controlport):
        self.strategy_init(Strategy)
        config =self.basic+self.Ip_Classfier+self.port
        # try:
        #     file = open('test.click', 'w')
        #     file.write(config)
        # except IOError:
        #     print('FILE WRITE ERROR')
        # else:
        #     print('FILE WRITE SUCCESS')
        # file.close()
        # 直接返回一个字符串形式的config文件,交给hotconfig写本地文件
        return config

if __name__ == '__main__':
    witer = ConfigWriter(22222,'192.168.3.133',[],'192.168.3.255')
    witer.NewConfig(('smuf_attack','land_attack','red'))