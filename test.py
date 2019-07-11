from multiprocessing import Process
import os
import time
import py_compile

def calculateTime(maxTime):
    beginTime = time.time()
    while True:
        time.sleep(maxTime / 1000)
        endTime = time.time()
        if endTime - beginTime >= maxTime:
            break


def process_while_true(name):
    print(name, "start!")
    beginTime = time.time()
    while True:
        endTime = time.time()
        # print(endTime-beginTime)


if __name__ == "__main__":
    print("Parent process %s. " % os.getpid())
    try:
        py_compile.compile("code.py", doraise=True)
    except py_compile.PyCompileError as error:
        print("sssssssss")
    """
    p1 = Process(target=process_while_true, args=("while",))
    p2 = Process(target=calculateTime, args=(2.0,))
    p1.start()
    p2.start()
    beginTime = time.time()
    p2.join()
    endTime = time.time()
    print("Time = {}".format(endTime-beginTime))
    p1.terminate()
    print("Child process end.")
    """