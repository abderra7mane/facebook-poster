#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from PyQt4.QtCore import *
from PyQt4.QtNetwork import *

from .fetcher import FBProfileFetcher
from .profile import FBProfile
from .poster import Poster
from ..common.utils import qtCookies_to_list
from ..common import consts
from ..logging import logger


class DataManager(QObject):
    """
    Manage fetching, retrieving and saving the data related
    to the user profile and the application.
    """

    # task started
    taskStarted = pyqtSignal()

    # ready to get data
    taskReadyRead = pyqtSignal(unicode)

    # task finished
    taskFinished = pyqtSignal(bool)

    # on errors
    taskError = pyqtSignal(unicode)

    # task progress
    taskProgress = pyqtSignal(int)

    # task paused
    taskPaused = pyqtSignal()

    # task resumed
    taskResumed = pyqtSignal()

    # need to refresh access token
    tokenExpired = pyqtSignal()


    def __init__(self, parent=None):
        super(DataManager, self).__init__(parent)

        self.session = requests.Session()

        self.profiles = dict()

        self.currentProfileId = None
        self.currentProfile = None

        self.logger = logger.getLogger()

    def loadSavedProfiles(self):
        """
        Load previously saved profiles.
        """

        self.logger.debug("[manager] loading saved profiles...")

        settings = QSettings()

        settings.beginGroup('profiles')

        self.lastConnectedProfile = \
            settings.value('lastConnected').toString()

        profiles = settings.childGroups()

        for profile_key in profiles:
            
            settings.beginGroup(profile_key)

            userId = unicode(settings.value('id').toString())
            userName = unicode(settings.value('name').toString())
            userPictureUrl = unicode(settings.value('picture_url').toString())
            userPicture = settings.value('picture_data').toByteArray()

            # groups
            userGroups = list()

            # settings.beginGroup('groups')

            # groups_keys = settings.childGroups()

            # for group_key in groups_keys:

            #     settings.beginGroup(group_key)

            #     groupId = unicode(settings.value('id').toString())
            #     groupName = unicode(settings.value('name').toString())
            #     groupPrivacy = unicode(settings.value('privacy').toString())
            #     groupDescription = unicode(settings.value('description').toString())

            #     userGroups.append({
            #         'id': groupId,
            #         'name': groupName,
            #         'privacy': groupPrivacy,
            #         'description': groupDescription
            #     })

            #     settings.endGroup()

            # settings.endGroup()

            # pages
            userPages = list()

            # settings.beginGroup('pages')

            # pages_keys = settings.childGroups()

            # for page_key in pages_keys:

            #     settings.beginGroup(page_key)

            #     pageId = unicode(settings.value('id').toString())
            #     pageName = unicode(settings.value('name').toString())
            #     pageAccessToken = unicode(settings.value('access_token').toString())
            #     pageAbout = unicode(settings.value('about').toString())

            #     userPages.append({
            #         'id': pageId,
            #         'name': pageName,
            #         'access_token': pageAccessToken,
            #         'about': pageAbout
            #     })

            #     settings.endGroup()

            # settings.endGroup()

            # likes
            userLikes = list()

            # settings.beginGroup('likes')

            # likes_keys = settings.childGroups()

            # for like_key in likes_keys:

            #     settings.beginGroup(like_key)

            #     likeId = unicode(settings.value('id').toString())
            #     likeName = unicode(settings.value('name').toString())
            #     likeAbout = unicode(settings.value('about').toString())
            #     likeCanPost = bool(settings.value('can_post').toBool())

            #     userLikes.append({
            #         'id': likeId,
            #         'name': likeName,
            #         'about': likeAbout,
            #         'can_post': likeCanPost
            #     })

            #     settings.endGroup()

            # settings.endGroup()

            # access_token
            access_token = unicode(settings.value('access_token').toString())

            # cookies
            cookies = list()

            settings.beginGroup('cookies')

            cookies_keys = settings.childKeys()

            for cookie_key in cookies_keys:

                b64Cookie = settings.value(cookie_key).toByteArray()
                
                rawCookie = QByteArray.fromBase64(b64Cookie)
                
                parsedCookies = QNetworkCookie.parseCookies(rawCookie)
                
                cookies.extend(parsedCookies)

            settings.endGroup()

            # statistics

            settings.endGroup()

            profile = FBProfile(
                { 'id' : userId, 'name' : userName }, 
                
                { 'url' : userPictureUrl, 'data' : userPicture }, 

                userGroups, 

                userPages, 

                userLikes,

                access_token,

                cookies,
            )

            self.profiles[profile.userId] = profile

        settings.endGroup()

    def saveProfiles(self):
        """
        Save profile.
        """

        self.logger.debug("[manager] saving profiles...")

        settings = QSettings()

        settings.beginGroup('profiles')

        settings.setValue(
            'lastConnected', self.lastConnectedProfile)

        for id in self.profiles:

            profile = self.profiles[id]
            
            settings.beginGroup(id)

            # user
            settings.setValue('id', profile.userId)
            settings.setValue('name', profile.userName)
            settings.setValue('picture_url', profile.userPictureUrl)
            settings.setValue('picture_data', profile.userPicture)
            
            # groups
            # settings.beginGroup('groups')

            # for group in profile.userGroups:

            #     settings.beginGroup(group['id'])

            #     settings.setValue('id', group['id'])
            #     settings.setValue('name', group['name'])
            #     settings.setValue('privacy', group['privacy'])

            #     try:
            #         settings.setValue('description', group['description'])

            #     except KeyError:
            #         settings.setValue('description', group['name'])

            #     settings.endGroup()

            # settings.endGroup()

            # pages
            # settings.beginGroup('pages')
            
            # for page in profile.userPages:

            #     settings.beginGroup(page['id'])

            #     settings.setValue('id', page['id'])
            #     settings.setValue('name', page['name'])
            #     settings.setValue('access_token', page['access_token'])

            #     try:
            #         settings.setValue('about', page['about'])

            #     except KeyError:
            #         settings.setValue('about', page['name'])

            #     settings.endGroup()

            # settings.endGroup()
            
            # likes
            # settings.beginGroup('likes')
            
            # for like in profile.userLikes:

            #     settings.beginGroup(like['id'])

            #     settings.setValue('id', like['id'])
            #     settings.setValue('name', like['name'])

            #     try:
            #         settings.setValue('about', like['about'])

            #     except KeyError:
            #         settings.setValue('about', like['name'])
                
            #     settings.setValue('can_post', like['can_post'])

            #     settings.endGroup()

            # settings.endGroup()

            # access_token
            settings.setValue('access_token', profile.accessToken)

            # cookies
            settings.beginGroup('cookies')

            for c, cookie in enumerate(profile.cookies):

                rawCookie = cookie.toRawForm()
                
                b64Cookie = rawCookie.toBase64()
                
                settings.setValue(str(c), b64Cookie)

            settings.endGroup()

            # statistics

            settings.endGroup()

        settings.endGroup()

    def setTmpProfileCookies(self, cookies):
        """
        Update the temporary profile set of cookies.
        """

        self.logger.debug("[manager] saving profile cookies...")

        if not hasattr(self, '_tmpProfileData') or \
                self._tmpProfileData is None:

            self._tmpProfileData = dict()

        self._tmpProfileData['cookies'] = cookies

        self.setSessionCookies(cookies)

    def setSessionCookies(self, cookies):

        self.logger.debug("[manager] setting session cookies...")

        for cookie in qtCookies_to_list(cookies):
                
            self.session.cookies.set(**cookie)

    def getCurrentUserCookies(self):

        if self.currentProfile:

            return self.currentProfile.cookies

    def fetchUserProfile(self, access_token, cookies=None):
        """
        Fetch a user profile information.
        """

        self.logger.debug("[manager] fetching user profile...")

        if not hasattr(self, '_tmpProfileData') or \
                self._tmpProfileData is None:

            self._tmpProfileData = dict()

        self._tmpProfileData['access_token'] = access_token

        if cookies:

            self.setSessionCookies(cookies)

            self._tmpProfileData['cookies'] = cookies

        elif not self._tmpProfileData.has_key('cookies'):
            
            self._tmpProfileData['cookies'] = None

        self.fetcher = FBProfileFetcher(access_token, self.session)

        self.fetcherThread = QThread(self)
        self.fetcher.moveToThread(self.fetcherThread)

        self.fetcher.started.connect(self.fetcherStarted)
        self.fetcher.readyRead.connect(self.fetcherDataReady)
        self.fetcher.finished.connect(self.fetcherFinished)
        self.fetcher.error.connect(self.fetcherError)

        self.fetcher.finished.connect(self.fetcherThread.quit)
        self.fetcher.finished.connect(self.fetcher.deleteLater)

        self.fetcherThread.started.connect(self.fetcher.start)
        self.fetcherThread.finished.connect(self.fetcherThread.deleteLater)

        self.fetcherThread.start()

    def fetcherStarted(self):

        self.logger.debug("[manager] fetcher started")

        self.taskStarted.emit()

    def fetcherDataReady(self, type):
        """
        Read received user data, save it to a temporary place.
        """

        self.logger.debug("[manager] fetcher data ready")

        type = unicode(type)

        data = self.fetcher.readData(type)

        self._tmpProfileData[type] = data

        self.taskReadyRead.emit(type)

    def fetcherFinished(self, ok):
        """
        Check all received data, build a profile object 
        and possibly report errors.
        """

        self.logger.debug("[manager] fetcher task finished")

        if ok:

            _newProfile = FBProfile(
                self._tmpProfileData['user_info'], 
                self._tmpProfileData['user_picture'], 
                self._tmpProfileData['user_groups'], 
                self._tmpProfileData['user_pages'], 
                self._tmpProfileData['user_likes'], 
                self._tmpProfileData['access_token'], 
                self._tmpProfileData['cookies'], 
                self
            )

            self.insertOrUpdateProfile(_newProfile)

            self.currentProfileId = _newProfile.userId
            
            self.lastConnectedProfile = self.currentProfileId

            self.currentProfile = self.profiles[self.currentProfileId]

        self._tmpProfileData = None

        self.taskFinished.emit(ok)

    def fetcherError(self, errorString):
        """
        Report errors happening during fetching process.
        """

        self.logger.debug("[manager] fetcher error")

        self.taskError.emit(errorString)

    def readFetchedData(self, type):
        """
        Read fetched user data from the temporary place.
        """

        self.logger.debug("[manager] reading fetched data")

        return self._tmpProfileData[type]

    def insertOrUpdateProfile(self, profile):
        """
        Inserts a new profile or updates an existing profile.
        """

        self.logger.debug("[manager] saving fetched profile")

        if self.profiles.has_key(profile.userId):

            self.logger.debug("[manager] profile already exists")

            self.profiles[profile.userId].updateData(profile)

        else:

            self.profiles[profile.userId] = profile

    def getCurrentUserGroups(self):
        """
        Returns the current logged in user profile groups.
        """

        return self.currentProfile.userGroups

    def getCurrentUserPages(self):
        """
        Returns the current logged in user profile pages.
        """

        return self.currentProfile.userPages

    def getCurrentUserLikes(self):
        """
        Returns the current logged in user profile liked pages.
        """

        return self.currentProfile.userLikes

    def schedulePoster(self, tasks, config):
        """
        Initialize and start a post scheduler.
        """

        self.logger.debug("[manager] scheduling poster task...")

        if not self.currentProfileId:
            return

        config['access_token'] = \
            self.currentProfile.accessToken

        config['session'] = self.session

        config['tasks'] = tasks

        self.poster = Poster(**config)

        self.posterThread = QThread(self)
        self.poster.moveToThread(self.posterThread)

        self.poster.started.connect(self.posterStarted)
        self.poster.finished.connect(self.posterFinished)
        self.poster.paused.connect(self.posterPaused)
        self.poster.resumed.connect(self.posterResumed)
        self.poster.error.connect(self.posterError)
        self.poster.progress.connect(self.posterProgress)

        self.poster.finished.connect(self.posterThread.quit)
        self.poster.finished.connect(self.poster.deleteLater)

        self.posterThread.started.connect(self.poster.start)
        self.posterThread.finished.connect(self.posterThread.deleteLater)

        self.posterThread.start()

    def posterStarted(self):

        self.logger.debug("[manager] poster task started")

        self.taskStarted.emit()

    def posterFinished(self, ok):

        self.logger.debug("[manager] poster task finished")

        self.taskFinished.emit(ok)

    def posterPaused(self):

        self.logger.debug("[manager] poster task paused")

        self.taskPaused.emit()

    def posterResumed(self):

        self.logger.debug("[manager] poster task resumed")

        self.taskResumed.emit()

    def posterProgress(self, progress):

        self.logger.debug(
            "[manager] poster task progress : {0}", progress)

        self.taskProgress.emit(progress)

    def posterError(self, errorString):

        self.logger.debug("[manager] poster task error")

        if unicode(errorString).find('expired') >= 0 or \
            unicode(errorString).find('invalidated') >= 0:

            self.logger.debug("[manager] token expired/invalidated")

            self.tokenExpired.emit()

        else:

            self.resumePoster()

            self.taskError.emit(errorString)

    def pausePoster(self):

        if hasattr(self, 'poster') and self.poster:

            self.poster.pause()

    def resumePoster(self):

        if hasattr(self, 'poster') and self.poster:

            self.poster.resume()

    def stopPoster(self):

        if hasattr(self, 'poster') and self.poster:

            self.poster.stop()

    def currentUserDisconnected(self):

        self.logger.debug("[manager] disconnected")

        self.currentProfileId = None

    def updateToken(self, access_token):

        self.logger.debug("[manager] updaing token")

        self.currentProfile.accessToken = access_token

        self.updatePosterToken(access_token)

    def tokenUpdateFailed(self):

        self.logger.debug("[manager] token update failed")

        self.stopPoster()

    def updatePosterToken(self, access_token):

        self.logger.debug("[manager] updating poster token")

        if hasattr(self, 'poster') and self.poster:

            self.poster.updateAccessToken(access_token)

            self.poster.setRepublishLastFlag(True)

            self.poster.resume()

