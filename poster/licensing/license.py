#-*- coding: utf-8 -*-

import json

from .request import Request, RequestError
from . import _utils


class LicenseError(Exception):
    pass


class License(object):
    """
    """
    def __init__(self, id, request, begin, duration, expire):
        self._fields = dict(
            id=id,
            request=request,
            begin=begin,
            duration=duration,
            expire=expire
        )

    def __getattribute__(self, attr):
        fields = ['id', 
                  'request', 
                  'begin', 
                  'duration', 
                  'expire']

        if attr == 'fields':
            return self._fields
        elif attr in fields:
            return self._fields[attr]
        else:
            return super(License, self).__getattribute__(attr)

    def __getitem__(self, item):
        return self._fields[item]

    def dumps(self):
        _tmp = self._fields.copy()
        _tmp['request'] = _tmp['request'].dumps()
        return json.dumps(_tmp)

    @staticmethod
    def loads(s):
        try:
            fields = json.loads(s)
            fields['request'] = Request.loads(fields['request'])
        except (ValueError, RequestError), e:
            raise LicenseError("Invalid License")

        return License(**fields)

    @staticmethod
    def new(licenseId, request, durationDays):
        begin = License.newLicenseBeginTime()
        duration = _utils.getDaysDurationInSecs(durationDays)
        expire = begin + duration
        
        return License(licenseId, request, 
                       begin, duration, expire)

    @staticmethod
    def newLicenseBeginTime():
        return _utils.get_network_time()
