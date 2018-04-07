/*
Main click 的初始配置
控制服务器通过CONTROL和click通信,更新配置
更新Main click的目的是在负载均衡中增加/删除sub click
工作流程:外网网卡->更改目的ip报头(src/dst等内容)->内网网卡
*/
define($FROMIFACENAME ens33);
define($TOIFACENAME ens37);
CONTROL :: ControlSocket(tcp, 22222);
FromDevice($FROMIFACENAME)-> Queue(1024) -> ToDevice($TOIFACENAME);