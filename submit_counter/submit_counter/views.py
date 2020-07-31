import json
import requests
from django.http import HttpResponse
from django.shortcuts import render


def text_read(filename):
    try:
        file = open(filename,"r")
    except IOError:
        return []
    content = file.readlines()

    for i in range(len(content)):
        content[i] = content[i][:len(content[i])]

    file.close()
    return content


token = text_read("auth_code.txt")
url = "https://snrsnr.com/api/getDataView"
headers = {"Accept": "application/json, text/plain, */*", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "zh-CN,zh;q=0.9", 
        "authorization": token[0], 
        "Connection": "keep-alive", 
        "Content-Length": "0", 
        "Cookie": r"connect.sid=s%3AWA9DVAa3xjj0vTWVMC6h2WFbz8SVgUb5.Nv3ZwpCMgDYoxaUIEvaJKIKo%2FaA5qMQtHIco8nOuohA", 
        "Host": "snrsnr.com", 
        "If-None-Match": "W/\"bc-tA6V90h5+T7aEP9CySfrWspx18o\"", 
        "Referer": "https://snrsnr.com", 
        "Sec-Fetch-Dest": "empty", 
        "Sec-Fetch-Mode": "cors", 
        "Sec-Fetch-Site": "same-origin", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

def get(type):
    respond = requests.get(url, headers = headers)
    respond.encoding = "utf-8"

    if str(json.loads(respond.text)["code"]) == "error":
        return 1
    else:
        # html = json.loads(respond.text)
        # data = json.loads(str(html["data"]).replace("\'", "\""))
        # dataview = json.loads(str(data["dataView"]).replace("\'", "\""))

        dataview = json.loads(str(json.loads(str(json.loads(respond.text)["data"]).replace("\'", "\""))["dataView"]).replace("\'", "\""))
        return dataview[type]


def run(request):
    waiting = get("noAudit")
    unpassed = get("noPass")
    passed = get("pass")
    waiting_recheck = get("noRecheck")
    rate = round(passed / (unpassed + passed) * 100)

    content = [waiting, unpassed, passed, rate, waiting_recheck]
    return render(request, "fontend.html", {"content": content})

def refresh(request):
    waiting = get("noAudit")
    unpassed = get("noPass")
    passed = get("pass")
    waiting_recheck = get("noRecheck")
    rate = str(round(int(passed) / (int(unpassed) + int(passed)) * 100))

    content = [waiting, ",", unpassed, ",", passed, ",", rate, ",", waiting_recheck]
    return HttpResponse(content)
