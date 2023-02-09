from cmath import pi
from ctypes.wintypes import SIZE
import os
from re import I
import threading


class MyThread(threading.Thread):
    ip_1 = ''

    semaphore_run = threading.Semaphore(1)  # 最多同时运行100个线程

    def start(self):  # 重载start方法
        MyThread.semaphore_run.acquire()  # 启动之前先取得信号量
        try:
            super().start()
        except:
            MyThread.semaphore_run.release()  # 线程启动失败时释放信号量

    def run(self):  # threading模块没有提供线程的善后处理，于是新定义_run函数执行线程任务，并在run中善后
        try:
            self._run()
        finally:  # 在线程任务完成后或异常退出时释放信号量
            MyThread.semaphore_run.release()

    def _run(self):  # 真正执行的线程任务
        for i in range(0, 255):
            lsip = 'ping -n 1 -w 1 10.' + str(self.ip_1) + '.' + str(i) + '.1'
            result = os.system(lsip)
            if result == 0:
                fp = open('记录.txt', 'a+')
                print(lsip, file=fp)
                fp.close()


if __name__ == '__main__':  # 测试
    for i in range(0, 255):
        task = MyThread()
        task.ip_1 = i
        task.start()
