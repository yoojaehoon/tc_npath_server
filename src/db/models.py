#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence, ForeignKey, Table
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class NEServer(Base):
    __tablename__ = 'ne_server'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    hostname = Column(String)
    uuid = Column(String)
    availability_zone = Column(String)
    project_type = Column(String)
    #flavor = Column(String, ForeignKey('hardware_spec.flavor'))
    nic1 = Column(String)
    nic2 = Column(String)
    updated_at = Column(DateTime, default=func.now())
    alive_status = relationship("AliveStatus", backref="ne_server", passive_deletes=True)

    def __init__(self, hostname, uuid, availability_zone, project_type, nic1=None, nic2 = None):
        self.hostname = hostname
        self.uuid = uuid
        self.availability_zone = availability_zone
        self.project_type = project_type
        #self.flavor = flavor
        self.nic1 = nic1
        self.nic2 = nic2

    def result(self):
        output = {}
        output['id'] = self.id
        output['hostname'] = self.hostname
        output['uuid'] = self.uuid
        output['availability_zone'] = self.availability_zone
        output['project_type'] = self.project_type
        output['nic1'] = self.nic1
        output['nic2'] = self.nic2
        #output['flavor'] = self.flavor

        return output

class HardwareSpec(Base):
    __tablename__ = 'hardware_spec'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    flavor = Column(String)
    cpu_core = Column(Integer)
    memory_volume = Column(Integer)
    memory_count = Column(Integer)
    disk_volume = Column(Integer)
    disk_count = Column(Integer)
    #ne_servers = relationship("NEServer", backref='hardware_spec')

    def __init__(self, flavor, cpu_core, memory_volume, memory_count, disk_volume, disk_count):
        self.flavor = flavor
        self.cpu_core = cpu_core
        self.memory_volume = memory_volume
        self.memory_count = memory_count
        self.disk_volume = disk_volume
        self.disk_count = disk_count
    def result(self):
        output = {}
        output['cpu_core'] = self.cpu_core
        output['memory_count'] = self.memory_count
        output['memory_volume'] = self.memory_volume
        output['disk_count'] = self.disk_count
        output['disk_volume'] = self.disk_volume
        return output

class AliveStatus(Base):
    __tablename__ = 'alive_status'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    hostname = Column(String(32))
    uuid = Column(String, ForeignKey('ne_server.uuid', ondelete='CASCADE'))
    project_type = Column(String(16))
    wmi_private_fx = Column(Boolean, default=False)
    wmi_private_fl = Column(Boolean, default=False)
    wmi_public_fx = Column(Boolean, default=False)
    wmi_public_fl = Column(Boolean, default=False)
    normal_public_fx = Column(Boolean, default=False)
    normal_public_fl = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=func.now())

    def __init__(self, hostname, uuid, project_type, wmi_private_fx=None, wmi_private_fl=None, wmi_public_fx=None, wmi_public_fl=None, normal_public_fx=None, normal_public_fl=None):
        self.hostname = hostname
        self.uuid = uuid
        self.project_type = project_type
        self.wmi_private_fx = wmi_private_fx
        self.wmi_private_fl = wmi_private_fl
        self.wmi_public_fx = wmi_public_fx
        self.wmi_public_fl = wmi_public_fl
        self.normal_public_fx = normal_public_fx
        self.normal_public_fl = normal_public_fl

    def result(self):
        output = {}
        output['id'] = self.id
        output['hostname'] = self.hostname
        output['uuid'] = self.uuid
        output['project_type'] = self.project_type
        output['wmi_private_fx'] = self.wmi_private_fx
        output['wmi_private_fl'] = self.wmi_private_fl
        output['wmi_public_fx'] = self.wmi_public_fx
        output['wmi_public_fl'] = self.wmi_public_fl
        output['normal_public_fx'] = self.normal_public_fx
        output['normal_public_fl'] = self.normal_public_fl
        output['updated_at'] = self.updated_at
        return output
