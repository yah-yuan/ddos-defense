import socket
import time
import re
import os
from prettytable import PrettyTable
import json
'''
仅被sub-click使用
建立一个和clickserver通信的socket
定时读取click log文件中的数据,(总结)发送至clickserver,清空click log
读之前使用句柄让click log刷新
'''
logtext = ''
def ReadLog(logpath = 'testlog'):
    '''读文件'''
    os.system('click -h LOG:flush')
    logfile = open(logpath,'r')
    currentLog = logfile.read(-1)
    logfile.close()
    # print(currentLog.encode('utf8'))
    name = ('timestamp','ip_src','ip_dst','size','pkt_type')
    table = PrettyTable(name)
    form_dic = {}
    num2 = 0
    for sentence in currentLog.split('\n'):
        item = sentence.split(' ')
        if len(item) != 5:
            continue
        local_dic = {}
        num = 0
        for element in item:
            local_dic[name[num]] = element
            num += 1
        dump = json.dumps(local_dic,sort_keys=True,indent=4,separators=(',',':'))
        form_dic[num2] = item 
        num2 += 1
        print(dump)
        table.add_row(item)
    print(table)
    json_out = json.dumps(form_dic,sort_keys=True,indent=4,separators=(',',':'))
    print(json_out)
    # logfile = open(logpath,'w')
    # logfile.close()

def Send(socket):
    pass

def main():
    remote_addr = ('192.168.3.129',33333)
    s = socket.socket()
    s.connect()
    self.con = s
    while True:
        ReadLog()
        Send()
        time.sleep(0.1)

if __name__ == '__main__':
    ReadLog()