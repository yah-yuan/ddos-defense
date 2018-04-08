out :: Queue(1024) -> ToDevice(ens33);
FromDevice(ens33)-> is_ip :: Classifier(12/0800, -);
is_ip [1] -> Print(!ip)->out;

is_ip [0] 
  -> SetIPAddress()
  ->Print(is_ip)->out
