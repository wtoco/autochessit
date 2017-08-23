from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
import tratto.connectivity
import tratto.systems
import os
import re
import sys
import csv

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

@login_required
def chengdu_catalogue(request):
    return render(request, 'custom/chengdu/chengdu_catalogue.html')

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
