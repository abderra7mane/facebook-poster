#-*- coding: utf-8 -*-

import binascii
import time
import json

from .cipher import Cipher, CipherException
from .request import Request, RequestError
from .license import License


class KeygenError(Exception):
    pass


class Keygen(object):
    """
    """

    LICENSE_ID_SIZE = 128

    def __init__(self):
        self.cipher = Cipher()
        self.loadPrivateKey()

    def loadPrivateKey(self):
        import os
        _dir = os.path.dirname(__file__)
        _relpath = '..\\rc\\asc\\private.asc'
        _path = os.path.join(_dir, _relpath)
        with open(_path, 'rb') as _file:
            key = _file.read()
            self.cipher.importPrivateKey(key)
            return True
        return False

    def genereateLicense(self, request, durationDays):
        reqObj = self.parseLicenseRequst(request)
        
        if reqObj is None:
            raise KeygenError("Invalid Request")

        licenseId = self.genereateLicenseId()
        licenseObj = License.new(licenseId, reqObj, durationDays)

        licenseData = self.cipher.encode(licenseObj.dumps())
        signature = self.cipher.sign(licenseData)

        licenseStruct = dict(
            license=licenseData, 
            signature=signature
        )

        license = self.cipher.encode(json.dumps(licenseStruct))
        return license

    def parseLicenseRequst(self, request):
        try:
            plain = self.cipher.decrypt(request)
            return Request.loads(plain)
        except CipherException:
            return
        except RequestError:
            return

    def genereateLicenseId(self):
        randomBytes = self.cipher.random(self.LICENSE_ID_SIZE)
        return binascii.hexlify(randomBytes)



if __name__ == '__main__':
    import sys, argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('request', help="the license request")
    parser.add_argument('duration', type=int, help="the license duration in days")
    args = parser.parse_args()
    
    keygen = Keygen()
    try:
        request = keygen.parseLicenseRequst(args.request)
        license = keygen.genereateLicense(args.request, args.duration)
    except KeygenError as e:
        print e.message
        sys.exit()

    print ""
    print "###########################    Request    ###########################"
    print ""
    print "first name : " + request.firstName
    print "last name  : " + request.lastName
    print "email      : " + request.email
    print "uuid       : " + request.uuid
    print "hostname   : " + request.hostname
    print "bios sn    : " + request.bios_sn
    print "cpu id     : " + request.cpu_id
    print "hdd sn     : " + request.hdd_sn
    print "mac        : " + request.mac
    print ""
    print "###########################    License    ###########################"
    print ""
    print license
    print ""
    print "#####################################################################"
    print ""

