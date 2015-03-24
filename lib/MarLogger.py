#-*- coding:utf-8 -*-
'''
Created on 2011-8-29

@author: sengo
'''
import os
import logging

def initSysLog(logpath, formatter, timestamp):
        if(not os.path.exists(logpath)):
                os.mkdir(logpath)
        logfile = logpath + '/sys.log'
        logger = logging.getLogger()
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter(formatter)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.NOTSET)

        return logger
