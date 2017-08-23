from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
import tratto.connectivity
import tratto.systems
from networktools.custom.chengdu.tools import *
import os
import re
import sys
import csv

# Chengdu Catalogue
@login_required
def chengdu_catalogue(request):
    return render(request, 'custom/chengdu/chengdu_catalogue.html')

# Performance_monitoring view method
@login_required
def performance_monitoring(request):
    if request.method == 'POST':
        # 定义全局变量
        global lists
        lists = ['', '', '', '', '', '', '', '', '']
        # total = 0
        # 创建锁
        # mutex = threading.Lock()
        # 定义线程池
        threads = []
        # 创建线程对象
        threads.append(ThreadImpl_per('10.85.123.1', '1000',0))
        threads.append(ThreadImpl_per('10.85.120.201', '1000',1))
        threads.append(ThreadImpl_per('10.192.8.138', '1000', 2))
        threads.append(ThreadImpl_per('uc-emea1dir.myatos.net', '50', 3))
        threads.append(ThreadImpl_per('10.85.119.213', '50', 4))
        threads.append(ThreadImpl_per('10.85.119.210', '50', 5))
        threads.append(ThreadImpl_per('10.85.119.212', '50', 6))
        threads.append(ThreadImpl_per('phmnlgenb01.genesys.local', '50', 7))
        threads.append(ThreadImpl_per('mykulgenb01.genesys.local', '50', 8))
        # 启动线程
        for t in threads:
            t.start()
            # 等待子线程结束
        for t in threads:
            t.join()
        return JsonResponse(lists,safe=False)
    return render(request, 'custom/chengdu/Performance Monitoring.html')

# Add a Mac address to a single instance
@login_required
def add_mac(request):
    if request.method == 'POST':
        mac = request.POST['mac']
        p = re.compile(r"^([0-9a-fA-F]{4}[.]){2}([0-9a-fA-F]{4})$")
        success = ''
        failed = ''

        # 验证mac是否合格,若符合则添加，若不符合则抛出错误
        if p.match(mac) == None:
            failed = 'format of mac address is not correct,please re-enter again!'
        else:
            m = tratto.systems.SystemProfiles['IOS']
            iplist = ['10.85.123.251', '10.85.123.252', '10.85.123.253', '10.85.123.254']
            cmd = "access-list 720 permit " + mac

            for ip in iplist:
                try:
                    s = tratto.connectivity.Session(ip, 22, "ssh", m)
                    s.login("nscsoffshoring", "NSCSOffshoring")

                    s.connection.sendline("config t")
                    s.connection.sendline(cmd)
                    s.connection.sendline("do wr")

                    s.login("nscsoffshoring", "NSCSOffshoring")
                    result = s.sendcommand(str("show run | in " + mac))

                    if result == None:
                        failed = 'AP '+ ip + ' add mac address failed\n'
                    else:
                        success += 'AP '  + ip + ' is added successfully\n'
                        s.logout()
                except:
                    failed = 'Error find'

        ret = {'success': success, 'failed': failed}
        print(failed)
        print(success)
        return JsonResponse(ret)
    else:
        return render(request, 'custom/chengdu/add_mac.html')

# Add a Mac address in file
@login_required
def add_mac_file(request):
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
        for item in reader:
            datas.append(item)
        csvFile.close()


        # start add mac
        p = re.compile(r"^([0-9a-fA-F]{4}[.]){2}([0-9a-fA-F]{4})$")
        success = ''
        failed = '<font color=\"#FF0000\">'
        for data in datas:
            temp = str(data).replace("['", "").replace("']", "");

            if p.match(temp) == None:
                failed += '('+str(datas.index(data)+1)+')format of mac address is not correct,please re-enter again!\n'
            else:
                m = tratto.systems.SystemProfiles['IOS']
                iplist = ['10.85.123.251', '10.85.123.252', '10.85.123.253', '10.85.123.254']
                cmd = "access-list 720 permit " + temp

                for ip in iplist:
                    try:
                        s = tratto.connectivity.Session(ip, 22, "ssh", m)
                        s.login("nscsoffshoring", "NSCSOffshoring")

                        s.connection.sendline("config t")
                        s.connection.sendline(cmd)
                        s.connection.sendline("do wr")

                        s.login("nscsoffshoring", "NSCSOffshoring")
                        result = s.sendcommand(str("show run | in " + temp))

                        if result == None:
                            failed += 'AP ' + ip + ' add mac address failed,mac '+str(datas.index(data)+1)+'\n'
                        else:
                            success += 'AP ' + ip + ' is added successfully,mac '+str(datas.index(data)+1)+' has added!\n'
                            s.logout()
                    except:
                        failed = 'Error find'
        failed+='</font>'
        ret = {'success': success, 'failed':failed}
        return JsonResponse(ret)
    else:
        return render(request, 'custom/chengdu/add_mac.html')
