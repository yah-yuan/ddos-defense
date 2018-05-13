import socket
import time
import re
'''
仅被sub-click使用
建立一个和clickserver通信的socket
定时读取click log文件中的数据,(总结)发送至clickserver,清空click log
读之前使用句柄让click log刷新
'''
logtext = ''
def ReadLog(logpath = '/root/logfile/log'):
    '''读文件'''

def Send(socket):
    pass

def main():
    local_addr = ('192.168.2.129',11111)
    s = socket.socket()
    s.bind(local_addr)
    s.listen(5)
    conn,addr = s.accept()

if __name__ == '__main__':
    main()