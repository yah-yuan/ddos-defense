import Click

class Center():
    '''管理click,接受web-server的控制信息'''
    click_list = []
    main_click = None
    web_server = None
    current_strategy = None
    new_strategy = None
    subnet = '192.168.2.0/24'

    def __init__(self):
        '''设置main click,创建click-server/web-server间的socket'''
        # 申请一个新的main计算资源
        # self.main_click = Click.Click('main_click','192.168.3.134',22222,33333)
        self.demo_click = Click.Click('demo_click','192.168.2.129',22222,33333)
        self.click_list.append(self.demo_click)
        pass

    def Create_click(self):
        '''创建一个新的click,成功后向main click声明新增click的内网ip以负载均衡'''
        # 通过何种方式获得新路由器的网络信息?
        # get_new_click()
        # name =
        # ip =
        # control_port = 
        # data_port =
        click = Click(name, ip control_port, data_port)

    def Destroy_click(self):
        '''main click停止向被销毁的click转发,销毁一个click'''
        pass

    def Change_config(self, configfile):
        '''更改防御策略'''
        if self.current_strategy == 'user-define':
            # 这里好像比较难以自动化
            pass
        for click in sefl.click_list:
            click.HotConfig(configfile)

    def Create_config(self, strategy):
        click = self.click_list[0]

    def Check_Online(self):
        '''检测当前click是否在线'''
        pass

    def Listener(self):
        '''监听web服务器发来的控制请求'''
        pass