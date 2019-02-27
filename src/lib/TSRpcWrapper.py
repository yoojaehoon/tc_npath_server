import sys, glob
#sys.path.insert(0, glob.glob('/usr/lib/python2.6/site-packages/thrift/lib/py/build/lib*')[0])
#sys.path.insert(0, glob.glob('/root/thrift-0.9.3/lib/py/build/lib*')[0])

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
#from thrift.server import TServer
from thrift.server import TNonblockingServer

#from daemon import *
#from log import *
#from TSServices import *

#import traceback
#import time

#daemonize()

#log = prepare_log("preparelog")
#log.info("blabla")

class TSRpcWrapper():
    def __init__(self, processor, port):
        self.processor = processor
        self.transport = TSocket.TServerSocket(port=port)
        self.tfactory = TTransport.TBufferedTransportFactory()
        self.pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        #self.server = TServer.TThreadPoolServer(self.processor, self.transport , self.tfactory, self.pfactory)
        #self.server = TServer.TSimpleServer(self.processor, self.transport , self.tfactory, self.pfactory)
        self.server = TNonblockingServer.TNonblockingServer(self.processor, self.transport)

    def __del__(self):
        pass

    def setThreadPoolCount(self, count):
        self.server.setNumThreads(count)

    def start(self):
        self.server.serve()

    def stop(self):
        self.server.close()

if __name__ == '__main__':
    pass
