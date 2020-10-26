#-*- coding: utf-8 -*-

import json
import time
from PyQt4.QtCore import *

from .cipher import *
from .request import Request, RequestError
from .license import License, LicenseError
from ._utils import *
from ..common import consts


class Licenser(QObject):
    """
    """
    class __impl(QObject):
        """
        """
        def __init__(self, parent=None):
            QObject.__init__(self, parent)

            self.cipher = Cipher()
            self.loadPublicKey()

            self.loadUsageDetails()
            self.loadLicense()

            self.saveUsageDetails()

        def loadPublicKey(self):
            _f = QFile(':/asc/public.asc')
            if _f.open(QFile.ReadOnly):
                key = str(_f.readAll())
                self.cipher.importPublicKey(key)
                return True
            return False

        def loadLicense(self):
            settings = QSettings()
            settings.beginGroup('license')

            self.firstName = unicode(settings.value('firstName').toString())
            self.lastName = unicode(settings.value('lastName').toString())
            self.email = unicode(settings.value('email').toString())
            self.request = unicode(settings.value('request').toString())
            self.b64req = unicode(settings.value('b64req').toString())
            self.license = unicode(settings.value('license').toString())

            settings.endGroup()

        def loadUsageDetails(self):
            settings = QSettings()
            settings.beginGroup('app')

            now_t = int(get_network_time())
            now = QDateTime.fromTime_t(now_t)
            
            installedOn_t, _ok = settings.value('installedOn').toInt()
            if not _ok:
                # get from another source
                installedOn_t = now_t
            
            self.installedOn = QDateTime.fromTime_t(installedOn_t)
            self.usageDays = abs(self.installedOn.daysTo(now))
            
            self.usageCount, _ok = settings.value('usageCount').toInt()
            if not _ok:
                # get from another source
                pass

            self.usageCount += 1

            settings.endGroup()
            
        def saveUsageDetails(self):
            settings = QSettings()
            settings.beginGroup('app')

            installedOn_dt = self.installedOn.toPyDateTime()
            installedOn_t = int(time.mktime(installedOn_dt.timetuple()))

            settings.setValue('installedOn', installedOn_t)
            settings.setValue('usageCount', self.usageCount)

            settings.endGroup()

        def isTrialActive(self):

            return (self.usageDays <= consts.APP_TRIAL_MAX_DAYS and 
                    self.usageCount <= consts.APP_TRIAL_MAX_USAGE)

        def saveLicense(self):
            settings = QSettings()
            settings.beginGroup('license')

            settings.setValue('firstName', self.firstName)
            settings.setValue('lastName', self.lastName)
            settings.setValue('email', self.email)
            settings.setValue('request', self.request)
            settings.setValue('b64req', self.b64req)
            settings.setValue('license', self.license)

            settings.endGroup()

        def hasLicense(self):
            """
            Check whether a license already exists or not.
            """
            infos = [self.firstName, 
                     self.lastName, 
                     self.email, 
                     self.request, 
                     self.b64req, 
                     self.license]
            return sum(bool(info) for info in infos) == len(infos)

        def checkUserLicense(self, license=None):
            """
            Check if the validity of the existing license.
            """
            if license is None:
                license = self.license

            try:
                licenseStruct = json.loads(self.cipher.decode(license))

                licenseData = licenseStruct['license']
                signature = licenseStruct['signature']

                if not self.cipher.verify(licenseData, 
                                          signature):
                    self.errorString = "License invalid"
                    return False

                licenseDump = self.cipher.decode(licenseData)
                licenseObj = License.loads(licenseDump)
                licenseRequestObj = licenseObj.request

                localRequstObj = Request.loads(self.cipher.decode(self.b64req))

                for field in licenseRequestObj.fields:
                    if licenseRequestObj[field] != localRequstObj[field]:
                        self.errorString = "License invalid"
                        return False

                currentTime = get_network_time()
                if currentTime < licenseObj.begin:
                    self.errorString = "License not validated"
                    return False
                elif currentTime > licenseObj.expire:
                    self.errorString = "License expired"
                    return False

                self.errorString = str()
                return licenseObj
            except:
                self.errorString = "License invalid"
                return False

        def setUserDetails(self, firstName, lastName, email):
            self.firstName = firstName
            self.lastName = lastName
            self.email = email
            self.saveLicense()

        def setUserLicense(self, license):
            self.license = license
            self.saveLicense()

        def generateRequest(self):
            fields = dict(
                firstName=self.firstName,
                lastName=self.lastName,
                email=self.email,
                uuid=get_uuid(),
                hostname=get_hostname(),
                bios_sn=get_bios_serial_number(),
                hdd_sn=get_hdd_serial_number(),
                cpu_id=get_processor_id(),
                mac=get_network_ifaces()[0]
            )

            try:
                reqObj = Request(**fields)
            except RequestError as e:
                self.errorString = e.message
                return

            reqDump = reqObj.dumps()
            self.b64req = self.cipher.encode(reqDump)
            self.request = self.cipher.encrypt(reqDump)
            self.saveLicense()

            return self.request

    __instance = None

    def __init__(self, parent=None):
        super(Licenser, self).__init__(parent)

        if Licenser.__instance is None:
            Licenser.__instance = Licenser.__impl()

        self.__dict__['_Licenser__instance'] = Licenser.__instance

    def __getattr__(self, attr):
        return getattr(Licenser.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(Licenser.__instance, attr, value)
