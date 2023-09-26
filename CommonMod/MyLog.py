import time
import sys
sys.path.append("..")
from CommonMod.SysVar import *


# 图片存放位置
g_image_path            = "D:\\proj\\image"

# debug标记, 减少日志打印
g_debug_leave = {
    "leave_0":True,   # 默认打印日志
    "leave_1":True,   # TCP服务器内部日志

    # 业务自定义日志
    "leave_2":False,  # dump task node日志
    "leave_3":True,   # 定时器日志
    "leave_4":True,   # 接收udp 22345
    "leave_5":False,   # 接收udp 22346
    "leave_6":True,   # 转发报文
    "leave_7":False,  # 报文数据太多的放在这个模式打印
    "leave_8":True,   # 是否将接收到的图片报文到服务器本地D:\proj\image目录下
}

def my_print(*obj, debug="leave_0"):
    if not g_debug_leave[debug]:
        return
    
    # 开启图片数据打印, 则写入文件中 srcdev_oprid.jpg
    if debug == "leave_8":
        img_path = "{}\\{}_{}.jpg".format(g_image_path, obj[0]["src_dev"], obj[0]["opr_id"])
        my_print("write image to:{}, size:{}".format(img_path, obj[0]["total_len"]))
        with open(img_path, 'wb') as f:
            f.write(obj[0]["data"])
        return

    time_str = time.strftime("%Y-%m-%d %H:%M:%S", getSysTime())
    print("[{}][{}]".format(time_str, debug), *obj)

def show_time_str(localtime):
    return time.strftime("%Y-%m-%d %H:%M:%S", localtime)


