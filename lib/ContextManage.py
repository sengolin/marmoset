#-*- coding:utf-8 -*-
'''
Created on 2011-8-24

@author: sengo
'''
import Queue
import threading
import MarLogger
import os

global queue
queue = Queue.Queue(0)

global lock
lock = threading.RLock()

global projetctMap
projetctMap = {}

global blockMap
blockMap = {}

# server.xml
global address
#global port
global connectionTimeout
global maxThreads
global minSpareThreads
global logpath
global timestamp
global formatter
global syslog
global context
global serverModel
global apps
global appname
appname = ''

global acceptCount
acceptCount = ''

global an
an = ''

global globalMap
globalMap = {}

#import multiprocessing
#queue = multiprocessing.Queue()
            
from xml.etree.ElementTree import ElementTree

# 实例化一个ElementTree对象
context = ElementTree()

apps = {}

#element = context.parse(os.sep.join(["..","conf","server.xml"]))
element = context.parse(os.getenv('MARMOSET_HOME')+"/conf/server.xml")
for server in element.getiterator("server"):
    serverModel = server.attrib['model']
    
    for loghandler in element.getiterator("log-handler"):
        logpath = loghandler.find("path").text
        timestamp = loghandler.find("timestamp").text
        formatter = loghandler.find("formatter").text
    
    for http in element.getiterator("http"):
        address = http.find('address').text
        #port = http.find('port').text
        connectionTimeout = http.find('connectionTimeout').text
        maxThreads = http.find('maxThreads').text
        minSpareThreads = http.find('minSpareThreads').text
        acceptCount = http.find('acceptCount').text
        
    for business in element.getiterator('business'):
        for app in business.getiterator('apps'):
            for element in app:
                appName = element.find('name').text
                appModel = element.find('model').text
                appPort = element.find('port').text
                responseTimeout = element.find('responseTimeout').text
                apps[appName] = [appModel, appPort, responseTimeout]
                
syslog = MarLogger.initSysLog(logpath, formatter, timestamp)
