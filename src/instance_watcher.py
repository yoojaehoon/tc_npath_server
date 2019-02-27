#!/usr/bin/env python
# -*- coding: utf-8 -*-

from manager import Manager
from tc_npath_monitor.src.lib import config
from datetime import datetime, timedelta
from tc_npath_monitor.src.lib.blabla_bot import *

class InstanceWatcher(Manager):
    def __init__(self):
        Manager.__init__(self)
        self.log = {}
        self.daemon_conf = config.getDaemonConf()

        self.interval = self.daemon_conf['interval']
        super(InstanceWatcher, self).__init__()

    def listVms(self,**kwargs):

        filter = {}

        if kwargs.has_key('hostname'):
            filter['hostname'] = kwargs['hostname']
        if kwargs.has_key('availability_zone'):
            filter['availability_zone'] = kwargs['availability_zone']
        if kwargs.has_key('uuid'):
            filter['uuid'] = kwargs['uuid']
        if kwargs.has_key('project_type'):
            filter['project_type']= kwargs['project_type']

        ne_server = self.engine.getModel('NEServer')
        vm_list = self.db_session.query(ne_server).filter_by(**filter)

        wmi_output = []
        normal_output = []
        for vm in vm_list:
            if vm.project_type == 'WMI':
                wmi_output.append(vm)
            else:
                normal_output.append(vm)

        return wmi_output , normal_output

    def _listErrVm(self):
        alivestatus = self.engine.getModel('AliveStatus')
        wmi_output = []
        normal_output = []
        dtnow = datetime.now()
        #interval = dtnow - timedelta(seconds = 15)
        interval = dtnow - timedelta(minutes = self.interval)

        for wmi_rs in self.db_session.query(alivestatus).filter(alivestatus.project_type == 'WMI').filter( (alivestatus.wmi_private_fx != True) | (alivestatus.wmi_private_fl != True) | (alivestatus.wmi_public_fx != True) | (alivestatus.wmi_public_fl != True) | (alivestatus.updated_at < interval) ).all():
            wmi_output.append(wmi_rs)

        for normal_rs in self.db_session.query(alivestatus).filter(alivestatus.project_type == 'NORMAL').filter( (alivestatus.normal_public_fx != True) | (alivestatus.normal_public_fl != True) | (alivestatus.updated_at < interval) ).all():
            normal_output.append(normal_rs)

        return wmi_output, normal_output

    def _listWmiVm(self):
        alivestatus = self.engine.getModel('AliveStatus')
        wmi_output = []
        for wmi_rs in self.db_session.query(alivestatus).filter(alivestatus.project_type == 'WMI').all():
            wmi_output.append(wmi_rs)

        return wmi_output

    def updateScilentVm(self):
        from pinger import Pinger

        alivestatus = self.engine.getModel('AliveStatus')
        ne_server = self.engine.getModel('NEServer')

        dtnow = datetime.now()
        interval = dtnow - timedelta(minutes = self.interval)
        
        ping = Pinger()
        hosts = []

        for alive_rs in self.db_session.query(alivestatus).filter(alivestatus.updated_at < interval):
            ne_rs = self.db_session.query(ne_server).filter(ne_server.uuid == alive_rs.uuid).one()
            if ping.ping(ne_rs.nic2):
                self.db_session.query(alivestatus).filter_by(uuid=uuid).update({'updated_at': datetime.now()})
                self.db_session.commit()

    def report(self):
        wmi_output , normal_output = self._listErrVm()
        data = {}

        ret = True
        DT_WMI = ""
        DT_NORMAL = ""

        if len(wmi_output) > 0:
            DT_WMI += "|\tHostname|\t WMI_PRIVATE_FX|\tWMI_PRIVATE_FL|\t WMI_PUBLIC_FX|\t WMI_PUBLIC_FL|\t LastReported|\n"
            for wmi in wmi_output:
                DT_WMI += "|\t %s |\t %s |\t %s |\t %s |\t %s |\t %s|\n" %(wmi.hostname , wmi.wmi_private_fx , wmi.wmi_private_fl, wmi.wmi_public_fx, wmi.wmi_public_fl , wmi.updated_at)
                #ret = datetime.now() - wmi.updated_at

        if len(normal_output) > 0:
            DT_NORMAL += "|\tHostname|\t NORMAL_PUBLIC_FX|\t NORMAL_PUBLIC_FL|\t LastReported|\n"
            for normal in normal_output:
                DT_NORMAL += "|\t %s |\t %s |\t %s |\t %s |\n" %(normal.hostname , normal.normal_public_fx, normal.normal_public_fl , normal.updated_at)
        
        DT_ALL = DT_WMI + DT_NORMAL
        if len(DT_ALL) > 0:
            drmsg = generate_post_data(DT_ALL)
            send_data(HOOK_URL,drmsg)

        return ret


    def report_daily(self):
        wmi_all_output = self._listWmiVm()
        data = {}
        ret = True
        DT_WMI = ""
        DT_NORMAL = ""

        for wmi in wmi_all_output:
            print "|\t %s |\t %s |\t %s |\t %s |\t %s |\t %s|\n" %(wmi.hostname , wmi.wmi_private_fx , wmi.wmi_private_fl, wmi.wmi_public_fx, wmi.wmi_public_fl , wmi.updated_at)



if __name__ == '__main__':
    iw = InstanceWatcher()
    rets = iw.report_influxDB()
    #rets = iw.updateScilentVm()
