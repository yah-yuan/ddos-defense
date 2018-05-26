CONTROL :: ControlSocket(tcp,8082)
out :: Queue(1024) -> ToDevice(ens34)
FromDevice(ens34)-> cl :: Classifier(12/0806 20/0001,12/0806 20/0002,12/0800)
-> arpr :: ARPResponder(192.168.3.128 00:0c:29:44:f4:4c)
->out;
cl[1] -> [1]arpq :: ARPQuerier(192.168.3.128,00:0c:29:44:f4:4c)
->out;
rw :: IPAddrPairRewriter(pattern - 192.168.2.132 0 0)
-> IPPrint("send IP detail")
->DecIPTTL
->IPFragmenter(300)
-> arpq;
passLog :: ToIPSummaryDump(/root/log/passlog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto count)
->rw
cl[2]->Strip(14)
-> CheckIPHeader(CHECKSUM false)
->CheckLength(65535)
-> IPPrint("recv IP detail")
->ic_pass :: IPClassifier(231.213.20.12/24 or 98.123.21.54/24)
->IPPrint("Pass through white list")
->ic :: IPClassifier( -)
ic[0]
->passLog
