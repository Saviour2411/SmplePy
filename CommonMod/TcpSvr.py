

import select, socket
import sys
sys.path.append("..")

from CommonMod.MyLog import *
from CommonMod.PublicFunc import *
from CommonMod.SysVar import *

class TcpSvr(object):

    # 构造方法
    def __init__(self, svr_ip="0.0.0.0", svr_port=22345):
        self.svr_ip             = svr_ip
        self.svr_port           = svr_port

        # previte attr 私有属性
        self._listen_num        = 1000
        self._cliaddr_map       = {}
        self._svr_sock          = None
        self._reg_funcs         = {"accept":None, "recv":None, "close":None, "except":None}
        self._select_timeout    = 0.2
        self._recv_maxsize      = 1024*1024*32

        # select框架监听列表
        self._input_list = []
        self._output_list = []

        # 开启绑定
        self._bind_sock()
    
    # 析构方法
    def __del__(self):
        pass
    
    # 创建绑定套接字
    @CapError
    def _bind_sock(self):
        self._svr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._svr_sock.bind((self.svr_ip, self.svr_port))
        self._svr_sock.listen(self._listen_num)
        self._svr_sock.setblocking(False)
        my_print("bind svr addr {}:{}".format(self.svr_ip, self.svr_port), debug="leave_1")

    # 解绑定
    @CapError
    def _unbind_sock(self):
        pass

    # 重新绑定
    @CapError
    def reBindSock(self, svr_ip="0.0.0.0", svr_port=22345):
        pass
    
    # 开始监听sock处理任务
    @CapError
    def doTcpSvrStart(self, args):
        my_print("start tcp server, wait client connect ...", debug="leave_1")

        # 设置监听服务器sock
        if self._svr_sock not in self._input_list:
            self._input_list.append(self._svr_sock)

        # 开始轮询
        while isRuning():
            rl, wl, el = select.select(
                self._input_list, self._output_list, self._input_list, self._select_timeout)
            
            # 处理可读
            for sock in rl:
                # 处理一个新的连接
                if sock is self._svr_sock:
                    cli, addr = sock.accept()
                    self._accept_cli_link_handle(cli, addr)
                    continue

                # 处理接收客户端数据
                data = sock.recv(self._recv_maxsize)
                if data:
                    self._recv_cli_data_handle(sock, data)
                else:
                    # 没收到数据断开连接
                    self._close_cli_sock_handle(sock, data)
            
            # 处理可写 --暂不处理
            # 处理异常
            for sock in el:
                # 同断开连接处理
                self._close_cli_sock_handle(sock, data)

        # 退出服务器
        return 0
    
    # 退出服务器
        
    # 客户端连接请求处理方法
    @CapError
    def _accept_cli_link_handle(self, cli, addr):
        my_print("recv cli link from({}:{})".format(addr[0], addr[1]), debug="leave_1")
        cli.setblocking(False)
        self._input_list.append(cli)
        self._cliaddr_map[cli] = addr

        if not self._reg_funcs["accept"]:
            return 0

        # 调用注册的函数
        return self._reg_funcs["accept"](cli, addr)

    # 接收客户端数据处理方法
    @CapError
    def _recv_cli_data_handle(self, cli, data):
        my_print("recv cli({}:{}) data :"
                 .format(self._cliaddr_map[cli][0], self._cliaddr_map[cli][1]), data, debug="leave_1")

        if not self._reg_funcs["recv"]:
            return 0
        return self._reg_funcs["recv"](cli, data)
    
    # 客户端关闭处理方法
    @CapError
    def _close_cli_sock_handle(self, cli, data):
        my_print("cli({}:{}) will close"
                 .format(self._cliaddr_map[cli][0], self._cliaddr_map[cli][1]), debug="leave_1")
        
        # 关闭并移除连接客户端
        cli.close()
        if cli in self._input_list:
            self._input_list.remove(cli)
        if cli in self._output_list:
            self._output_list.remove(cli)
        if cli in self._cliaddr_map.keys():
            del self._cliaddr_map[cli]

        if not self._reg_funcs["close"]:
            return 0

        return self._reg_funcs["close"](cli, data)
    

    # 注册处理函数
    @CapError
    def addCliHandleFunc(self, type=None, func=None):
        self._reg_funcs[type] = func
        return 0

# example
# t = TcpSvr()
# t.doTcpSvrStart()