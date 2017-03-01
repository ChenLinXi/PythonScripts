import os, sys, json, time
import urllib
import xml.dom.minidom
import urllib2
import httplib
from xml.dom.minidom import parse
import collections
import xml.etree.cElementTree as ET
from io import StringIO

class configInfo(object):
    def __init__(self):
        self.skyEye = []
        self.groupName = []
        self.redisName = []
        self.ip = []
        self.env = "QA"

    def openFile(self, filePath):
        f = open(filePath)
        lines = f.readlines()
        f.close()
        count = 0
        for line in lines:
            if "_" in line:
                line = ''.join(line).strip('\n').strip('?').split("_")
                self.skyEye.append(line[0].lower())
                self.groupName.append(line[1])
                self.redisName.append(line[0] + '_' + line[1])
                continue
            if ":" in line:
                line = ''.join(line).strip('\n')
                self.ip.append(line)
                count += 1
                continue

def getConfig(skyEye, groupName, ip):
    fp = urllib.urlopen("http://xxxx/getProject?project="+skyEye)
    tmp = fp.read()
    fp.close()
    f = urllib.urlopen("http://xxxx/v4/getconfiglist/" + tmp)
    result = f.read()
    config = json.loads(result)
    if config == "TCBase.Cache":
        xmlfile = config['value']
        dom = xml.dom.minidom.parseString(xmlfile)
        root = dom.documentElement
        node = root.getElementsByTagName('cache')
        print node.getAttribute('name')
        print len(node)
        if node.getAttribute('name') == groupName:
            fu = file("D:\MyConfiguration\xxxx\Desktop\QA.txt", "a+")
            fu.write(skyEye + "_" + groupName + "_QA" + "\n" + ip + '\n\n')
            fu.close()
        else:
            cache = dom.createElement('cache')
            cache.setAttribute('name', groupName)
            cache.setAttribute('enabled', 'true')
            cache.setAttribute('type', 'C')
            cache.setAttribute('scene', 'C')
            cache.setAttribute('needPrefixKey', 'false')

            redis = dom.createElement('redis')
            redis.setAttribute('ip', ip)
            redis.setAttribute('minPool', str(3))
            redis.setAttribute('maxPool', str(20))
            redis.setAttribute('password', '')
            redis.setAttribute('read', 'true')
            redis.setAttribute('enabled', 'true')
            redis.setAttribute('type', 'redis')
            redis.setAttribute('timeOut', str(1000))

            cache.appendChild(redis)
            root.appendChild(cache)
            dom.appendChild(root)

            fw = file("D:\MyConfiguration\xxxx\Desktop\\test.xml", 'w')
            dom.writexml(fw, '', '', '', 'utf-8')
            fw.close()

            f = open("D:\MyConfiguration\xxxx\Desktop\\test.xml", 'r')
            res = f.read()
            f.close()
            return res
    else:
        doc = xml.dom.minidom.Document()
        tcbase = doc.createElement('tcbase.cache')

        cache = doc.createElement('cache')
        cache.setAttribute('name', groupName)
        cache.setAttribute('enabled', 'true')
        cache.setAttribute('type', 'C')
        cache.setAttribute('scene', 'C')
        cache.setAttribute('needPrefixKey', 'false')

        redis = doc.createElement('redis')
        redis.setAttribute('ip', ip)
        redis.setAttribute('minPool', str(3))
        redis.setAttribute('maxPool', str(20))
        redis.setAttribute('password', '')
        redis.setAttribute('read', 'true')
        redis.setAttribute('enabled', 'true')
        redis.setAttribute('type', 'redis')
        redis.setAttribute('timeOut', str(1000))

        cache.appendChild(redis)
        tcbase.appendChild(cache)
        doc.appendChild(tcbase)

        fw = file("D:\MyConfiguration\xxxx\Desktop\\newtest.xml", 'w')
        doc.writexml(fw, '', '', '', 'utf-8')
        fw.close()

        f = open("D:\MyConfiguration\xxxx\Desktop\\newtest.xml", 'r')
        res = f.read()
        f.close()
        return res

class postInfo(object):
    def __init__(self):
        self.projectName = ''
        self.key = ''
        self.value = ''
        self.userName = 'xxxx'
        self.open = 'false'
        self.cacheType = 'update'

    def setInfo(self, projectName, key, value):
        self.projectName = projectName
        self.key = key
        self.value = value
        RES = {}
        RES['projectName'] = projectName
        RES['key'] = key
        RES['value'] = value
        RES['userName'] = self.userName
        RES['open'] = self.open
        RES['cacheType'] = self.cacheType
        return json.dumps(RES).encode("utf-8")


def main():
    ConfigInfo = configInfo()
    ConfigInfo.openFile("D:\MyConfiguration\cm41643\Desktop\UAT\\redisinfo")

    for i in range(len(ConfigInfo.groupName)):
        PostInfo = postInfo()

        res = getConfig(ConfigInfo.skyEye[i], ConfigInfo.groupName[i], ConfigInfo.ip[i])
        result = PostInfo.setInfo(ConfigInfo.skyEye[i], "TCBase.Cache", res)

        f = open("D:\MyConfiguration\cm41643\Desktop\UAT\\xmlfile.txt", 'a+')
        f.write(ConfigInfo.skyEye[i] + '\n' + result + '\n\n')
        f.close()

        print result
        print type(result)
        # try:

        #     headers = {"Content-Type": "application/json",
        #                "Cache-Control": "no-cache"}
        #     url = "http://xxxx:8110/v4/modifyandpush"
        #     result = '[' + result + ']'
        #     req = urllib2.Request(url, result)
        #     req.add_header('Content-Type','application/json')
        #     req.add_header('Cache-Control','no-cache')
        #     req.get_method = lambda: 'POST'
        #     req = urllib2.urlopen(req)
        #     print req.read()


            # httpClient = httplib.HTTPConnection("http://xxxx", 8210, timeout=30)
            # httpClient.request("POST", "/v5/modifyandpush", params, headers)

            # response = httpClient.getresponse()
            # print response.status
            # print response.reason
            # print response.read()
            # print response.getheaders()
        # except Exception, e:
        #     print e
        #print res
        # f = open("D:\MyConfiguration\cm41643\Desktop\QA\\xmlfile.txt", 'a+')
        # f.write(ConfigInfo.skyEye[i] + ": \n" +res + "\n\n")
        # f.close()



if __name__ == "__main__":
    main()

