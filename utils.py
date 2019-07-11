import time
import os
import psutil
from multiprocessing import Queue

# 通过一个进程的名字找该进程
def get_proc_by_name(pname):
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == pname.lower():
                return proc  # return if found one
        except psutil.AccessDenied:
            print("AcessDenied")
        except psutil.NoSuchProcess:
            print("NoSuchProcess")
    return None

# 这个进程统计执行时间和内存
def calculateTime(maxTime, maxMemory, name, q):
    beginTime = time.time()

    # q是管道，执行的任务进程为把自己的pid号存在管道里，这里取出来
    pid = q.get(True)

    # 首先找到目标进程
    proc = psutil.Process(pid)
    time.sleep(1)
    try:
        while True:
            lst = proc.children()
            if len(lst) != 0:
                proc = lst[0]
            else:
                break
    except psutil.NoSuchProcess:
        q.put('0')
        return

    while True:
        time.sleep(maxTime / 1000)
        endTime = time.time()
        try:
            rss = proc.memory_info().rss        # 读取任务进程所占用的内容空间
        except psutil.NoSuchProcess:            # 如果不存在这个进程，表示任务进程已经退出了，即无tle 和 mle的情况
            q.put('0')
            return
        if float(rss) / 1024 / 1024 > maxMemory:    # 如果超过了最大的内存
            q.put('1')
            return
        if endTime - beginTime >= maxTime:          # 如果超过了限制的时间
            q.put('2')
            return

# 这个进程用于判断是否会tle，这里不输出到文件
def process_test_tle(testfile, standardIn, name, q):
    q.put(os.getpid())
    makeEchoPy(standardIn, name + "_echo.py")       # 创建一个echo的文件
    os.system("python {} | python {}".format(       # 执行
        name + "_echo.py",
        testfile
    ))

def process(testfile, standardIn, name):            # 这里同上，进行执行
    makeEchoPy(standardIn, name + "_echo.py")
    os.system("python {} | python {}>{} 2>{}".format(
        name + "_echo.py",
        testfile,
        name + "_result.out",
        name + "_error.out"
    ))

# echo.py 目的是将标准输入进行输出，再通过管道，传给目标的进行
def makeEchoPy(standardIn, name):
    str = "f = open('{}', 'r')\n".format(standardIn)
    str += "lines = f.readlines()\n"
    str += "for line in lines:\n"
    str += "\tprint(line, end='')\n"
    f = open(name, "w")
    f.write(str)
    f.close()
