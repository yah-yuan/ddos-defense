import re
from define import *

'''
'rst_attack'
'echo_attack'
'smuf_attack'
'land_attack'
'red'
'''

class ConfigWriter(object):
    def __init__(self,ControlPort,Ip,IpDst,IpBrodCast,GateWay,Mac):
    #basic
        self.Out_default   = 'out :: Queue(1024) -> ToDevice('+GateWay+')\n'
        self.Out_red = 'out :: RED(768,1024,0.02)->Queue(1024) -> ToDevice('+GateWay+')\n'
        self.dropLog ='dropLog :: ToIPSummaryDump(/root/log/droplog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto count)\n'
        self.passLog ='passLog :: ToIPSummaryDump(/root/log/passlog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto count)\n'
        self.Classifier ='FromDevice('+GateWay+')-> cl :: Classifier(12/0806 20/0001,12/0806 20/0002,12/0800)\n'
        self.arpr    ='-> arpr :: ARPResponder('+Ip+' '+Mac+')\n->out;\n'
        self.arpq    ='cl[1] -> [1]arpq :: ARPQuerier('+Ip+','+Mac+')\n->out;\n'
        self.Set_IPAddr ='SetIPAddress('+IpDst+')'
        self.Ip_strip = 'cl[2]->Strip(14)\n-> CheckIPHeader(CHECKSUM false)\n->CheckLength(65535)\n'
        self.IpPrintR ='-> IPPrint("recv IP detail")\n'
        self.IpPrintS   ='-> IPPrint("send IP detail")\n'
        self.IpOut      ='-> arpq;\n'
        self.red_flag =0
        ############不再命名,防止重复
        self.DecIpTTL   ='->DecIPTTL\n'
        self.IpFragment ='->IPFragmenter(300)\n'
        ##################
        ############将iprewriter放在最前面保证复用
        self.IpRewriterDeclare ='rw :: IPAddrPairRewriter(pattern - '+IpDst+' 0 0)\n'+ self.IpPrintS + self.DecIpTTL + self.IpFragment + self.IpOut
        self.IpRewriter ='->rw\n'
        #####################
        self.passLog += self.IpRewriter
        self.dropLog += '-> Discard\n'

        #strategy
        self.rst_attack  = 'rst,'
        self.echo_attack ='dst udp port 7 or 19,'
        self.smuf_attack ='src host '+IpBrodCast+' and icmp,'
        self.land_attack = 'dst '+Ip+' and src '+Ip+' and syn,'

    # def ChangePort(self,newPort):
    #     self.Control = 'CONTROL :: ControlSocket(tcp,'+newPort+')\n'

    def strategy_init(self,Strategy:list,IpBanList:list,IpPassList:list):
        self.Strategy_build=''
        self.length =len(Strategy)+len(IpBanList)+len(IpPassList)
        if IpPassList:
            for i in IpPassList:
                self.Strategy_build+='src '+i+','
        if IpBanList:
            for i in IpBanList:
                self.Strategy_build+='src '+i+','
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
                self.length=self.length-1
            else:
                print('STRATEGY ERROR')

        #IpClassfier
        self.Ip_Classfier = '->ic :: IPClassifier( '+self.Strategy_build+ '-)\n'
        final_list = IpPassList + Strategy + IpBanList
        port = ''
        i=0
        serial = 0
        ############################
        if IpPassList:
            for i in range(len(IpPassList)):
                port +='ic['+str(i)+']\n'+'->Print("[WHITE LIST '+ final_list[i] + ' passed]")\n'+'->passLog\n'
                # port += 'ic[' + str(i) + ']->passLog\n->Print("[WHITE LIST ' + final_list[i] + ' passed]")\n->out\n'
        serial += i+1
        i = 0
        ###########################
        if IpBanList:
            for i in range(len(IpBanList)):
                port += 'ic[' + str(serial + i) + ']'+'->Print("[BLACK LIST ' + IpBanList[i] + ' droped]")\n'+'->dropLog\n'
        serial += i+1

        ###########################
        for i in range(self.length-len(IpPassList)-len(IpBanList)):
            port +='ic['+str(i+serial)+']'+'->Print("['+Strategy[i]+' droped]")\n'+ '->dropLog\n'
        ###########################
        port +='ic['+str(self.length)+']\n'+ '->passLog\n'#+self.DecIpTTL+self.IpFragment+self.IpOut+'\n'

        if self.red_flag == 0:
           basic =self.Control + self.Out_default  +  self.Classifier + self.arpr + self.arpq + self.IpRewriterDeclare + self.dropLog + self.passLog + self.Ip_strip
           basic+=self.IpPrintR
           self.basic = basic
        else:
           basic = self.Control + self.Out_red + self.Classifier + self.arpr + self.arpq + self.IpRewriterDeclare + self.dropLog + self.passLog + self.Ip_strip
           basic += self.IpPrintR
           self.basic =basic

        self.port = port
    '''添加了白名单(IpPassList),在学姐论文中看到好像队列的输入端口可以有多个，我是依据这一基础改的，具体的可以看一下队列元素'''
    def NewConfig(self,controlPort,Strategy,IpBanList,IpPassList,id):
        self.Control = 'CONTROL :: ControlSocket(tcp,'+str(controlPort)+')\n'
        self.strategy_init(Strategy,IpBanList,IpPassList)
        config =self.basic+self.Ip_Classfier+self.port
        # try:
        #     file = open('click_'+str(id)+'.click', 'w',encoding='UTF-8')
        #     file.write(config)
        # except IOError:
        #     print('FILE WRITE ERROR')
        #     file.close()
        # else:
        #     print('FILE WRITE SUCCESS')
        #     file.close()
        return config
    '''        
    def ConfigDefine(self,conf,id):
        try:
            file = open('click_'+id+'.click','w')
            file.write(conf)
        except IOError:
            print('FILE WRITE ERROR')
            file.close()
        else:
            print('FILE WRITE SUCCESS')
            file.close()
    '''


if __name__ == '__main__':
    witer = ConfigWriter(22222,'192.168.3.128','192.168.3.129','192.168.3.255','ens34','00:0c:29:44:f4:4c')
    witer.NewConfig(999,('smuf_attack','land_attack','red'),('10.1.1.2','10.1.1.3'),'',1124)
'''这里的参数我调试的时候乱改的'''