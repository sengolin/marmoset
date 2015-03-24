#-*- coding:utf-8 -*-
'''
Created on Sep 21, 2011

@author: sengo
'''

"""
    等待子进程执行结束后接收子进程的返回值，向客户端回应
"""
global JOIN
JOIN = 'join'

"""
    子进程执行过程中可以随时返回数据，向客户端回应
"""
global UNJOIN
UNJOIN = 'unjoin'

"""
    taskQ节点追加taskid
"""
global TASKQ
TASKQ = 'taskq'

"""
    taskQ节点追加taskid
"""
global JOBQ
JOBQ = 'jobq'