#!/usr/bin/env python
#-*- coding: utf-8 -*-


class FBGraphError(Exception):
    """
    """
    
    def __init__(self, error):
        self.code = None
        self.type = None

        try:
            self.message = error['error']['message']
            self.code = error['error']['code']
            self.type = error['error']['type']
        except:
            self.message = str(error)
        
        super(FBGraphError, self).__init__(self.message)

