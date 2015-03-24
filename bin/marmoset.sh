#!/bin/sh
source $2
#///////////////////// System log file configure //////
jobtype=$1
errorlog=err.log
logpath=${LISPEED_LOG}
keeplog=${LISPEED_LIB}/util/keeplog
## .end
python ${MARMOSET_HOME}/lib/TcpWorkerThread.py $jobtype 2>&1 | $keeplog ${errorlog}.${jobtype} $logpath