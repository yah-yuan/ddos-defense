CONTROL :: ControlSocket(tcp,22222)
out :: RED(768,1024,0.02)->Queue(1024) -> ToDevice(192.168.3.133)
FromDevice(ens37)-> is_ip :: Classifier(12/0800, -)
is_ip[1]->out
is_ip[0]->Strip(14)-> CheckIPHeader(CHECKSUM false) -> CheckLength(65535) -> IPReassembler() ->
ic :: IPClassifier( dst 192.168.3.255 and icmp,dst 192.168.3.133 and src 192.168.3.133,-)ic[0]->discard
ic[1]->discard
ic[2]->discard
ic[4]->SetIPAddress(192.168.3.133)->out