// 这是demo的router文件
// 基本的转发操作在这里实现，每个click都应该有对应的代码
// arpr, arpq, rw 初始化的参数应根据当前click的硬件信息改变
// 接受以上参数
CONTROL :: ControlSocket(tcp, 22222);
out :: Queue(1024) -> ToDevice(ens34)
dropLOG :: ToIPSummaryDump(/root/log/dropLog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto count)
passLOG :: ToIPSummaryDump(/root/log/passLog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto count)

FromDevice(ens34)
  -> 

cl :: Classifier(12/0806 20/0001,
                  12/0806 20/0002,
                  12/0800) 
  -> arpr :: ARPResponder(192.168.3.128 00:0c:29:44:f4:4c) //click在网段上的ip地址，和该ip网卡的硬件地址
  -> out;

cl[1]
  -> [1]arpq :: ARPQuerier(192.168.3.128, 00:0c:29:44:f4:4c) //同
  -> out

cl[2]
  -> ip :: Strip(14)
  -> CheckIPHeader()
  -> DropBroadcasts
  -> IPPrint("recv IP detail")
  -> dropLOG
  -> passLOG
  //这里是ddos防御的操作
  //丢弃的内容在丢弃前过一下dropLOG
  //通过的内容在通过前过一下passLOG
  -> rw :: IPRewriter(pattern - - 192.168.3.129 - 0 0) //此ip为业务服务器的地址
  -> dt :: DecIPTTL
  -> fr :: IPFragmenter(300)
  -> IPPrint("send IP detail")
  -> arpq;