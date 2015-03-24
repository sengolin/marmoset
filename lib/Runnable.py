#-*- coding:utf-8 -*-
'''
Created on 2011-8-26

@author: sengo
'''
import sys, os
from multiprocessing import Process, Queue
import ContextManage
import socket
import ServerModel

class Runnable:
    
    def __init__(self, connection, address, timeout, model, responseTimeout, hander):
        self.connection = connection
        self.address = address
        self.timeout = timeout
        self.model = model
        self.syslog = ContextManage.syslog
        self.lastSepIndex = self.model.rfind(os.sep)
        self.responseTimeout = responseTimeout
        self.hander = hander
        sys.path.append(self.model[:self.lastSepIndex])
        
    def run(self):
        try: 
            self.syslog.info('runnable run!')
            self.connection.settimeout(self.timeout)
            buf = ''  
            # 读取请求文中的body部分
            while True: 
                buf += self.connection.recv(2048)
                if buf[-4:] == '\n\n\n\n':
                    break
            buf = self.hander + buf # 合并hander和body部分
                
            queue = Queue()
            
            # 生成taskid，一次请求中的唯一标示
            taskid = ''
            if ContextManage.an == ServerModel.TASKQ:
                import uuid
                taskid = str(uuid.uuid1()).replace('-', '')
                buf = 'Taskid:' + taskid + '\n' + buf
            
            # buf    请求文
            # queue  共享内存队列在取得lispeed的返回值时使用
            xargs = (buf, queue)    
                
            model = self.model[self.lastSepIndex + 1:]
            if self.syslog.getEffectiveLevel() <= 10 :
                self.syslog.debug("model: " + model)
                
            exec('import ' + model)
            clazz = eval(model + '.' + model + '()')
            if self.syslog.getEffectiveLevel() <= 10 :
                self.syslog.debug("eval this clazz")
            
            # 创建子进程处理请求任务    
            p = Process(target=clazz.createApp, args=xargs)
            p.start()
            self.syslog.info(p.is_alive())
            self.syslog.info("child process is started")
            
            # 通过response共享内存队列获得返回值
            response = queue.get(self.responseTimeout)

            resultLen = len(response)
            
            if self.syslog.getEffectiveLevel() <= 10 :
                self.syslog.debug("response len is :" + str(resultLen))
                
            # 按字节区间通过socket返回数据部分
            start = 0
            end = 1024
            lens = 1024
            while 1:
                if resultLen <= lens:
                    end = resultLen
                    self.connection.send(response[start : end])
                    break
                self.connection.send(response[start : end])   
                if end >= resultLen:
                    break
                start = end
                end += lens
                if resultLen - start < lens:
                    end = resultLen
                    
            # 从内存中移除该请求
            #ContextManage.projetctMap.get(self.pid[4:].strip()).pop(self.connection)
            
        except socket.timeout:
            self.syslog.error('response timeout')
            self.connection.send('timeout!')
        except Exception, msg:
            self.syslog.error(msg)
            self.connection.send(msg)
        finally:
            try:
                self.connection.close()
            except Exception, msg:
                self.syslog.error(msg)
            try:
                # 'p' 是子进程的变量
                # 等待子进程退出后，结束当前线程。
                # 为了避免僵尸进程
                if 'p' in locals().keys():
                    while p.is_alive():
                        continue
                self.syslog.info('request process done.')
            except Exception, msg:
                self.syslog.error(msg)
