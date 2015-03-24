#-*- coding:utf-8 -*-
'''
Created on 2011-8-24

@author: sengo
'''
from __future__ import division 
import socket
from PoolTcpEndPoint import ThreadPool
import ContextManage
from Runnable import Runnable
import sys
import RequestProcessor
import threading
import time

class TcpWorkerThread:
    
    # 1. 接收一个新的连接请求
    def __init__(self, listen, timeout, appName, pool,):
            self.appName = appName
            self.port = int(ContextManage.apps.get(appName)[1])
            self.listen = int(listen)
            self.timeout = int(timeout)
            self.tasks = ContextManage.queue
            self.model = ContextManage.apps.get(appName)[0]
            self.syslog = ContextManage.syslog
            self.syslog.info('server start!')
            self.syslog.info('app name is ' + appName)
            self.pool = pool
            self.acceptCount = int(ContextManage.acceptCount)
            self.responseTimeout = int(ContextManage.apps.get(appName)[2])
            
    def runIt(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket server
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', self.port))
            
            if self.syslog.getEffectiveLevel() <= 10 :
                print 'marmoset start! '
                print 'appName: ' + self.appName
                print 'port: ' + str(self.port)
                print 'model: ' + self.model 
            sock.listen(self.listen)
            
            while True:  
                connection, address = sock.accept()
                self.syslog.info("request : {ip: " + str(address[0]) + ", port: " + str(address[1]) + "}");
                
                if self.syslog.getEffectiveLevel() <= 10 :
                    self.syslog.debug("current queue size is " + str(self.tasks.qsize()))
                
                # 如果当前队列的数量达到指定值最大值，则不处理当前请求，返回code：500
                if self.tasks.qsize() >= self.acceptCount:
                    try:
                        connection.send("Code:500\nServer:1.0\n\nserver busy\n\n\n\n")
                        connection.close()    
                        self.syslog.info("current queue is full. size: " + str(self.tasks.qsize()))
                        self.syslog.info("return server busy")
                    except Exception,ex:
                        self.syslog.error(ex)
                else:
                    # 1. 读取请求文的hander
                    # 2. 解析hander得到pid和operation
                    # 3. 在请求处理线程中继续从缓存中读取请求文并合并hander和body部分
                    
                    hander = ''
                    connection.settimeout(self.timeout)
                    while True: 
                        hander += connection.recv(1)
                        if hander.strip() == "":
                            break
                        if hander[-2:] == '\n\n':
                            break
                    if hander != '':
                        handerMap = RequestProcessor.parseRequest(hander)
                        pid = handerMap.get('ProjectId')
                        operation = handerMap.get('Operation').lower()
                        if pid == None or operation == None:
                            continue;
                        else:
                            pid = pid.strip()
                            operation.lower()
                            
                        # 判断是否是阻塞请求(指定客户阻塞) 
                        if operation == 'block': 
                            if not pid in ContextManage.blockMap:
                                ContextManage.blockMap[pid] = '';
                            self.SendAndcloseConnection(connection)
                            self.syslog.info("block success, projectId: " + pid)
                            
                        # 判断是否解除阻塞请求
                        elif operation == 'unblock': 
                            if pid in ContextManage.blockMap:
                                ContextManage.blockMap.pop(pid);
                            self.SendAndcloseConnection(connection)
                            self.syslog.info("unblock success, projectId: " + pid)
                        
                        else :
                            # 1. 判断该客户的是否被阻塞限制
                            # 2. 正常处理请求
                            if not ContextManage.blockMap.has_key(pid):
                                task = Runnable(connection, address, self.timeout, self.model, self.responseTimeout, hander)
                                self.tasks.put(task)
                                
                                # 在内存中记录当前每个客户的请求数
                                #stmap = ContextManage.projetctMap.get(pid)
                                #if stmap == None:
                                #    stmap = {}
                                #    ContextManage.projetctMap[pid] = stmap
                                #stmap[sock] = task
                            else:
                                connection.send("Code:200\nServer:1.0\n\nblocked , projectId: "+ pid +"\n\n\n\n")
                                connection.close()    
                                
#                        else:
#                            ContextManage.blockMap[pid] = ''
#                            t=threading.Thread(target=self.runBlockThread,args=(pid, sock))
#                            t.start()
        except Exception, ex:
            self.syslog.error(ex)
            print ex
            
    def SendAndcloseConnection(self, connection):
        try:
            connection.send("0")
            connection.close() 
        except Exception, msg:
            self.syslog.error(msg)

    def runBlockThread(self, pid, sock):
        while not ContextManage.projetctMap.get(pid) == None:
            time.sleep(1)
        sock.send('0');
        sock.close()

            
if __name__ == '__main__':
    if len(sys.argv) > 1 :
        appName = sys.argv[1] 
        ContextManage.an = appName
        pool = ThreadPool()
        pool.start(ContextManage.minSpareThreads)
        tcpWorker = TcpWorkerThread(ContextManage.maxThreads, ContextManage.connectionTimeout, appName, pool)
        tcpWorker.runIt()
        
    else:
        ContextManage.syslog.error('missing argument')
