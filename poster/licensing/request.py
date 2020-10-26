#-*- coding: utf-8 -*-

import json

from . import _utils


class RequestError(Exception):
    pass



class Request(object):
    """
    """
    def __init__(self, **fields):

        fieldValidators = {
            'firstName' :   [_utils.checkNotNull, _utils.checkName], 
            'lastName'  :   [_utils.checkNotNull, _utils.checkName], 
            'email'     :   [_utils.checkNotNull, _utils.checkEmail], 
            'uuid'      :   [_utils.checkNotNull, _utils.checkUUID], 
            'hostname'  :   [_utils.checkNotNull, _utils.checkHostname], 
            'bios_sn'   :   [_utils.checkNotNull, _utils.checkBiosSN], 
            'hdd_sn'    :   [_utils.checkNotNull, _utils.checkHDDSN], 
            'cpu_id'    :   [_utils.checkNotNull, _utils.checkCPUID], 
            'mac'       :   [_utils.checkNotNull, _utils.checkMAC]
        }

        validFields = set(fieldValidators.keys())
        givenFields = set(fields.keys())

        invalidFields = givenFields - validFields
        missingFields = validFields - givenFields

        if invalidFields:
            raise RequestError("Invaid Request Fields : " + 
                               ", ".join(invalidFields))

        if missingFields:
            raise RequestError("Missing Request Fields : " + 
                               ", ".join(missingFields))

        for field, validators in fieldValidators.items():
            for validator in validators:

                value = fields[field]
                
                if not validator(value):
                    raise RequestError(
                            "Invalid Field Value : { %s: %s }" % 
                            (field, value)
                        )

        self._fields = fields

    def __getattribute__(self, attr):
        fields = ['firstName', 
                  'lastName', 
                  'email', 
                  'uuid', 
                  'hostname', 
                  'bios_sn', 
                  'hdd_sn', 
                  'cpu_id',
                  'mac']
        
        if attr == 'fields':
            return self._fields
        elif attr in fields:
            return self._fields[attr]
        else:
            return super(Request, self).__getattribute__(attr)

    def __getitem__(self, item):
        return self._fields[item]

    def dumps(self):
        return json.dumps(self._fields)

    @staticmethod
    def loads(s):
        try:
            fields = json.loads(s)
        except ValueError:
            raise RequestError("Invalid Request")

        return Request(**fields)
