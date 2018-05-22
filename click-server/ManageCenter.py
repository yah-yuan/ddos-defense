import backends
import Click
import time
import threading
from define import *


class Center():
    '''管理click,接受web-server的控制信息'''
    click_list = []
    main_click = None
    web_server = None
    current_strategy = None
    new_strategy = None

    def __init__(self):
        '''设置main click,创建click-server/web-server间的socket'''
        # 申请一个新的main计算资源
        # self.main_click = Click.Click('main_click','192.168.3.134',22222,33333)

        self.backends = backends.Backends(self)
        pass
    def run(self):
        # threading.Thread(target=self.backends.run())
        # time.sleep(65576)
        pass

    def Create_click(self):
        '''创建一个新的click,成功后向main click声明新增click的内网ip以负载均衡'''
        '''涉及到自动化的一些东西'''
        # 通过何种方式获得新路由器的网络信息?
        # get_new_click()
        # name =
        # ip =
        # control_port = 
        # data_port =
        click = Click(name,ipaddr,app_server_ip,broadcast,gateway,ether,controlPort,dataPort)
        self.click_list.append(click)

    def Destroy_click(self):
        '''main click停止向被销毁的click转发,销毁一个click'''
        pass

    def Change_config(self):
        '''更改防御策略'''
        if self.current_strategy == 'user-define':
            # 这里好像比较难以自动化
            pass
        else:
            for click in self.click_list:
                res = click.ChangeConfig()

            self.current_strategy = self.un_commit_strategy
            return 'SUCCESS'

    def Create_config(self, strategy):
        self.un_commit_strategy = strategy
        for click in self.click_list:
            click.CreateConfig(strategy)
        return self.click_list[0].newconfig

    def Check_Online(self):
        '''检测当前click是否在线'''
        pass

    def ReadFlow(self, interval, amount):
        # 查询,返回一个字典
        return {}
        pass