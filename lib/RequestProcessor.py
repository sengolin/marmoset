#-*- coding:utf-8 -*-
'''
Created on 2011-8-24

@author: sengo
'''

#header 和body分隔符
headerAndbodySplit = "\n\n"
#header分隔符
headerSplit = '\n'
#header key value 分隔符
headerKeyValueSpilt = ':'


#解析请求    Customer  Operation  ProjectId  Accept-Charset Accept-Encoding  content
def parseRequest(request):
    try:
        headerAndBodyDic = {}#headerBody 字典
        #request=request.decode('UTF-8')
        if request:
            bodyAndHeader = request.split(headerAndbodySplit, 1)#'\n\n'    分割header 和body
            if len(bodyAndHeader) == 2:      #  确保有 header 和body
                header = bodyAndHeader[0]    #header序列值
                body = bodyAndHeader[1]      #body值
                headerAndBodyDic['content'] = body.decode('UTF-8')
                headerColumn = header.split(headerSplit)#'\n'    分割header
                for column in headerColumn:
                        key, val = column.split(headerKeyValueSpilt, 1)
                        key = key.strip().decode('UTF-8')
                        val = val.strip().decode('UTF-8')
                        headerAndBodyDic[key] = val
        return headerAndBodyDic
    except  Exception, ex:
        raise ex;
