/*
Sub click 的初始配置
控制服务器通过CONTROL和click通信,更新配置
更新Sub click的目的是改变ddos的防御策略
工作流程:内网网卡->写日志->ddos过滤->更改ip报头内容(发至目的ip)->
*/
CONTROL :: ControlSocket(tcp, 8081);