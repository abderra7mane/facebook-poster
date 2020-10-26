#-*- coding: utf-8 -*-

import re
import base64
import uuid
import time
import os
import win32api
import socket
from functools import partial
from Crypto.PublicKey import RSA

from ..common import consts
from ..packages import wmi
from ..packages import ntplib

#####################################################################
#                                                                   #
# Note: some functions here may take a while to retrun a result     #
#       depending on the machine and other stuff, so it's better    #
#       to run them only once and save the result somewhere else    #
#       for later reuse.                                            #
#                                                                   #
#####################################################################

def get_hdd_serial_number():
    """
    Return the serial number for the attached Hard Disk Drive if possible, 
    otherwise return the windows installation volume serial number.

    See note above.
    """
    sn = None
    try:
        c = wmi.WMI()
        for m in c.Win32_PhysicalMedia():
            sn = str(m.SerialNumber.strip())
            break
    except:
        try:
            sn = os.popen(
                    'wmic path win32_physicalmedia get SerialNumber'
                ).read().split()[1].strip()
            if not sn:
                raise Exception
        except:
            try:
                win_vol = get_windows_volume()
                sn = win32api.GetVolumeInformation(win_vol)[1]
                sn = hex(sn)[2:].upper()
            except:
                pass
    if not checkNotNull(sn):
        sn = 'A01B02C03D04E5'
    return sn

def get_windows_volume():
    """
    Return the Windows installation volume name.
    """
    win_dir = win32api.GetWindowsDirectory()
    win_vol = win_dir.split('\\')[0] + '\\'
    return win_vol

def get_processor_id():
    """
    Return the processor id.
    """
    pid = None
    try:
        pid = os.popen(
                'wmic cpu get ProcessorId'
            ).read().split()[1].strip()
        if not pid:
            raise Exception
    except:
        try:
            c = wmi.WMI()
            for p in c.Win32_Processor():
                pid = str(p.ProcessorId)
                break
        except:
            pass
    if not checkNotNull(pid):
        pid = 'A1B2C3D4E5F6G7H8'
    return pid

def get_network_ifaces():
    """
    Return the list of MAC addresses for attached physical network interfaces.
    """
    ifaces = list()
    try:
        output = os.popen(
                'wmic nic get MACAddress,PhysicalAdapter'
            ).read()
        lines = output.split('\n')[1:] ## skip header
        for line in lines:
            iface = line.split()
            if len(iface) != 2:
                continue
            mac, physical = iface
            if physical.upper() == 'TRUE':
                ifaces.append(str(mac))
    except:
        try:
            c = wmi.WMI()
            for iface in c.Win32_NetworkAdapter():
                mac = iface.MACAddress
                physical = iface.PhysicalAdapter
                if physical and mac:
                    ifaces.append(str(mac))
        except:
            pass
    if not ifaces:
        ifaces.append('AA:BB:CC:DD:EE:FF')
    return ifaces

def get_bios_serial_number():
    """
    Return the serial number of the BIOS.
    """
    sn = None
    try:
        c = wmi.WMI()
        for i in c.Win32_Bios():
            sn = str(i.SerialNumber)
            break
    except:
        try:
            sn = os.popen(
                    'wmic bios get SerialNumber'
                ).read().split()[1].strip()
            if not sn:
                raise Exception
        except:
            pass
    if not checkNotNull(sn):
        sn = '0123456'
    return sn

def get_hostname():
    """
    Return the hostname.
    """
    hostname = None
    try:
        hostname = win32api.GetComputerName()
    except:
        hostname = socket.gethostname()
    if not checkNotNull(hostname):
        hostname = 'DEFAULT'
    return hostname

def get_network_time():
    """
    Return the current time from the internet if possible, 
    otherwise return the local time.
    """
    try:
        c = ntplib.NTPClient()
        r = c.request('pool.ntp.org')
        t = r.tx_time
    except:
        t = time.time()
    return t

def get_uuid():
    """
    Return a user unique id.
    """
    return uuid.uuid1().hex

def getDaysDurationInSecs(duration):
    secsInDay = 24 * 3600
    return duration * secsInDay


def checkNotNull(arg):
    return bool(arg)

def checkNameLength(name):
    return (name is not None and
            consts.USER_NAME_MINLEN <= len(name.strip()) <= consts.USER_NAME_MAXLEN)

def checkName(name):
    nameRegExp = r'^[A-Z ]+$'
    return (checkNameLength(name) and 
            bool(re.match(nameRegExp, name, re.IGNORECASE)))

def checkEmail(email):
    emailRegExp = r'^[A-Z0-9._-]+@([A-Z0-9-]+\.)+[A-Z]{2,}$'
    return bool(re.match(emailRegExp, email, re.IGNORECASE))

def checkUUID(_uuid):
    try:
        uuid.UUID(hex=_uuid)
    except ValueError:
        return False
    return True

def checkHostname(hostname):
    return (get_hostname() == hostname)

def checkBiosSN(bios_sn):
    return (get_bios_serial_number() == bios_sn)

def checkHDDSN(hdd_sn):
    return (get_hdd_serial_number() == hdd_sn)

def checkCPUID(cpu_id):
    return (get_processor_id() == cpu_id)

def checkMAC(mac):
    macRegExp = r'^[0-9A-Z]{2}(:[0-9A-Z]{2}){5}$'
    return bool(re.match(macRegExp, mac, re.IGNORECASE))


if __name__ == '__main__':

    print 'collecting information...',
    sn = get_hdd_serial_number()
    vol = get_windows_volume()
    pid = get_processor_id()
    ifaces = get_network_ifaces()
    print '\r',
    print 'HDD serial number :', sn
    print 'Windows volume    :', vol
    print 'Processor ID      :', pid
    print 'Network Interfaces:'
    for i, mac in enumerate(ifaces):
        print '  %02d. %s' % (i+1, mac)
