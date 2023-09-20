import time
import sys
sys.path.append("..")


# 存放框架运行的全局变量

# ------------------------------------------------------------
# 线程池框架, 线程池线程数, 默认5个
g_max_workers       = 5
# ------------------------------------------------------------
# 程序运行标记
g_proess_run        = True
# 系统时间, 定时修改, s级
g_sys_time          = time.localtime()

# ------------------------------------------------------------
def getThreadWorkNum():
    global g_max_workers
    return g_max_workers

def setThreadWorkNum(work_num = 5):
    global g_max_workers
    g_max_workers = work_num
    return

# ------------------------------------------------------------

# 提供函数返回/修改其中的值
def isRuning():
    global g_proess_run
    return g_proess_run

def setNoRun():
    global g_proess_run
    g_proess_run = False
    return

def getSysTime():
    global g_sys_time
    return g_sys_time

def getTimeNum():
    global g_sys_time
    return time.mktime(g_sys_time)

def updateTime():
    global g_sys_time
    g_sys_time = time.localtime()
    return