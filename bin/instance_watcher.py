from tc_npath_monitor.src.instance_watcher import InstanceWatcher
from tc_npath_monitor.src.lib.daemon import *
import time
import threading

from tc_npath_monitor.src.lib.log import *

log = prepare_log('/opt/tc_npath_monitor/log/instance_watcher.log')

daemonize()

instance_watcher = InstanceWatcher()

def reporter():
    while True:
        try:
            instance_watcher.report()
            time.sleep(15)
        except Exception as e:
            log.error('repoter Error reason [ %s ]' %(e.message))

def updator():
    while True:
        try:
            instance_watcher.updateScilentVm()
            time.sleep(600)
        except Exception as e:
            log.error('updator Error reason [ %s ]' %(e.message))

rp = threading.Thread(name='reporter', target=reporter)
ud = threading.Thread(name='updator', target=updator)

rp.start()
ud.start()

rp.join()
ud.join()
