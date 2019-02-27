#!/usr/bin/env python
# -*- coding: utf-8 -*-

import array
import shutil
import string
import ast
import platform
import os
import sys
import commands
import struct
import socket
import fcntl
import rsa
import base64
import random
from pyasn1.type import univ
from pyasn1.codec.der import encoder as der_encoder


def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()

def setFileLock(file):
    if os.path.exists(file):
        cmd = "chattr +i %s" %(file)
        commands.getoutput(cmd)

def setFileUnlock(file):
    if os.path.exists(file):
        cmd = "chattr -i %s" %(file)
        commands.getoutput(cmd)

def setLinuxPassword(user, password):
    cmd = 'echo -e "%s\n%s" | passwd %s' %(password, password, user)
    commands.getoutput(cmd)

def getOSInfo():
    os_info = {}
    os_info['type'] = platform.system() 
    os_info['kernel'] = platform.release()
    os_info['dist'] = platform.dist()[0]
    os_info['version'] = platform.dist()[1]

    return os_info

def listInterfaces():
    is_64bits = sys.maxsize > 2**32
    struct_size = 40 if is_64bits else 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    max_possible = 8 # initial value
    while True:
        bytes = max_possible * struct_size
        names = array.array('B', '\0' * bytes)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            s.fileno(),
            0x8912,  # SIOCGIFCONF
            struct.pack('iL', bytes, names.buffer_info()[0])
        ))[0]
        if outbytes == bytes:
            max_possible *= 2
        else:
            break
    namestr = names.tostring()
    return [(namestr[i:i+16].split('\0', 1)[0],
        socket.inet_ntoa(namestr[i+20:i+24]))
        for i in range(0, outbytes, struct_size)]

def getIP(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname)
    )[20:24])

def getNetmask(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x891b, # SIOCGIFADDR
        struct.pack('256s',ifname)
    )[20:24])

def int2IP(intip):
    """ 
    convert integer IP to dotted format
    ex) 1234455 -> 8.8.8.8
    """
    octet = ''
    for exp in [3,2,1,0]:
        octet = octet + str(intip / ( 256 ** exp )) + "." 
        intip = intip % ( 256 ** exp )
    return octet.rstrip('.')

def ip2Int(dotted_ip):
    """ 
    convert dotted IP to Integer number
    ex) 8.8.8.8 -> 123455
    """
    exp = 3 
    intip = 0 
    for quad in dotted_ip.split('.'):
        intip = intip + (int(quad) * (256 ** exp))
        exp = exp - 1 
    return intip

def getRoutes():
    cmd = 'route -n'
    route_info = commands.getoutput(cmd) 
    routing_rules = route_info.split('\n')

    default_gw = ''
    routes = []
    for rule in routing_rules:
        rule_arr = rule.split()
        if rule_arr[0] not in ['Kernel', 'Destination']:
            if rule_arr[0] == '0.0.0.0':
                default_gw = rule_arr[1]
            else:
                dic = {}
                dic['dest'] = rule_arr[0]
                dic['gateway'] = rule_arr[1]
                dic['netmask'] = rule_arr[2]
                dic['iface'] = rule_arr[7]

                routes.append(dic)

    return (default_gw, routes)

def setMultiAuthentication():
    cmd = "echo 'RequiredAuthentications2 publickey,password' >> /etc/ssh/sshd_config"
    commands.getoutput(cmd)

    print "Set multiple authentication successfule!"

def convertSSHKey2RSA(ssh_pubkey):
    keydata = base64.b64decode(ssh_pubkey.split(None)[1])

    parts = []
    while keydata:
        # read the length of the data
        dlen = struct.unpack('>I', keydata[:4])[0]

        # read in <length> bytes
        data, keydata = keydata[4:dlen+4], keydata[4+dlen:]

        parts.append(data)

    e_val = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in
        parts[1]]))
    n_val = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in
        parts[2]]))

    pkcs1_seq = univ.Sequence()
    pkcs1_seq.setComponentByPosition(0, univ.Integer(n_val))
    pkcs1_seq.setComponentByPosition(1, univ.Integer(e_val))

    return '-----BEGIN RSA PUBLIC KEY-----\n%s-----END RSA PUBLIC KEY-----' %(base64.encodestring(der_encoder.encode(pkcs1_seq)))

def encryptRSA(value, pubkey_str):
    pubkey = rsa.PublicKey.load_pkcs1(pubkey_str)

    encrypted_value = rsa.encrypt(value, pubkey)

    return base64.b64encode(encrypted_value)

def makePassword(length=10):
    pwd = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + '!@#%') for x in range(length-1))
    return pwd + ''.join(random.choice('!@#%') for x in range(1))

def growPart(dev , hidden):
    cmd = 'growpart %s %d' %(dev , hidden)
    (status_code, result) = commands.getstatusoutput(cmd)

    return status_code
    
def resizeFS(devpth):
    cmd = 'resize2fs %s' %(devpth) 
    (status_code, result) = commands.getstatusoutput(cmd)

    return status_code

if __name__ == '__main__':
    pass
