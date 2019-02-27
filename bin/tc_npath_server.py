#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tc_npath_monitor.src.lib.TSRpcWrapper import TSRpcWrapper
from tc_npath_monitor.src.TnpathMonServices import *
from tc_npath_monitor.src.lib.daemon import *
from tc_npath_monitor.src.lib.log import *

from tc_npath_monitor.src.lib.daemon import *

daemonize()

handler = ServerSvcHandler()
processor = ServerSvc.Processor(handler)

tsrpc = TSRpcWrapper(processor, 9090)
tsrpc.setThreadPoolCount(40)

#print "Thrift Server"
tsrpc.start()
