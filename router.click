// ens33 192.168.3.136 00:0c:29:44:f4:4c
//这是demo的router文件
out :: Queue(1024) -> ToDevice(ens34)

FromDevice(ens34)
  -> 

cl :: Classifier(12/0806 20/0001,
                  12/0806 20/0002,
                  12/0800) 
  -> arpr :: ARPResponder(192.168.3.128 00:0c:29:44:f4:4c)
  -> out;

cl[1]
  -> [1]arpq :: ARPQuerier(192.168.3.128, 00:0c:29:44:f4:4c)
  -> out

cl[2]
  -> ip :: Strip(14)
  -> CheckIPHeader()
  -> DropBroadcasts
  -> IPPrint("recv IP detail")
  -> rw1 :: IPRewriter(pattern - - 192.168.3.129 - 0 0)
  -> dt :: DecIPTTL
  -> fr :: IPFragmenter(300)
  -> IPPrint("send IP detail")
  -> arpq;