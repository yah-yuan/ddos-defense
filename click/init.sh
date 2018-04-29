setsid click init.click -R
route del -net 192.168.3.0/24 ens34 #在路由表中删除要处理的理的路由信息
python3 SendDump.py