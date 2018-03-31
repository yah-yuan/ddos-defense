CONTROL :: ControlSocket(tcp,8888)
define($REMOTEIP 192.168.3.1)
out :: Queue(1024) -> ToDevice($IFACENAME);FromDevice($IFACENAME)-> is_ip :: Classifier(12/0800, -);is_ip[0]->out;