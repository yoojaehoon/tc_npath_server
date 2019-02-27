import sys, glob
#sys.path.append('../../gen-py')
sys.path.append('/opt/tc_npath_monitor/gen-py')

from tcnpathmonitor import ServerSvc
from tcnpathmonitor.ttypes import *

from tc_npath_monitor.src.lib import config
from manager import Manager

class ServerSvcHandler(Manager):
    def __init__(self):
        Manager.__init__(self)

        self.log = {}
        super(ServerSvcHandler, self).__init__()

    def ping(self):
        print('ping received')

    def registVm(self, vminfo):
        from datetime import datetime
        ret = OP_RESULT()

        ne_server = self.engine.getModel('NEServer')
        vm = self.db_session.query(ne_server).filter_by(uuid=vminfo.uuid)
        #vm = self.db_session.query(ne_server).filter_by(uuid=vminfo.uuid).one()

        if vm.count() == 0:
            new_vm = self.engine.getModel('NEServer')(vminfo.hostname, vminfo.uuid, vminfo.availability_zone, vminfo.project_type,
                                                        vminfo.nic1, vminfo.nic2)
            self.db_session.add(new_vm)
            self.db_session.commit()
#        elif vm['hostname'] != vminfo.hostname or vm['availability_zone'] != vminfo.availability_zone
#                                               or vm['flavor'] != vminfo.flavor
#                                               or vm['nic1'] != vminfo.nic1
#                                               or vm['nic2'] != vminfo.nic2:
        else:
            self.db_session.query(ne_server).filter_by(uuid=vminfo.uuid).update({'hostname':vminfo.hostname,
                                                                                 'availability_zone':vminfo.availability_zone,
                                                                                 'nic1':vminfo.nic1,
                                                                                 'nic2':vminfo.nic2} )
            self.db_session.commit()
            

        ret.rcode = RETURN_CODE.RC_SUCCESS
        ret.reason = "Success"
        
        return ret

    def reportAlive(self, uuid, aliveinfo):
        from datetime import datetime
        from sqlalchemy.orm.exc import NoResultFound

        ret = OP_RESULT()
        ret.rcode = RETURN_CODE.RC_FAIL
        alivestatus = self.engine.getModel('AliveStatus')
        ne_server = self.engine.getModel('NEServer')
        try:
            vm = self.db_session.query(ne_server).filter_by(uuid=uuid).one()
            vm_result = vm.result()

            try:
                alive = self.db_session.query(alivestatus).filter_by(uuid=uuid).one()
                alive_result = alive.result()
                if vm_result['project_type'] == "WMI":
                    self.db_session.query(alivestatus).filter_by(uuid=uuid).update( {'wmi_private_fx':aliveinfo.wmi_private_fx,
                                                                                    'wmi_private_fl':aliveinfo.wmi_private_fl,
                                                                                    'wmi_public_fx':aliveinfo.wmi_public_fx,
                                                                                    'wmi_public_fl':aliveinfo.wmi_public_fl,
                                                                                    'updated_at': datetime.now()} )
                else:
                    self.db_session.query(alivestatus).filter_by(uuid=uuid).update( {'normal_public_fx':aliveinfo.normal_public_fx,
                                                                                    'normal_public_fl':aliveinfo.normal_public_fl,
                                                                                    'updated_at': datetime.now()} )
                self.db_session.commit()
                    
            except NoResultFound, e:
                if vm_result['project_type'] == "WMI":
                    new_vm = self.engine.getModel('AliveStatus')(vm_result['hostname'],uuid,'WMI',
                                    aliveinfo.wmi_private_fx,aliveinfo.wmi_private_fl,
                                    aliveinfo.wmi_public_fx,aliveinfo.wmi_public_fl,
                                    None,None)

                else:
                    new_vm = self.engine.getModel('AliveStatus')(vm_result['hostname'],uuid,'NORMAL',
                                    None,None,
                                    None,None,
                                    aliveinfo.normal_public_fx,aliveinfo.normal_public_fl)

                self.db_session.add(new_vm)
                self.db_session.commit()
            except Exception as e:
                print e

            ret.rcode = RETURN_CODE.RC_SUCCESS
            ret.reason = "SUCCESS"
        except NoResultFound, e:
            print "Error vm : %s" %(uuid)
            print e
            ret.rcode = RETURN_CODE.RC_SERVER_NOT_FOUND
            ret.reason = 'DB has not VM Info'

        #if vm.count() == 0:
        #    ret.rcode = RETURN_CODE.RC_SERVER_NOT_FOUND
        #    ret.reason = 'DB has not VM Info'
        #else:
        #    l_alive = self.db_session.query(alivestatus).filter_by(uuid=uuid)
            """
            if l_alive.count() == 0:
                if vm['project_type'] == "WMI":
                    new_vm = self.engine.getModel('AliveStatus')(vm['hostname'],uuid,
                                    aliveinfo.wmi_private_fx,aliveinfo.wmi_private_fl,
                                    aliveinfo.wmi_public_fx,aliveinfo.wmi_public_fl,
                                    None,None)

                else:
                    new_vm = self.engine.getModel('AliveStatus')(vm['hostname'],uuid,
                                    None,None,
                                    None,None,
                                    aliveinfo.normal_public_fx,aliveinfo.normal_public_fl)

                    self.db_session.add(new_vm)
                    self.db_session.commit()
            else:
                if vm['project_type'] == "WMI":
                    self.db_session.query(alivestatus).filter_by(uuid=uuid).update( {'wmi_private_fx':aliveinfo.wmi_private_fx,
                                                                                    'wmi_private_fl':aliveinfo.wmi_private_fl,
                                                                                    'wmi_public_fx':aliveinfo.wmi_public_fx,
                                                                                    'wmi_public_fl':aliveinfo.wmi_public_fl} )
                else:
                    self.db_session.query(alivestatus).filter_by(uuid=uuid).pudate( {'normal_public_fx':aliveinfo.normal_public_fx,
                                                                                    'normal_public_fl':aliveinfo.normal_public_fl} )
                self.db_session.commit()
                    
            ret.rcode = RETURN_CODE.RC_SUCCESS
            ret.reason = "SUCCESS"
            """
        print ret.reason
        return ret
