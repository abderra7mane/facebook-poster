#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from PyQt4.QtCore import *

from .graph import FBGraph
from .exceptions import FBGraphError
from ..common.utils import getSyncFile
from ..logging import logger


class FBProfileFetcher(QObject):
    """
    Retrieve all needed information about a user profile.
    """

    # started the job
    started = pyqtSignal()

    # finished all work
    finished = pyqtSignal(bool)

    # in case of errors
    error = pyqtSignal(unicode)

    # received some data and is prepared to deliver it
    readyRead = pyqtSignal(unicode)


    def __init__(self, access_token, 
                       session=requests.Session(), 
                       parent=None):

        super(FBProfileFetcher, self).__init__(parent)

        self.access_token = access_token

        self.session = session
        
        self.graph = FBGraph(access_token, self.session)
        
        self.data = dict()

        self.errorString = None

        self.logger = logger.getLogger()

    def start(self):

        self.logger.debug("[fetcher] start fetching...")
        
        self.started.emit()

        result = True

        _fn = [
            self._fetchUserInfo, 
            self._fetchUserPicture, 
            self._fetchUserGroups, 
            self._fetchUserPages, 
            self._fetchUserLikes, 
        ]

        for _f in _fn:

            result = (result and _f())

            if not result:

                self.logger.debug("[fetcher] fetcher error")

                break

        self.finished.emit(result)

    def _fetchUserInfo(self):

        self.logger.debug("[fetcher] fetching user info...")

        try:
            user_info = self.graph.get_user_info()

        except FBGraphError as e:

            self.logger.debug("[fetcher] fetching user info faild")

            self.errorString = e.message

            self.error.emit(self.errorString)

            return False

        self.data['user_info'] = user_info

        self.readyRead.emit('user_info')

        self.logger.debug("[fetcher] fetched user info")

        return True

    def _fetchUserPicture(self):

        self.logger.debug("[fetcher] fetching user picture...")

        try:
            user_picture_url = self.graph.get_user_picture_url()

            self.logger.debug("[fetcher] fetched user picture url")

        except FBGraphError as e:

            self.logger.debug("[fetcher] fetching user picture url failed")

            self.errorString = e.message

            self.error.emit(self.errorString)

            return False

        self.data['user_picture'] = dict()
        self.data['user_picture']['url'] = user_picture_url

        ok, data = getSyncFile(user_picture_url)

        if ok:
            self.data['user_picture']['data'] = QByteArray(data)

            self.readyRead.emit('user_picture')

            self.logger.debug("[fetcher] fetched user picture")

        else:
            self.errorString = data

            self.error.emit(self.errorString)

            self.logger.debug("[fetcher] fetching user picture failed")

            return False

        return True

    def _fetchUserGroups(self):

        self.logger.debug("[fetcher] fetching user groups...")

        try:
            user_groups = self.graph.get_user_groups()

        except FBGraphError as e:

            self.logger.debug("[fetcher] fetching user groups failed")

            self.errorString = e.message

            self.error.emit(self.errorString)

            return False

        self.data['user_groups'] = user_groups

        self.readyRead.emit('user_groups')

        self.logger.debug("[fetcher] fetched user groups")

        return True

    def _fetchUserPages(self):

        self.logger.debug("[fetcher] fetching user pages...")

        try:
            user_pages = self.graph.get_user_pages()

        except FBGraphError as e:

            self.logger.debug("[fetcher] fetching user pages failed")

            self.errorString = e.message

            self.error.emit(self.errorString)

            return False

        self.data['user_pages'] = user_pages

        self.readyRead.emit('user_pages')

        self.logger.debug("[fetcher] fetched user pages")

        return True

    def _fetchUserLikes(self):

        self.logger.debug("[fetcher] fetching user likes...")

        try:
            user_likes = self.graph.get_user_likes()

        except FBGraphError as e:

            self.logger.debug("[fetcher] fetching user likes failed")

            self.errorString = e.message

            self.error.emit(self.errorString)

            return False

        self.data['user_likes'] = user_likes

        self.readyRead.emit('user_likes')

        self.logger.debug("[fetcher] fetched user likes")

        return True

    def readData(self, type):

        self.logger.debug("[fetcher] reading fetched data...")

        if self.data.has_key(unicode(type)):
            return self.data[unicode(type)]

        else:
            self.error.emit("Trying to read non existent data.")
