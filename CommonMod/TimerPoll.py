import threading as mt
import time
import sys
sys.path.append("..")

from CommonMod.MyLog import *
from CommonMod.PublicFunc import *


# 定时任务计数器, 从系统运行一直自增
g_timer_cocunt          = 0
# g_timer_cb_list 共享锁
g_timer_lock            = mt.Lock()


@CapError
def updateSysTime(data):
    updateTime()


# 简单实现一个循环调用的定时器，不能执行耗时任务会阻塞线程，定时可能不准
# 定时器名称: 多少s执行一次, 执行的函数void timer_fun_cb(data), 函数参数
g_timer_cb_list = {
    "uptime_timer" : [1, updateSysTime, None],
    # "test_timer" : [60, my_test_timer, "test"]
}

# 注册定时器
@CapError
def startTimerPlus(name, timout, timer_cb, data):
    # 类型检查, 省略
    # isinstance(name, str) isinstance(timout, int)
    if name in g_timer_cb_list.keys():
        my_print("startTimerPlus falid, name is exit: ", name)
        return None
    
    with g_timer_lock:
        g_timer_cb_list[name] = [timout, timer_cb, data]
    return name

# 删除定时器
@CapError
def stopTimerPlus(name):
    if name not in g_timer_cb_list.keys():
        my_print("stopTimerPlus falid, name is not exit: ", name)
        return
    
    with g_timer_lock:
        del g_timer_cb_list[name]
    return


# 阻塞函数, 需要启用线程调用
@CapError
def doTimerTaskStart(data):
    my_print("doTimerTaskStart start ...")

    # 每秒通过取模判断是否到时间
    # 到时间则执行对应定时任务
    global g_timer_cb_list
    global g_timer_cocunt
    global g_timer_lock

    while isRuning():
        # 加锁遍历定时任务
        with g_timer_lock:
            for t_name in g_timer_cb_list.keys():
                if (g_timer_cocunt % g_timer_cb_list[t_name][0]) != 0:
                    # 还没到时间执行，遍历其它任务
                    continue

                # 立即执行
                g_timer_cb_list[t_name][1](g_timer_cb_list[t_name][2])

            # 定时任务都遍历完了
            g_timer_cocunt += 1
        
        # 睡眠1s, 则定时器最小精度为1s
        time.sleep(1)

    
    my_print("doTimerTaskStart end ...")

