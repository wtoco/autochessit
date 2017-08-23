import os
import re
import threading
from time import ctime

# Batch multithreading ping
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

# Reachability judgment
def reachable_detection(ip):
    data = ""
    shell = "ping "+ip+" -c 6 -i 0.5"
    pipe = os.popen(shell)
    text = pipe.read()
    if text == "":
        data = "Unkown host"
        return data
    regular_v1 = re.findall(r"Request timeout", text)
    regular_v2 = re.findall(r"Unreachable", text)
    timeout_counts = regular_v1.__len__()
    Unreachable_counts = regular_v2.__len__()
    pipe.close()
    if timeout_counts>=3:
        data = "Request is timeout"
        error_file_tracert(ip, data)
        return data
    elif Unreachable_counts>=3:
        data = "Host Unreachable"
        error_file_tracert(ip, data)
        return data
    else:
        return True

# Tracert and generate the file for "Batch multithreading ping"
def error_file_tracert(ip,error_messages):
    ipAddress = ip
    file_object = open('templates/static/files/custom/chengdu/error_to_file.txt', 'a')
    if "Unkown host" == error_messages:
        file_object.write(ctime())
        file_object.write(error_messages)
        file_object.write("Error Host Ip :" + ip)
        return
    tracetMaxTTL = "10"
    tracetWaitingTime = "2"
    shell = "traceroute -m "+tracetMaxTTL+" -w "+tracetWaitingTime+" "+ipAddress
    pipe = os.popen(shell)
    text = pipe.read()
    file_object.write(ctime())
    file_object.write(error_messages)
    file_object.write("Error Host Ip :"+ip)
    file_object.write("\n"+text)
    pipe.close()
    return text

# performance_monitoring ThreadImplement
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