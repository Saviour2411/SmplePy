from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import threading as mt
import sys
sys.path.append("..")

from CommonMod.MyLog import *
from CommonMod.PublicFunc import *
from CommonMod.SysVar import *

# 轮询线程列表间隔时间, 200ms
g_loop_sleep        = 0.2

# 线程池
g_thread_pool       = None
# g_thread_pool锁
g_pool_lock         = mt.Lock()

# 线程列表, [线程对象,函数对象,函数参数] 
g_thread_list       = []
# g_thread_list锁
g_thread_lock       = mt.Lock()


# 初始化线程池, 默认5个
@CapError
def initThreadPool(max_works=5):
    global g_thread_pool
    g_thread_pool = ThreadPoolExecutor(max_workers=max_works)

    my_print("initThreadPool success")

# 添加线程到线程池执行
# 被执行的函数, 函数参数, 是否服务线程(非执行一次就退出)
@CapError
def addThreadTask(func, args=(), wloop=False):
    global g_thread_pool, g_pool_lock
    global g_thread_list, g_thread_lock

    f_thd = None

    with g_pool_lock:
        f_thd = g_thread_pool.submit(func, args)

    # 不是服务线程，直接返回
    if not wloop:
        return 0
    
    # 服务线程随着线程池结束再结束, 传入参数固定
    with g_thread_lock:
        g_thread_list.append([f_thd, func, args])

    return 0

# 等待线程执行完
@CapError
def loopThreatWait():
    global g_loop_sleep
    global g_thread_pool, g_pool_lock
    global g_thread_list, g_thread_lock

    #wait(all_task, return_when=FIRST_COMPLETED)
    my_print("Enter thread loop ...")
    while True:
        error_list = []
        done_list = []

        for thd_node in g_thread_list:
            # 线程未执行完成，继续执行
            if not thd_node[0].done():
                continue

            # 执行完成需要判断返回值是否异常
            if thd_node[0].result() != 0:
                # 异常, 重新执行
                my_print(thd_node[1].__name__, " excepted: ", thd_node[0].result())
                error_list.append(thd_node)
            else:
                # 无异常, 则表示需要退出
                my_print(thd_node[1].__name__, " finished: ", thd_node[0].result())
                done_list.append(thd_node)

        # 移除需要退出的线程
        for tmp_node in done_list:
            with g_thread_lock:
                g_thread_list.remove(tmp_node)

        # 重新执行异常线程
        for tmp_node in error_list:
            addThreadTask(tmp_node[1], tmp_node[2], wloop=True)
            with g_thread_lock:
                g_thread_list.remove(tmp_node)

        # 判断是否还有线程需要运行
        if not g_thread_list:
            break
        
        # 轮询间隔
        time.sleep(g_loop_sleep)

    # 线程池关闭
    g_thread_pool.shutdown()
    my_print("Exit thread loop ...")
