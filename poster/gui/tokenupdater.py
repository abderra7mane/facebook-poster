#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from PyQt4.QtWebKit import *

from ..common.utils import fetchTokenFromUrl, fetchErrorFromUrl
from ..common import consts


class TokenUpdater(QObject):
    """
    """

    ## token updated
    tokenAcquired = pyqtSignal(unicode)

    ## error
    tokenUpdateError = pyqtSignal(unicode)

    def __init__(self, cookies, 
                       version=consts.FB_GRAPH_DEFAULT_VERSION, 
                       parent=None):
        super(TokenUpdater, self).__init__(parent)

        self.cookies = cookies

        self.version = version

        self.cookieJar = QNetworkCookieJar()
        self.cookieJar.setAllCookies(self.cookies)

        self.nam = QNetworkAccessManager(self)
        self.nam.setCookieJar(self.cookieJar)

        self.webView = QWebView()
        self.webView.page().setNetworkAccessManager(self.nam)

        self.webView.urlChanged.connect(self.urlChanged)

    def start(self):

        self.loadAccessTokenRequestPage(self.version)

    def urlChanged(self, url):
        """
        Try to fetch access token or error from the redirect url.
        """

        access_token = fetchTokenFromUrl(url)

        if access_token:

            self.access_token = access_token
            
            self.tokenAcquired.emit(self.access_token)

            return

        error, error_description = fetchErrorFromUrl(url)

        if error:

            self.error, self.error_description = \
                error, error_description

            self.tokenUpdateError.emit(self.error, 
                                       self.error_description)

    def loadUrl(self, url):
        """
        Load the given url in the web view.
        """

        self.webView.load(QUrl(url))

    def loadAccessTokenRequestPage(self, version):
        """
        Load the access token request page.
        """

        version = 'v' + version

        url = consts.FB_OAUTH_URL.format(version=version)

        permissions = consts.FB_PERMISSIONS
        
        query_items = {
                'client_id': consts.FB_CLIENT_ID,
                'display': 'popup',
                'response_type': 'token',
                'redirect_uri': consts.FB_OAUTH_REDIRECT_URL,
                'scope': ','.join(permissions)
            }
        
        query = '&'.join([
                '='.join((k, v)) for k, v 
                                 in query_items.items()
            ])

        self.loadUrl('{}?{}'.format(url, query))    

