import sys, signal
from inspect import *
sys.path.append("..")

from CommonMod.MyLog import *
from CommonMod.SysVar import *


# 定义异常处理函数
def CapError(func):
    def excel_func(*args,**kwargs):
        ret = 0
        try:
            ret = func(*args,**kwargs)
            if ret == None or ret == 0:
                ret = 0
            else:
                my_print("CapError(ret) :", ret, ", func_name :", func.__name__)
        except Exception as e:
            my_print("CapError :", e, ", func_name :", func.__name__)
            ret = 1
        finally:
            return ret

    return excel_func

# 定义信号处理函数
@CapError
def SignalHandleReg(int_func=None, term_func=None):
    
    # 定义默认信号处理函数
    def default_handle_sig(signal, frame):
        my_print("recv sig :", signal, " !!!")

        # 默认调用退出程序函数
        if isfunction(setNoRun):
            setNoRun()

        return 0
    
    if not int_func:
        int_func = default_handle_sig
    if not term_func:
        term_func = default_handle_sig

    # 注册信号处理函数
    signal.signal(signal.SIGINT, int_func)
    signal.signal(signal.SIGTERM, term_func)

    return 0