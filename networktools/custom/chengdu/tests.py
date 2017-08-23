from django.test import TestCase

# Create your tests here.
import os
import re
import csv
import numpy as np
from time import ctime
import threading


class ThreadImpl_per(threading.Thread):
    def __init__(self, ip, counts, x):
        threading.Thread.__init__(self)
        self.ip = ip
        self.counts = counts
        self.x = x

    def run(self):
        global lists
        dict = multi_threads_ping(self.ip, self.counts)
        lists[self.x] = dict
        # for x in range(0, int(self._num)):
        #     # 取得锁
        #     mutex.acquire()
        #     total = total + 1
        #     # 释放锁
        #     mutex.release()


def performance_monitoring():
    # 定义全局变量
    global lists
    lists = ['', '', '', '', '', '', '', '', '']
    # total = 0
    # 创建锁
    # mutex = threading.Lock()
    # 定义线程池
    threads = []
    # 创建线程对象 prem:: (IP,COUNTS,LIST_ID)
    threads.append(ThreadImpl_per('10.85.123.1', '5',0))
    threads.append(ThreadImpl_per('10.85.120.201', '5',1))
    threads.append(ThreadImpl_per('10.192.8.138', '5', 2))
    threads.append(ThreadImpl_per('www.baidu.com', '5', 3))
    threads.append(ThreadImpl_per('10.85.119.213', '5', 4))
    threads.append(ThreadImpl_per('10.85.119.210', '5', 5))
    threads.append(ThreadImpl_per('10.85.119.212', '5', 6))
    threads.append(ThreadImpl_per('www.baidu.com', '5', 7))
    threads.append(ThreadImpl_per('www.baidu.com', '5', 8))
    # 启动线程
    for t in threads:
        t.start()
        # 等待子线程结束
    for t in threads:
        t.join()
    return lists


def multi_threads_ping(ip,counts):
    dict = {}
    if reachable_detection(ip)==True:
        shell = "ping " + ip + " -c "+counts
        pipe = os.popen(shell)
        text = pipe.read()
        reg = re.findall(r"min/avg/max/stddev =(.*)ms", text)[0].strip()
        result = re.compile(r'/')
        result_list = result.split(reg)
        dict['min']=result_list[0]
        dict['avg'] = result_list[1]
        dict['max'] = result_list[2]
        dict['packets'] = re.findall(r"(\d) packets transmitted", text)[0].strip()
        dict['Received'] = re.findall(r"(\d) packets received", text)[0].strip()
        dict['loss'] = re.findall(r"(\d)% packet loss", text)[0].strip()+'%'
        pipe.close()
        return dict
    else:
        dict['min']="null"
        dict['avg'] = "null"
        dict['max'] = "null"
        dict['packets'] = "null"
        dict['Received'] = "null"
        dict['loss'] = "null"
        return dict

def reachable_detection(ip):
    data = ""
    shell = "ping "+ip+" -c 6 -i 0.5"
    pipe = os.popen(shell)
    text = pipe.read()
    regular_v1 = re.findall(r"Request timeout", text)
    regular_v2 = re.findall(r"Unreachable", text)
    regular_v3 = re.findall(r"Unknown host", text)
    timeout_counts = regular_v1.__len__()
    Unreachable_counts = regular_v2.__len__()
    unknown = regular_v3.__len__()
    pipe.close()
    if timeout_counts>=3:
        data = "Request is timeout"
        return data
    elif Unreachable_counts>=3:
        data = "Host Unreachable"
        return data
    elif unknown==1:
        data = "Unknown host"
        return data
    else:
        return True

if __name__ == '__main__':
    shell = "ping uc-emea1dir.myatos.net -c 6 -i 0.5"
    pipe = os.popen(shell)
    text = pipe.read()
    print("wqee:"+text)

