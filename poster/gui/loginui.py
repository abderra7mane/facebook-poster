#!/usr/bin/env python
#-*- coding: utf-8 -*-

from urlparse import parse_qs
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from PyQt4.QtWebKit import *

from ..common.utils import fetchTokenFromUrl, fetchErrorFromUrl
from ..common import consts


class LoginUi(QDialog):
    """
    """

    connectionStatusChanged = pyqtSignal(bool)

    tokenAcquired = pyqtSignal('QString')

    accessTokenAcquired = pyqtSignal('QString')

    loginError = pyqtSignal('QString', 'QString')


    def __init__(self, profiles,
                       appID,  
                       version, 
                       parent=None):

        super(LoginUi, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.profiles = profiles

        self.appID = appID
        self.version = version

        self._noPendingOperation = True

        self.connected = False

        self.cookieJar = QNetworkCookieJar()

        self.nam = QNetworkAccessManager(self)
        self.nam.setCookieJar(self.cookieJar)

        self.profileHistoryLabel = QLabel("Recent")
        self.profileHistoryLabel.setFrameShadow(QFrame.Sunken)
        self.profileHistoryLabel.setFrameShape(QFrame.StyledPanel)

        self.profileHistoryListWidget = QListWidget()
        self.profileHistoryListWidget.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.profileHistoryListWidget.setSelectionMode(
            QAbstractItemView.SingleSelection)

        self.loadProfileButton = QPushButton("Load Profile")
        self.loadProfileButton.setIcon(QIcon(':/img/forward.png'))

        self.webView = QWebView()
        self.webView.page().setNetworkAccessManager(self.nam)

        self.reloadButton = QPushButton("Reload")
        self.reloadButton.setIcon(QIcon(':/img/reload.png'))

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setIcon(QIcon(':/img/cancel.png'))

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.profileHistoryLabel)
        leftLayout.addWidget(self.profileHistoryListWidget)
        leftLayout.addWidget(self.loadProfileButton)

        rightBottomLayout = QHBoxLayout()
        rightBottomLayout.addStretch()
        rightBottomLayout.addWidget(self.reloadButton)
        rightBottomLayout.addWidget(self.cancelButton)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.webView)
        rightLayout.addLayout(rightBottomLayout)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout, 1)
        mainLayout.addLayout(rightLayout, 3)

        self.setLayout(mainLayout)
        self.setWindowTitle("Facebook Login")

        self.webView.loadStarted.connect(self.loadStarted)
        self.webView.loadFinished.connect(self.loadFinished)
        self.webView.urlChanged.connect(self.urlChanged)

        self.profileHistoryListWidget.itemDoubleClicked.connect(
                                        self.loadSelectedProfile)
        
        self.reloadButton.clicked.connect(self.reload)
        self.cancelButton.clicked.connect(self.reject)
        self.loadProfileButton.clicked.connect(self.loadSelectedProfile)

        self.setFixedSize(680, 400)
        self.webView.setFocus()

        self.setupProfileHistory()

    def setupProfileHistory(self):
        """
        Setup the profile login history list.
        """

        for profile in self.profiles.values():
            
            user_name = profile.userName
            user_id = profile.userId

            # last_login = profile.lastConnected
            
            user_picture = profile.userPicture
            
            item = QListWidgetItem()

            item.setText(user_name)
            item.setData(Qt.UserRole, user_id)

            pixmap = QPixmap()
            
            if pixmap.loadFromData(user_picture):

                item.setIcon(QIcon(pixmap))

            self.profileHistoryListWidget.addItem(item)

    def accept(self):
        
        if self._noPendingOperation:
            QDialog.accept(self)
        
        else:
            self.webView.stop()
            self.accept()

    def reject(self):
        
        if self._noPendingOperation:
            QDialog.reject(self)

        else:
            self.webView.stop()
            self.reject()

    def loadStarted(self):
        
        self._noPendingOperation = False

    def loadFinished(self):
        
        self._noPendingOperation = True

        self.checkLoginStatus()

    def checkLoginStatus(self):
        """
        Check whether the user has successfully logged in.
        """

        self.setLoginStatus(self.isLoggedIn())

    def setLoginStatus(self, connected):
        """
        Change the local user login status.
        """
        
        if connected != self.connected:

            self.connected = connected

            self.connectionStatusChanged.emit(self.connected)

    def isLoggedIn(self):
        """
        Return the current user login status.
        """
        
        return (self.hasUserCookies() and \
                self.isCookiesSessionOpen())

    def hasUserCookies(self):
        """
        Check if the received cookies contains user cookies 
        which are sent when the user successfully login.
        """
        
        user_cookies = set(['c_user', 'datr', 'xs'])
        
        cookies_names = set(self.getCookiesNames())

        if user_cookies.issubset(cookies_names):
            
            return True

        return False

    def getCookiesNames(self):
        """
        Return the received cookies names.
        """
        
        qtCookies = self.getCookies()

        cookies = list()
        
        for cookie in qtCookies:

            c_name = QString(cookie.name())
            
            c_domain = cookie.domain()
            
            if c_domain.endsWith('.facebook.com'):
                
                cookies.append(unicode(c_name))
        
        return cookies

    def getCookies(self):
        """
        Return the received cookies.
        """

        return self.cookieJar.allCookies()

    def isCookiesSessionOpen(self):
        """
        Check whether cookies session is still open.
        """
        
        return True

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

    def reload(self):
        """
        Reload the login page.
        """
        if self._noPendingOperation:
            self.loadTransientAccessTokenRequestPage()

        else:
            self.webView.stop()
            self.reload()

    def loadSelectedProfile(self):

        selectedItems = self.profileHistoryListWidget.selectedItems()

        if not selectedItems:
            return

        selected = selectedItems[0]
        
        user_id = unicode(selected.data(Qt.UserRole).toString())

        profile = self.profiles[user_id]

        self.cookieJar.setAllCookies(profile.cookies)
        
        self.reload()

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
                'client_id': self.appID,
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

    def loadTransientAccessTokenRequestPage(self):

        self.tokenAcquired.connect(self.transientTokenAcquired)

        self.loadAccessTokenRequestPage(self.version)

    def transientTokenAcquired(self):

        self.tokenAcquired.disconnect(self.transientTokenAcquired)

        self.loadFinalAccessTokenRequestPage()

    def loadFinalAccessTokenRequestPage(self):

        self.tokenAcquired.connect(self.finalTokenAcquired)

        self.loadAccessTokenRequestPage('2.3')

    def finalTokenAcquired(self, token):

        self.tokenAcquired.disconnect(self.finalTokenAcquired)

        self.accessTokenAcquired.emit(token)
