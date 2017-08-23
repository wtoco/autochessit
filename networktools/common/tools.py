import os
import re
import csv
from time import ctime


# Remove redundant code
def delete_useless_words(text):
    regex1 = re.compile(r'Starting.*CST')
    result = regex1.sub('',text)
    return result

# Read the contents of the csv file
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

# Write the contents of the ping to the file
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

# Write the contents of the tracert to the file
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