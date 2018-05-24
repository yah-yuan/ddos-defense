CONTROL :: ControlSocket(tcp,8082)
out :: Queue(1024) -> ToDevice(ens34)
dropLog :: ToIPSummaryDump(/root/log/droplog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto count)
passLog :: ToIPSummaryDump(/root/log/passlog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto count)
FromDevice(ens34)-> cl :: Classifier(12/0806 20/0001,12/0806 20/0002,12/0800)
-> arpr :: ARPResponder(192.168.3.128 00:0c:29:44:f4:4c)
->out;
cl[1] -> [1]arpq :: ARPQuerier(192.168.3.128,00:0c:29:44:f4:4c)
->out;
cl[2]->Strip(14)
-> CheckIPHeader(CHECKSUM false)
->CheckLength(65535)
-> IPPrint("recv IP detail")
->ic :: IPClassifier( src host 192.168.3.255 and icmp,-)
ic[0]->dropLog->print("smuf_attack")->Discard
ic[1]->rw :: IPAddrPairRewriter(pattern - 192.168.2.132 0 0)
-> dt :: DecIPTTL
-> fr :: IPFragmenter(300)
-> IPPrint("send IP detail")->passLog-> arpq;

