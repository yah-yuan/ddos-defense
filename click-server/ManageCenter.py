import Click

class Center():
    '''管理click,接受web-server的控制信息'''
    click_list = []
    main_click = None
    web-server = None

    def __init__():
        '''设置main click,创建click-server/web-server间的socket'''
        # 申请一个新的main计算资源
        self.main_click = Click.Click('main_click','192.168.3.134',22222,33333)
        if not isinstance(self.main_click,Click.Click):
        pass

    def Create_click(self):
        '''创建一个新的click,成功后向main click声明新增click的内网ip以负载均衡'''
        # 通过何种方式获得新路由器的网络信息?
        # get_new_click()
        click = Click('sub_click0','192.168.4.130',22222,33333)

    def Destroy_click(self):
        '''main click停止向被销毁的click转发,销毁一个click'''
        pass

    def Change_strategy(self,strategy_list):
        '''更改防御策略'''
        pass

    def Check_Online(self):
        '''检测当前click是否在线'''
        pass

    def Listener(self):
        '''监听web服务器发来的控制请求'''
        pass