#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4.QtCore import *

from ..logging import logger


class FBProfile(QObject):
    """
    Facebook Profile.
    """

    def __init__(self, user_info, 
                       user_picture, 
                       user_groups, 
                       user_pages, 
                       user_likes, 
                       access_token, 
                       cookies, 
                       parent=None):

        super(FBProfile, self).__init__(parent)

        self.userId = user_info['id']
        
        self.userName = user_info['name']
        
        self.userPictureUrl = user_picture['url']
        
        self.userPicture = user_picture['data']
        
        self.userGroups = user_groups
        
        self.userPages = user_pages
        
        self.userLikes = user_likes

        self.accessToken = access_token

        self.cookies = cookies

        self.logger = logger.getLogger()

    def resetStatistics(self):

        ## profile stats
        ##      nb times connected
        ##      first time connected
        ##      last time connected
        ##      nb times connected
        ##      nb times connected last day
        ##      nb times connected last week
        ##      nb times connected last month
        ##      nb times connected last year
        ##      average time spent connected

        ## publish stats
        ##      publshied successfull
        ##      not published
        ##      total
        ##      time spent
        ##      published in last day
        ##      published in last week
        ##      published in last month
        ##      published in last year
        ##      average publish by day
        ##      average publish by week
        ##      average publish by month
        ##      average publish by year

        ## app stats
        ##      nb times executed
        ##      nb times executed last day
        ##      nb times executed last week
        ##      nb times executed last month
        ##      nb times executed last year
        ##      average executed by day
        ##      average executed by week
        ##      average executed by month
        ##      average executed by year

        self.logger.debug("[profile] resetting profile statistics...")

        pass

    def updateData(self, profile):

        self.logger.debug("[profile] updating profile data...")

        self.userName = profile.userName
        
        self.userPictureUrl = profile.userPictureUrl
        
        self.userPicture = profile.userPicture
        
        self.userGroups = profile.userGroups
        
        self.userPages = profile.userPages
        
        self.userLikes = profile.userLikes

        self.accessToken = profile.accessToken

        self.cookies = profile.cookies

        pass

        ### update stats

