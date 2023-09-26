# 导入模块
import sys, os, time

# 自定义模块
from CommonMod.MyLog import *
from CommonMod.PublicFunc import *
from CommonMod.SysVar import *
from CommonMod.TimerPoll import *
from CommonMod.ThreadPool import *
from CommonMod.TcpSvr import *


@CapError
def test(data):
    my_print("1111111111111")
    
    time.sleep(5)
    return 0

def main(argv):

    my_print("hello")
    SignalHandleReg()
    initThreadPool()
    addThreadTask(test, wloop=True)
    addThreadTask(doTimerTaskStart, wloop=True)
    
    # tcp svr
    tsvr = TcpSvr()
    addThreadTask(tsvr.doTcpSvrStart, wloop=True)

    loopThreatWait()

if __name__ == "__main__":
    sys.exit(main(sys.argv))