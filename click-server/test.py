from ManageCenter import *

center = Center()
sub_click = Click.Click(name='sub-click-1',con_ipaddr=SUB_CLICK_1_COM_IP,listen_ipaddr=SUB_CLICK_1_WORK_IP,\
    app_server_ip=APP_SERVER_IP,listen_broadcast=SUB_CLICK_1_WORK_BROADCAST,listen_device=SUB_CLICK_1_WORK_DEVICE,\
    listen_ether=SUB_CLICK_1_WORK_ETHER,net_controlPort=SUB_CLICK_1_COM_CONTROL_PORT,net_dataPort=SUB_CLICK_1_COM_DATA_PORT)
center.click_list.append(sub_click)
# config = center.Create_config(['rst_attack'])
config = center.Create_config([],\
blackList=[],whiteList=['231.213.20.12/24','98.123.21.54/24'])
# config = center.Create_config(['smuf_attack'])
# config = center.Create_config(['land_attack'])
# config = center.Create_config(['red'])
center.Change_config()
# center.click_list[0].controller.WriteHandler('config')