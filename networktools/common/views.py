from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import os
import re
import csv
from time import ctime

@login_required
def common_catalogue(request):
    return render(request, 'common/common_catalogue.html')

@login_required
def tcp_easy_test(request):
    ip = None
    port = None
    if request.method == 'POST':
        ip = request.POST['ip']
        port = request.POST['port']
        en0 = os.popen("nmap -sT " + ip + " -p " + port)
        text = en0.read()
        en0.close()
        data = ""
        data += "Tcp scanning host ipAddress:" + ip
        data += delete_useless_words(text)
        return HttpResponse(data)
    else:
        return render(request, 'common/tcp_easy_test.html')

@login_required()
def udp_easy_test(request):
    ip = None
    port = None
    if request.method == 'POST':
        ip = request.POST['ip']
        port = request.POST['port']
        en0 = os.popen("nmap -sU " + ip + " -p " + port)
        text = en0.read()
        en0.close()
        data = ""
        data += "Ucp scanning host ipAddress:" + ip
        data += delete_useless_words(text)
        return HttpResponse(data)
    else:
        return render(request, 'common/udp_easy_test.html')

@login_required
def tcp_group_test(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        # save file
        if file_obj:  # 处理附件上传到方法
            f = open(os.path.join("templates/static/files", file_obj.name), "wb")
            for chunck in file_obj.chunks():
                f.write(chunck)
            f.close()
            print("true")
        else:
            print("false")

        # open file
        csvFile = open("templates/static/files/"+file_obj.name, "r")
        reader = csv.reader(csvFile)  # 返回的是迭代类型
        datas = []
        filepreview = ''
        for item in reader:
            filepreview = filepreview + 'ipaddress:' + item[0]+"\t ports:"+item[1]+'\n'
            datas.append(item)
        csvFile.close()

        # Tcp scanning start
        result = ''
        for test in datas:
            p = re.compile(r'\s')
            portLists = p.split(test[1])
            data = ""
            print("Tcp scanning host ipAddress:" + test[0],)
            for port in portLists:
                data = data + port + ','
            en0 = os.popen("nmap -sT " + test[0] + " -p " + data)
            text = en0.read()
            result = result + delete_useless_words(text)
            en0.close()
        ret = {'filepreview': filepreview, 'result': result}
        return JsonResponse(ret)
    else:
        return render(request, 'common/tcp_group_test.html', {})

@login_required
def udp_group_test(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        # save file
        if file_obj:  # 处理附件上传到方法
            f = open(os.path.join("templates/static/files", file_obj.name), "wb")
            for chunck in file_obj.chunks():
                f.write(chunck)
            f.close()
            print("true")
        else:
            print("false")

        # open file
        csvFile = open("templates/static/files/"+file_obj.name, "r")
        reader = csv.reader(csvFile)  # 返回的是迭代类型
        datas = []
        filepreview = ''
        for item in reader:
            filepreview = filepreview + 'ipaddress:' + item[0]+"\t ports:"+item[1]+'\n'
            datas.append(item)
        csvFile.close()

        # Tcp scanning start
        result = ''
        for test in datas:
            p = re.compile(r'\s')
            portLists = p.split(test[1])
            data = ""
            print("Udp scanning host ipAddress:" + test[0],)
            for port in portLists:
                data = data + port + ','
            en0 = os.popen("nmap -sU " + test[0] + " -p " + data)
            text = en0.read()
            result = result + delete_useless_words(text)
            en0.close()
        ret = {'result': result}
        return JsonResponse(ret)
    else:
        return render(request, 'common/udp_group_test.html', {})



@login_required
def ping_tracrt_to_file(request):
    ip = None
    if request.method == 'POST':
        ip = request.POST['ip']
        file_object = open('templates/static/files/pttext.txt', 'a')
        data = ""
        try:
            data += ping(ip,file_object)
            data += tracert(ip,file_object)
            file_object.write("\n")
        finally:
            file_object.close()
        return HttpResponse(data)
    else:
        return render(request, 'common/ping_tracrt_to_file.html')

############################## static method ##############################

def delete_useless_words(text):
    regex1 = re.compile(r'Starting.*CST')
    result = regex1.sub('',text)
    return result

def readCsvFile(file):
    lists = []
    csvFile = open(file, "r")
    reader = csv.reader(csvFile)  # 返回的是迭代类型
    data = []
    for item in reader:
#        print(item[0]+":"+item[1])
        data.append(item)
    csvFile.close()
    return data

def ping(ip,file):
    ipAddress = ip
    ping_counts = "4"
    shell = "ping "+ipAddress+" -c "+ping_counts
    pipe = os.popen(shell)
    text = pipe.read()
    file.write(ctime())
    file.write("\n"+text)
    pipe.close()
    return text

def tracert(ip,file):
    ipAddress = ip
    tracetMaxTTL = "20"
    tracetWaitingTime = "2"
    shell = "traceroute -m "+tracetMaxTTL+" -w "+tracetWaitingTime+" "+ipAddress
    pipe = os.popen(shell)
    text = pipe.read()
    file.write(ctime())
    file.write("\n"+text)
    pipe.close()
    return text
