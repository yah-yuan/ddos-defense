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
dropLog :: ToIPSummaryDump(/root/log/droplog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto count)
-> Discard
passLog :: ToIPSummaryDump(/root/log/passlog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto count)
->rw
cl[2]->Strip(14)
-> CheckIPHeader(CHECKSUM false)
->CheckLength(65535)
-> IPPrint("recv IP detail")
->ic_pass :: IPClassifier(231.213.20.12 or 98.123.21.54)
->IPPrint("Pass through white list")
->ic :: IPClassifier( src 10.3.152.132,src 32.1.21.90,dst udp port 7 or 19,src host 192.168.3.255 and icmp,dst 192.168.3.128 and src 192.168.3.128 and syn,rst,-)
ic[0]->Print("[BLACK LIST 10.3.152.132 droped]")
->dropLog
ic[1]->Print("[BLACK LIST 32.1.21.90 droped]")
->dropLog
ic[2]->Print("[echo_attack droped]")
->dropLog
ic[3]->Print("[smuf_attack droped]")
->dropLog
ic[4]->Print("[land_attack droped]")
->dropLog
ic[5]->Print("[rst_attack droped]")
->dropLog
ic[6]
->passLog
