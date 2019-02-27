#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

GLOBAL_CONF_PATH = '/opt/tc_npath_monitor/etc/global.conf'

def _parseConf():
    with open(GLOBAL_CONF_PATH, 'r') as f:
        conf = yaml.load(f)

    return conf

def getDBConf():
    global_conf = _parseConf()
    return global_conf['db']

def getApiConf():
    global_conf = _parseConf()
    return global_conf['api']

def getVmConf():
    global_conf = _parseConf()
    return global_conf['vm']

def getDaemonConf():
    global_conf = _parseConf()
    return global_conf['daemon']

if __name__ == '__main':
    ret = getDBConf()
