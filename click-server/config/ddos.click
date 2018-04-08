define($REMOTEIP 192.168.3.1);
define($IFACENAME ens33);
CONTROL :: ControlSocket(tcp, 22223);

out :: Queue(1024) -> ToDevice($IFACENAME);
FromDevice($IFACENAME)->
LOG :: ToIPSummaryDump(/root/log/testlog,CONTENTS timestamp ip_src ip_dst ip_len ip_proto)-> is_ip :: Classifier(12/0800, -);
is_ip [1] ->Discard; //not ip, so drop

is_ip [0] 
  -> Strip(14)
  -> CheckIPHeader(CHECKSUM false)
  -> CheckLength(65535)
  -> IPReassembler()
  -> ic :: IPClassifier(src or dst host $REMOTEIP,rst,dst udp port 7 or 19,-);
ic [0] ->Print(remoteIP)->out; //from remote ip
ic [1]->Print(rst)->Discard;
ic [2] ->Print(udp)-> Discard;
ic [3] ->Print(other)-> out;