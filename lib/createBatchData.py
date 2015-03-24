# -*- coding:utf-8 -*-
##  实时计算补数据
#  实时计算分割出增量数据
#  1.event类型log 
#        按照第二列日期分割
#  2.ec类型log
#        按照第二列下单时间分割
#  3.ec_detail类型log
#        按照第十一列商品时间分割


import os
import sys
import time
import datetime

ONEHOUR = datetime.timedelta(hours=1)
HOURFORMATE = "%Y-%m-%d"
MINUTEFORMATE = "%Y-%m-%d-%H-%M"#"%Y-%m-%d %H:%M:%S"
TWOMINUTE = datetime.timedelta(minutes=2)
tableName="jc_realtime_queue"
FILEMINUTEFORMATE="%Y-%m-%d.%H:%M" 
FILEHOURFORMATE="%Y-%m-%d.%H"        
outputFORMATE="%Y%m%d%H%M"

LOG_CONVERTOR_DATA = os.getenv('LOG_CONVERTOR_DATA')
def getTime(starttime,queueFormat):
    starttime=datetime.datetime.strptime(starttime,FILEMINUTEFORMATE)
    date=starttime.strftime(HOURFORMATE)
    hour=str(starttime.hour)
    minute=str(starttime.minute)
    minute= "0"+minute  if len(minute)==1 else minute
    
    max=datetime.timedelta(minutes=queueFormat-1)
    beginData=datetime.datetime.strptime(starttime.strftime("%Y-%m-%d %H:%M"),"%Y-%m-%d %H:%M")#2012-04-29 12:00
    beginData_max=beginData+max
    return date,hour,minute,beginData,beginData_max

#ec日志处理函数 按照第二列下单时间分割
def  doProcEcLog(projectId,starttime,queueFormat):#order.2012-05-09.16
    date,hour,minute,beginData,beginData_max = getTime(starttime,queueFormat)
    srcEcFile=''.join(["order.",date,".",hour])
    ordEcFile=''.join(["order.",date,".",hour,":",minute])
    
    ecPath=os.sep.join([LOG_CONVERTOR_DATA,"output","RTBatch",projectId,"ec"])
    if not os.path.exists(ecPath):
        os.makedirs(ecPath)
    srcEcPath = os.sep.join([LOG_CONVERTOR_DATA,"output","merge",projectId,"ec"])
    
    f=open(srcEcPath+os.sep+srcEcFile,"r")
    dataList = f.readlines()
    f.close()
    
    wList=[]
    for item in dataList:
        item=item.strip()
        itemArray = item.split('\t')
        filterTimeStr=itemArray[1]
        #filterTimeDate=datetime.datetime.strptime(filterTimeStr,"%Y-%m-%d %H:%M:%S")
        filterTimeDate=datetime.datetime.strptime(filterTimeStr[:-3],"%Y-%m-%d %H:%M")
        
        if  filterTimeDate>=beginData and filterTimeDate<=beginData_max:
            wList.append(item)
    f=open(ecPath+os.sep+ordEcFile,"w")
    f.write('\n'.join(wList))
    f.close()

#ec_detail日志处理函数  按照第十一列商品时间分割
def  doProcEcDetailLog(projectId,starttime,queueFormat):#order.2012-05-09.16
    date,hour,minute,beginData,beginData_max = getTime(starttime,queueFormat)
    srcEcFile=''.join(["order.detail.",date,".",hour])
    ordEcFile=''.join(["order.detail.",date,".",hour,":",minute])
    
    ecPath=os.sep.join([LOG_CONVERTOR_DATA,"output","RTBatch",projectId,"ec_detail"])
    if not os.path.exists(ecPath):
        os.makedirs(ecPath)
    srcEcPath = os.sep.join([LOG_CONVERTOR_DATA,"output","merge",projectId,"ec_detail"])
    
    f=open(srcEcPath+os.sep+srcEcFile,"r")
    dataList = f.readlines()
    f.close()
    
    wList=[]
    for item in dataList:
        item=item.strip()        
        itemArray = item.split('\t')
        filterTimeStr=itemArray[10]
        #filterTimeDate=datetime.datetime.strptime(filterTimeStr,"%Y-%m-%d %H:%M:%S")
        filterTimeDate=datetime.datetime.strptime(filterTimeStr[:-3],"%Y-%m-%d %H:%M")
        
        if  filterTimeDate>=beginData and filterTimeDate<=beginData_max:
            wList.append(item)
    f=open(ecPath+os.sep+ordEcFile,"w")
    f.write('\n'.join(wList))
    f.close()

#event日志处理函数  按照第二列日期分割
def  doProcEvent(projectId,starttime,queueFormat):#order.2012-05-09.16
    date,hour,minute,beginData,beginData_max = getTime(starttime,queueFormat)
    srcEcFile=''.join(["event.",date,".",hour])
    ordEcFile=''.join(["event.",date,".",hour,":",minute])
    
    ecPath=os.sep.join([LOG_CONVERTOR_DATA,"output","RTBatch",projectId,"event"])
    if not os.path.exists(ecPath):
        os.makedirs(ecPath)
    srcEcPath = os.sep.join([LOG_CONVERTOR_DATA,"output","merge",projectId,"event"])
    
    f=open(srcEcPath+os.sep+srcEcFile,"r")
    dataList = f.readlines()
    f.close()
    
    wList=[]
    for item in dataList:
        item=item.strip()        
        itemArray = item.split('\t')
        filterTimeStr=itemArray[1]
        #filterTimeDate=datetime.datetime.strptime(filterTimeStr,"%Y-%m-%d %H:%M:%S")
        filterTimeDate=datetime.datetime.strptime(filterTimeStr[:-3],"%Y-%m-%d %H:%M")
        
        if  filterTimeDate>=beginData and filterTimeDate<=beginData_max:
            wList.append(item)
    f=open(ecPath+os.sep+ordEcFile,"w")
    f.write('\n'.join(wList))
    f.close()





'''
projectId
starttime         "%Y-%m-%d.%H:%M" 2012-04-29.12:00
queueFormat
'''

def run(projectId,starttime,queueFormat):
    queueFormat=int(queueFormat.strip())
    doProcEcLog(projectId,starttime,queueFormat)
    doProcEcDetailLog(projectId,starttime,queueFormat)    
    doProcEvent(projectId,starttime,queueFormat)

if __name__ == "__main__":
    
    projectId="1152"
    starttime="2012-05-09.16:02"
    queueFormat="2"
    
    run(projectId,starttime,queueFormat)