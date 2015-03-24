#-*- coding:utf-8 -*-
'''
Created on 2011-8-24

@author: sengo
'''
import thread, threading
import ContextManage

counter = 0

class Tcpthread(threading.Thread):
    
    def __init__(self, threadname, workQueue, lock, times=0):
        self.lock = lock
        self.threadname = threadname
        self.queue = workQueue
        self.times = times
        self.syslog = ContextManage.syslog
        threading.Thread.__init__(self, name=threadname)
        
    def run(self):
        if self.times == 0:
            while True:
                self.doWork(True)
        else:
            while - -self.times > 0:
                self.doWork(False)

    def doWork(self, flag):
        try:
            self.lock.acquire()
            task = self.queue.get() # 如果队列为空则wait,队列有值时自动唤醒
            self.lock.release()
            task.run()
        except Exception, e:
            self.syslog.error(e)
        
#    def run(self):
#        global counter
#        #self.syslog.info(self.threadname)
#        if self.times == 0:
#            while True:
#                self.doWork(True)
#        else:
#            while - -self.times > 0:
#                self.doWork(False)
#            counter -= 1
#            
#    def doWork(self, flag):
#        try:
#            #self.syslog.debug('acquire before')
#            self.lock.acquire()
#            #self.syslog.debug('acquire')
#            global counter
#            #self.syslog.info('counter: ' + str(counter))
#            if counter > 1:
#                counter -= 1
#                task = self.queue.get() # 如果队列为空则wait,队列有值时自动唤醒
#                self.lock.release()
#                task.run()
#                counter += 1
#            else:
#                self.lock.release()
#                #self.syslog.info('else')
#                #time.sleep(10)
#                #pool = ThreadPool()
#                #pool.start2(ContextManage.minSpareThreads, 5)
#        except Exception, e: 
#            self.syslog.error(e)

class ThreadPool: 
    
    def __init__(self):
        self.lock = ContextManage.lock
        self.workQueue = ContextManage.queue
        self.syslog = ContextManage.syslog
        self.syslog.info('threadpool start!')
        
    # 默认最小线程数
    def start(self, num_of_threads): 
        global counter
        #counter = 0
        for i in xrange(int(num_of_threads)): 
            thread = Tcpthread('Thread ' + str(i), self.workQueue, self.lock, 0) 
            thread.start()
            counter += 1
    
    # 备用扩展线程 
    def start2(self, num_of_threads, times):
        global counter
        for i in xrange(int(num_of_threads)):
            thread = Tcpthread('Thread ' + str(i), self.workQueue, self.lock, times)
            thread.start()
            counter += 1
            
