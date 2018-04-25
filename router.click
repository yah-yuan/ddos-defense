// ens33 192.168.3.136 00:0c:29:e1:1f:18
//这是demo的router文件
out :: Queue(1024) -> ToDevice(ens33)

FromDevice(ens33) -> 

cl :: Classifier(12/0806 20/0001,
                  12/0806 20/0002,
                  12/0800) 
  -> arpr :: ARPResponder(192.168.3.136 00:0c:29:e1:1f:18)
  -> out;

cl[1]
  -> [1]arpq :: ARPQuerier(192.168.3.136, 00:0c:29:e1:1f:18)
  -> out

cl[2]
  -> ip :: Strip(14)
  -> CheckIPHeader()
  -> DropBroadcasts
  -> gio :: IPGWOptions(192.168.3.136)
//   -> FixIPSrc(192.168.3.136)
  -> rw1 :: IPRewriter(pattern - - 192.168.3.134 - 0 0)
  // -> SetIPAddress(192.168.3.134)
  -> dt :: DecIPTTL
  -> fr :: IPFragmenter(300)
  -> arpq;

dt[1] -> ICMPError(192.168.3.136, timeexceeded) 
//   -> [0]rt;
  -> arpq
fr[1] -> ICMPError(192.168.3.136, unreachable, needfrag) 
//   -> [0]rt;
  -> arpq
// gio[1] -> ICMPError(192.168.3.1 36, parameterproblem) -> [0]rt;
