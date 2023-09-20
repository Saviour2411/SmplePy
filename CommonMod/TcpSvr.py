

import select, socket
import sys
sys.path.append("..")

from CommonMod.MyLog import *
from CommonMod.PublicFunc import *
from CommonMod.SysVar import *



class TcpSvr(object):

    def __init__(self, svr_ip="0.0.0.0", svr_port=22345, cli_func=None):
        self.svr_ip = svr_ip
        self.svr_port = svr_port
        if not cli_func:
            self.cli_func = self.cli_default_handle
        else:
            self.cli_func = cli_func

    def cli_default_handle(cli, data):
        my_print("recv data from ", cli.getpeername())
        return 0
    

t = TcpSvr()