//这个是我们路由器和服务端的一个demo,因为想要让整个通讯链路实现[user->router->server->user]的模式,
//即user发往server的信息通过router,而server发往user的信息不通过router直接通过外网访问user
//这个server在192.168.3.0/24网段上的ip是192.168.3.134,user的client所在的ip是192.168.3.133
//client试图和router通信,router将信息转发给server(不改变ip报的源地址),server直接和user通信,并
//在server上开启一个click伪装ip报的src地址为router的地址,以实现通信

//server端运行了一个server.py的服务端程序,user端有一个client.py的进程

//现在已经可以接受到click转发来的user信息,且其ip都是被修改过的理想的状态,但是
//现在的问题是server总是收到一个来自网关(192.168.3.1)的icmp error报文,说目标地址unreachable
//麻烦学姐方便帮我们看下后边的配置文件应该怎么改...谢谢<_>
out :: Queue(1024) -> ToDevice(ens33)

FromDevice(ens33) -> 
cl :: Classifier(12/0806 20/0001,// 0. ARP queries
                  12/0806 20/0002,// 1. ARP replies
                  12/0800) // 2. IP
  -> arpr :: ARPResponder(192.168.3.134 00:0c:29:c4:a2:8d)
  -> ARPPrint("arp responder")->out;

FromHost(fakeDev, 192.168.3.0/24, ETHER 00-01-02-03-04-05)
  -> IPPrint(FromHost)
  -> lhcl :: Classifier(12/0800, 12/0806) //[0]IP, [1]ARP querier
  -> Strip(14)
  -> CheckIPHeader()
  -> IPPrint("send")
  -> gio :: IPGWOptions(192.168.3.134)
  -> IPRewriter(pattern 192.168.3.136 - - - 0 0)
  -> dt :: DecIPTTL
  -> fr :: IPFragmenter(300)
  -> arpq :: ARPQuerier(192.168.3.134, 00:0c:29:c4:a2:8d);

toh :: IPPrint(ToHost) -> ToHost(fakeDev)

lhcl[1]
  -> lharpr ::ARPResponder(0.0.0.0/0 00-01-02-03-04-05)
  -> IPPrint("lh arp respon")
  -> toh

cl[1]
  -> cp :: Tee(2)
  -> IPPrint("arp get")
  -> [1]arpq
  -> IPPrint("arp querier")
  -> out

cp[1]
  -> toh

cl[2]
  -> Strip(14)
  -> CheckIPHeader()
  -> ipcl :: IPClassifier(host dst 192.168.3.134)
  -> IPPrint("recv")
  -> toh