#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .ui_poster import Ui_PosterUi
from .ui_about import Ui_AboutUi
from .loginui import LoginUi
from .postdataui import PostDataUi
from .busydialog import BusyDialog
from .settingsdialog import SettingsDialog
from .tokenupdater import TokenUpdater
from ..facebook.datamanager import DataManager
from ..facebook.post import Post
from ..licensing.licenser import Licenser
from ..common import consts
from ..common.utils import colorizeHtmlText
from ..logging import logger


class PosterUi(QMainWindow):
    """
    The main interface for the application.
    """

    MAX_POST_TABS = 8

    TIMER_INTERVAL = 10

    TASK_NOT_STARTED = 0
    TASK_RUNNING = 1
    TASK_PAUSED = 2
    TASK_FINISHED = 3

    internalStateChanged = pyqtSignal()


    def __init__(self, isTrial=False, parent=None):
        super(PosterUi, self).__init__(parent)

        self.ui = Ui_PosterUi()
        self.ui.setupUi(self)

        self.datamanager = DataManager(self)

        self.logger = logger.getLogger()
        self.logger.registerHandler(self.logText)

        self.isTrial = isTrial

        self.loadAppSettings()

        self.setupTabCornerWidget()

        self.addPostTab()

        self.setupSystemTrayIcon()
        
        self.loadUiSettings()

        self.setWindowTitle(consts.__appname__)

        self.internalStateChanged.connect(self.updateUi)

        self.resetInternalState()

        self.disableTrialFeatures()

        QTimer.singleShot(0, self.loadData)

    def disableTrialFeatures(self):

        if self.isTrial:
            self.setWindowTitle("%s - (Trial Version)" % self.windowTitle())
            
            self.ui.addPostButton.setEnabled(False)
            self.ui.removePostButton.setEnabled(False)

            self.ui.savePostButton.setEnabled(False)
            self.ui.loadPostButton.setEnabled(False)

            self.ui.minDelaySpinBox.setEnabled(False)
            self.ui.maxDelaySpinBox.setEnabled(False)
            self.ui.sleepTimeSpinBox.setEnabled(False)
            self.ui.sleepAfterSpinBox.setEnabled(False)

            self.ui.settingsButton.setVisible(False)

            self.ui.postToWallCheckBox.setEnabled(False)
            self.ui.stopOnErrorsCheckBox.setEnabled(False)

    def setupTabCornerWidget(self):

        self.logger.debug("setting up tab corner widget...")

        self.savePostButton = QPushButton("Save")
        self.savePostButton.setIcon(QIcon(':/img/test.png'))

        self.savePostButton.setMinimumHeight(22)

        self.savePostButton.clicked.connect(self.saveCurrentPost)

        self.ui.postTabWidget.setCornerWidget(self.savePostButton)

    def saveCurrentPost(self):

        self.logger.debug("saving current post...")

        tab = self.ui.postTabWidget.currentWidget()

        if not tab.savePost():

            QMessageBox.warning(self, 
                "Post Not Saved",
                tab.errorString)

            self.logger.error("post not saved : %s" % tab.errorString)

        else:

            self.logger.info("post saved")

    def addPostTab(self, post=None):

        self.logger.debug("adding post tab...")

        if self.ui.postTabWidget.count() >= self.MAX_POST_TABS:
            
            self.logger.debug("maximum post count reached")

            QMessageBox.information(self, 
                "Add Post", 
                "The maximum number of posts has been reached.")

            return

        if not hasattr(self, 'lastTabIndex'):

            self.lastTabIndex = 0

        self.lastTabIndex += 1

        tab = PostDataUi(post, self.showAll, self.showLikes, self.isTrial, self)

        index = self.ui.postTabWidget.addTab(
                    tab, "Post %d" % self.lastTabIndex)

        if self.datamanager.currentProfile:

            self.logger.debug("populating user data...")
            
            user_groups = self.datamanager.getCurrentUserGroups()

            tab.updateUserGroups(user_groups)

            user_pages = self.datamanager.getCurrentUserPages()

            tab.updateUserPages(user_pages)

            user_likes = self.datamanager.getCurrentUserLikes()

            tab.updateUserLikes(user_likes)

        self.ui.postTabWidget.setCurrentIndex(index)

    def removePostTab(self):

        self.logger.debug("removing post tab...")

        if self.ui.postTabWidget.count() <= 1:
            self.logger.debug("minimum post count reached")
            return

        index = self.ui.postTabWidget.currentIndex()
        widget = self.ui.postTabWidget.widget(index)

        self.ui.postTabWidget.removeTab(index)
        widget.deleteLater()

    def savePostToFile(self):

        self.logger.debug("save post")

        if hasattr(self, 'saveDirPath'):
            
            savePath = self.saveDirPath

        else:
            savePath = QDir.currentPath()

        fileName = QFileDialog.getSaveFileName(self, "Save Post", savePath)

        if not fileName or fileName.isEmpty():

            return

        tab = self.ui.postTabWidget.currentWidget()

        post = tab.getPost()
            
        if self._savePostToFile(post, fileName):

            self.logger.info("post saved")

            self.saveDirPath = unicode(QFileInfo(fileName).canonicalPath())

        else:

            self.logger.error("post no saved")

            self.saveDirPath = unicode(QFileInfo(fileName).absolutePath())

            QMessageBox.critical(self, 
                "Saving Error", 
                QString("Failed to save data to file.\n\n"
                        "Error details: %1").arg(self.errorString))

    def _savePostToFile(self, post, fileName):

        self.logger.debug("saving post to file...")

        _file = QFile(fileName)
        
        if _file.open(QFile.WriteOnly):
            
            stream = QTextStream(_file)
            stream.setCodec('utf-8')

            stream << QString("type=%1\r\n").arg(post.type)
            stream << QString("message=%1\r\n").arg(post.data['message'])
            stream << QString("name=%1\r\n").arg(post.data['name'])
            stream << QString("link=%1\r\n").arg(post.data['link'])
            stream << QString("image=%1\r\n").arg(post.data['image'])

            _file.close()

            self.logger.debug("post saved to file")

            return True

        else:

            self.logger.debug("failed to save post")

            self.errorString = unicode(_file.errorString())

            return False

    def loadPostFromFile(self):

        self.logger.debug("load post")

        if hasattr(self, 'openDirPath'):

            openPath = self.openDirPath

        else:
            openPath = QDir.currentPath()

        fileName = QFileDialog.getOpenFileName(self, "Load Post", openPath)

        if not fileName or fileName.isEmpty():

            return

        post = self._loadPostFromFile(fileName)

        if post:

            self.logger.info("post loaded")

            self.addPostTab(post)

        else:

            self.logger.error("failed to load post")

            QMessageBox.critical(self, 
                "Loading Error", 
                QString("Failed to load data from file.\n\n"
                        "Error details: %1").arg(self.errorString))

        self.openDirPath = unicode(QFileInfo(fileName).canonicalPath())

    def _loadPostFromFile(self, fileName):

        self.logger.debug("loading post from file...")

        _file = QFile(fileName)

        post_type = None
        post_data = dict(message='', link='', 
                         image='', name='')
        post = None

        valid_types = ['text', 'link', 'image']

        if _file.open(QFile.ReadOnly):

            stream = QTextStream(_file)
            stream.setCodec('utf-8')

            while not stream.atEnd():

                line = unicode(stream.readLine())

                if line.startswith('#'):

                    self.logger.debug("ignoring line : " + line)

                    continue

                try:
                    key, value = line.split('=')
                
                except ValueError:

                    self.logger.debug("line does not match 'key=value' : " + line)
                    
                    continue

                if key == 'type' and value in valid_types:
                    
                    post_type = value

                elif key in post_data.keys():
                    
                    post_data[key] = value

                else:
                    self.logger.debug("error parsing line : " + line)

                    self.errorString = "Invalid file"

                    return False

            if post_type:

                self.logger.debug("post loaded")

                return Post(post_type, post_data)

            else:

                self.logger.debug("post loading failed : invalid file.")

                self.errorString = "Invalid file"

                return False

        else:

            self.logger.debug("failed to load post from file")

            self.errorString = unicode(_file.errorString())

            return False

    def setupSystemTrayIcon(self):

        self.logger.debug("setting up system tray icon...")

        if QSystemTrayIcon.isSystemTrayAvailable():

            self.logger.debug("system tray available")

            trayIconMenu = self.createSystemTrayIconMenu()

            self.trayIcon = QSystemTrayIcon(self)
            self.trayIcon.setIcon(QApplication.instance().windowIcon())
            self.trayIcon.setContextMenu(trayIconMenu)
            self.trayIcon.setToolTip(consts.__appname__)

            self.trayIcon.activated.connect(self.trayIconActivated)

            self.trayIcon.show()

        else:

            self.logger.debug("system tray not available")

    def createSystemTrayIconMenu(self):

        self.logger.debug("creating system tray icon menu...")

        self.trayShowAction = QAction("&Restore Window", self)
        self.trayHideAction = QAction("&Hide Window", self)
        self.trayQuitAction = QAction("&Quit", self)

        self.trayIconMenu = QMenu(self)

        self.trayIconMenu.addAction(self.trayShowAction)
        self.trayIconMenu.addAction(self.trayHideAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.trayQuitAction)

        self.connect(self.trayShowAction, 
                     SIGNAL('triggered()'), self.show)
        
        self.connect(self.trayHideAction, 
                     SIGNAL('triggered()'), self.hide)
        
        self.connect(self.trayQuitAction, 
                     SIGNAL('triggered()'), self.close)

        return self.trayIconMenu

    def trayIconActivated(self, reason):

        self.logger.debug("tray icon activated")

        if reason == QSystemTrayIcon.Trigger:
            
            if self.isVisible():

                self.hide()
            
            else:
                self.show()
                self.activateWindow()

    def hasSystemTrayIcon(self):

        return hasattr(self, 'trayIcon') and self.trayIcon

    def login(self):

        self.logger.info("logging in...")

        self.loginDialog = LoginUi(self.datamanager.profiles, 
                                   self.appID,
                                   self.apiDefaultVersion,
                                   parent=self)

        self.loginDialog.connectionStatusChanged.connect(
            self.connectionStatusChanged)
        
        self.loginDialog.accessTokenAcquired.connect(
            self.startProfileFetcher)
        
        self.loginDialog.accessTokenAcquired.connect(
            self.accessTokenAcquired)

        self.loginDialog.accessTokenAcquired.connect(
            self.loginDialog.accept)
        
        self.loginDialog.loginError.connect(
            self.loginDialog.reject)

        self.loginDialog.finished.connect(
            self.loginDialog.deleteLater)

        self.loginDialog.reload()
        self.loginDialog.exec_()

    def connectionStatusChanged(self, connected):

        if connected:

            self.saveUserCookies()

            self.logger.info("user connected")

        else:

            self.clearUserData()

            self.logger.info("user disconnected")

        self.setConnected(connected)

    def saveUserCookies(self):

        self.logger.debug("saving user cookies...")

        cookies = self.loginDialog.getCookies()

        self.datamanager.setTmpProfileCookies(cookies)
        
    def accessTokenAcquired(self):

        self.logger.debug("access token acquired")
        
        self.datamanager.tokenExpired.connect(
            self.updateAccessToken)
        
    def updateAccessToken(self):

        self.logger.debug("updating access token...")
        
        self.showBusyDialog('updating token...')

        cookies = self.datamanager.getCurrentUserCookies()

        self.tokenUpdater = TokenUpdater(cookies)

        self.tokenUpdater.tokenAcquired.connect(self.tokenUpdated)

        self.tokenUpdater.tokenUpdateError.connect(self.tokenUpdateFailed)

        self.tokenUpdater.start()

    def tokenUpdated(self, token):

        self.logger.debug("token updated successfully")

        self.hideBusyDialog()

        self.datamanager.updateToken(unicode(token))

    def tokenUpdateFailed(self):

        self.logger.debug("token update failed")

        self.hideBusyDialog()

        self.datamanager.tokenUpdateFailed()

        QMessageBox.critical(self, 
            "Error", 
            "Expired token update failed.\n\n"
            "Error details:\n"
            "An error was encountered while trying to "
            "update the expired access token.\n"
            "The pending operation cannot continue "
            "without this token.")

    def startProfileFetcher(self, access_token):

        self.logger.debug("starting profile fetcher...")

        self.showBusyDialog('fetching user information...')

        self.datamanager.taskStarted.connect(
            self.profileFetcherStarted)

        self.datamanager.taskReadyRead.connect(
            self.readUserData)
        
        self.datamanager.taskError.connect(
            self.profileFetcherError)
        
        self.datamanager.taskFinished.connect(
            self.profileFetcherFinished)

        self.datamanager.fetchUserProfile(unicode(access_token))

    def profileFetcherStarted(self):

        self.logger.info("start fetching user information...")

        self.setFetcherTaskState(self.TASK_RUNNING)

    def readUserData(self, type):

        self.logger.debug("reading user data : {0}", type)

        if type == 'user_info':

            self.updateUserInfo()

        elif type == 'user_picture':

            self.updateUserPicture()

        elif type == 'user_groups':

            self.updateUserGroups()

        elif type == 'user_pages':

            self.updateUserPages()

        elif type == 'user_likes':

            self.updateUserLikes()

    def profileFetcherError(self, errorString):

        self.logger.debug(
            "profile fetcher error : {0}", errorString)

        self.hideBusyDialog()

        QMessageBox.critical(self, 
            "Error", 
            "An error was encountered while trying to "
            "fetch user information.\n\n"
            "Error Details:\n%s" % errorString)

    def clearUserData(self):

        self.logger.debug("clear user data...")

        self.ui.userIdLabel.clear()
        self.ui.userNameLabel.clear()
        
        self.ui.profilePictureLabel.setPixmap(
            QPixmap(':/img/default-profile.png'))

        for index in range(self.ui.postTabWidget.count()):

            tab = self.ui.postTabWidget.widget(index)

            tab.clearUserData()

        self.ui.posterTimerLabel.setText("00:00:00:000")
        self.ui.posterProgressBar.setValue(0)

    def profileFetcherFinished(self, ok):

        self.logger.debug("profile fetcher finished : {0}", ok)

        self.setBusyMessage('terminated')

        if ok:
            self.setFetcherTaskState(self.TASK_FINISHED)

            self.logger.info("fetching user information succeeded")

        else:
            self.resetInternalState()

            self.logger.info("fetching user information failed")

        self.datamanager.taskStarted.disconnect(
            self.profileFetcherStarted)

        self.datamanager.taskReadyRead.disconnect(
            self.readUserData)
        
        self.datamanager.taskError.disconnect(
            self.profileFetcherError)
        
        self.datamanager.taskFinished.disconnect(
            self.profileFetcherFinished)

        self.hideBusyDialog()

    def logout(self):

        self.logger.info("logging out...")

        self.connectionStatusChanged(False)

        self.datamanager.currentUserDisconnected()

    def startPosterTask(self):

        self.logger.debug("starting poster task...")

        tasks = self.collectTasks()

        if not tasks:

            QMessageBox.warning(self, 
                "No Post", 
                "No post has been saved yet.\n\n"
                "Please save at least one post before continuing.")

            self.logger.debug("no post saved, aborting")

            return

        config = self.collectPosterConfiguration()

        if config['minDelay'] > config['maxDelay']:

            QMessageBox.warning(self, 
                "Invalid configuration",
                "Minimum delay cannot be greater than maximum delay.")

            self.logger.debug("invalid configuration, aborting")

            return

        self.datamanager.taskStarted.connect(self.posterTaskStarted)
        self.datamanager.taskFinished.connect(self.posterTaskFinished)
        self.datamanager.taskPaused.connect(self.posterTaskPaused)
        self.datamanager.taskResumed.connect(self.posterTaskResumed)
        self.datamanager.taskError.connect(self.posterTaskError)
        self.datamanager.taskProgress.connect(self.posterTaskProgress)

        self.posterTimer = QElapsedTimer()
        
        self.posterElapsedTime = 0

        self.timerId = 0

        self.posterTaskProgress(0)

        self.datamanager.schedulePoster(tasks, config)

        self.logger.debug("scheduling poster tasks...")

    def collectTasks(self):

        self.logger.debug("collecting saved tasks...")

        tasks = dict()

        tabCount = self.ui.postTabWidget.count()

        for index in range(tabCount):

            tab = self.ui.postTabWidget.widget(index)

            task = tab.getPosterTask()

            if task:
                
                task.setId(self.getNextTaskId())

                if self.ui.postToWallCheckBox.isChecked():

                    task.addTargets({
                        'me' : { 'type' : 'user' }
                    })

                tasks[task.id] = task

        self.logger.debug("%d tasks collected" % len(tasks))

        self.logger.debug("%d posts in total" % 
            sum(tasks[task].totalPosts for task in tasks))
        
        return tasks

    def collectPosterConfiguration(self):

        return {
            'minDelay' : self.ui.minDelaySpinBox.value(),
            'maxDelay' : self.ui.maxDelaySpinBox.value(),
            'sleepTime' : self.ui.sleepTimeSpinBox.value(),
            'sleepAfter' : self.ui.sleepAfterSpinBox.value(),
            'stopOnErrors' : self.ui.stopOnErrorsCheckBox.isChecked(),
        }

        self.logger.debug("loading user configuration...")

    def getNextTaskId(self):

        self.logger.debug("generating new task id...")

        if not hasattr(self, 'lastTaskId'):
            
            self.lastTaskId = 0

        self.lastTaskId += 1

        return self.lastTaskId

    def posterTaskStarted(self):

        self.logger.info("poster schedule started")

        self.posterTimer.restart()

        self.timerId = self.startTimer(self.TIMER_INTERVAL)

        self.setPosterTaskState(self.TASK_RUNNING)

    def posterTaskFinished(self, ok):

        self.logger.info("poster schedule terminated %s" % 
            ["with error", "successfully"][ok])

        self.posterTaskProgress(100)

        self.updatePosterTimer()

        self.killTimer(self.timerId)
        self.timerId = 0

        self.setPosterTaskState(self.TASK_FINISHED)

        self.datamanager.taskStarted.disconnect(
            self.posterTaskStarted)
        
        self.datamanager.taskFinished.disconnect(
            self.posterTaskFinished)
        
        self.datamanager.taskPaused.disconnect(
            self.posterTaskPaused)
        
        self.datamanager.taskResumed.disconnect(
            self.posterTaskResumed)
        
        self.datamanager.taskError.disconnect(
            self.posterTaskError)
        
        self.datamanager.taskProgress.disconnect(
            self.posterTaskProgress)

    def posterTaskPaused(self):

        self.logger.info("poster schedule paused")

        self.updatePosterTimer()

        self.killTimer(self.timerId)
        self.timerId = 0

        self.setPosterTaskState(self.TASK_PAUSED)

    def posterTaskResumed(self):

        self.logger.info("poster schedule resumed")

        self.posterTimer.restart()

        self.timerId = self.startTimer(self.TIMER_INTERVAL)

        self.setPosterTaskState(self.TASK_RUNNING)

    def posterTaskError(self, errorString):

        self.logger.info("poster schedule failed : {0}", errorString)

        if self.ui.stopOnErrorsCheckBox.isChecked():

            QMessageBox.critical(self, 
                "Error", 
                "An error was encountered while trying to "
                "publish post.\n\n"
                "Error Details:\n%s" % errorString)

    def posterTaskProgress(self, progress):

        self.logger.info("poster schedule progress {0}%", progress)

        self.ui.posterProgressBar.setValue(progress)

    def pausePosterTask(self):

        self.logger.debug("pausing poster task...")

        self.datamanager.pausePoster()

    def resumePosterTask(self):

        self.logger.debug("resuming poster task...")

        self.datamanager.resumePoster()

    def stopPosterTask(self):

        self.logger.debug("stopping poster task...")

        self.datamanager.stopPoster()

    def updateUserInfo(self):

        self.logger.debug("updating user info...")

        user_info = self.datamanager.readFetchedData('user_info')

        self.ui.userIdLabel.setText(user_info['id'])
        self.ui.userNameLabel.setText(user_info['name'])

        self.logger.debug("user details updated")

    def updateUserPicture(self):

        self.logger.debug("updating user picture...")

        user_picture = self.datamanager.readFetchedData('user_picture')

        picture_data = user_picture['data']

        pixmap = QPixmap()

        if pixmap.loadFromData(QByteArray(picture_data)):

            label = self.ui.profilePictureLabel

            size = label.size()

            label.setPixmap(pixmap.scaled(size))

        self.logger.debug("user profile picture updated")

    def updateUserGroups(self):

        self.logger.debug("updating user groups...")

        user_groups = self.datamanager.readFetchedData('user_groups')

        for index in range(self.ui.postTabWidget.count()):

            tab = self.ui.postTabWidget.widget(index)

            tab.updateUserGroups(user_groups)

        self.logger.debug("user groups list updated")

    def updateUserPages(self):

        self.logger.debug("updaing user pages...")

        user_pages = self.datamanager.readFetchedData('user_pages')

        for index in range(self.ui.postTabWidget.count()):

            tab = self.ui.postTabWidget.widget(index)

            tab.updateUserPages(user_pages)

        self.logger.debug("user pages list updated")

    def updateUserLikes(self):

        self.logger.debug("updating user likes...")

        user_likes = self.datamanager.readFetchedData('user_likes')

        for index in range(self.ui.postTabWidget.count()):

            tab = self.ui.postTabWidget.widget(index)

            tab.updateUserLikes(user_likes)

        self.logger.debug("user liked pages updated")

    def updatePosterTimer(self):

        self.logger.debug("updating poster timer...")

        if self.timerId:

            elapsed = self.posterTimer.restart()
            
            self.posterElapsedTime += elapsed

            h = (self.posterElapsedTime / 1000 / 60 / 60)
            m = (self.posterElapsedTime / 1000 / 60) % 60
            s = (self.posterElapsedTime / 1000) % 60
            ms = (self.posterElapsedTime % 1000)
            
            _t = "%02d:%02d:%02d:%03d" % (h, m, s, ms)

            self.ui.posterTimerLabel.setText(_t)

    def timerEvent(self, event):

        self.logger.debug("timer event")

        self.updatePosterTimer()

    def showEvent(self, event):

        self.logger.debug("showing main window...")

        if self.hasSystemTrayIcon():

            self.trayShowAction.setVisible(False)
            
            self.trayHideAction.setVisible(True)

        if self.fetcherTaskState == self.TASK_RUNNING:

            self.showBusyDialog()

        super(PosterUi, self).showEvent(event)

    def hideEvent(self, event):

        self.logger.debug("hiding main window...")

        if self.hasSystemTrayIcon():

            self.trayShowAction.setVisible(True)

            self.trayHideAction.setVisible(False)

        self.hideBusyDialog()
        
        super(PosterUi, self).hideEvent(event)

    def closeEvent(self, event):

        if self.okToClose():

            self.logger.debug("ok to close, closing...")

            self.saveUiSettings()

            self.saveData()

            event.accept()

        else:

            self.logger.debug("pending operations, waiting...")

            msgBox = QMessageBox(self)

            msgBox.setWindowTitle("Pending Operation")
            
            msgBox.setIcon(QMessageBox.Warning)
            
            msgBox.setText(
                "An internal operation is still ongoing.\n"
                "Please wait until it finished then try again.")

            okButton = msgBox.addButton(
                "Ok", QMessageBox.AcceptRole)

            if self.hasSystemTrayIcon():

                minimizeButton = msgBox.addButton(
                    "Minimize to tray", 
                    QMessageBox.ActionRole)
            
            discardButton = msgBox.addButton(
                "Close anyway", QMessageBox.DestructiveRole)

            msgBox.setDefaultButton(okButton)

            msgBox.exec_()

            if self.hasSystemTrayIcon() and \
                    msgBox.clickedButton() == minimizeButton:

                self.logger.debug("minimizing window to tray...")

                event.ignore()

                self.hide()

            elif msgBox.clickedButton() == okButton:

                self.logger.debug("not closing")

                event.ignore()

            else:

                self.logger.debug("closing anyway")

                self.stopPendingOperations()

                self.saveUiSettings()

                self.saveData()

                event.accept()

    def okToClose(self):

        if self.fetcherTaskState in [self.TASK_RUNNING]:

            return False

        elif self.posterTaskState in \
                [self.TASK_RUNNING, self.TASK_PAUSED]:

            return False

        return True

    def stopPendingOperations(self):

        self.logger.debug("stopping pending operations...")

        if self.posterTaskState in \
                [self.TASK_RUNNING, self.TASK_PAUSED]:

            self.stopPosterTask()

    def saveUiSettings(self):

        self.logger.info("saving application settings...")

        settings = QSettings()

        settings.beginGroup('ui')

        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('state', self.saveState())
        settings.setValue('saveDirPath', self.saveDirPath)
        settings.setValue('openDirPath', self.openDirPath)

        settings.endGroup()

    def loadUiSettings(self):

        self.logger.info("loading application ui settings...")

        settings = QSettings()

        settings.beginGroup('ui')

        self.restoreGeometry(
            settings.value('geometry').toByteArray())
        self.restoreState(
            settings.value('state').toByteArray())
        self.saveDirPath = unicode(
            settings.value('saveDirPath').toString())
        self.openDirPath = unicode(
            settings.value('openDirPath').toString())

        settings.endGroup()

    def loadAppSettings(self):

        self.logger.info("loading application settings...")

        settings = QSettings()

        settings.beginGroup('app')

        self.showAll = settings.value('showAll', False).toBool()
        self.showLikes = settings.value('showLikes', False).toBool()
        self.apiDefaultVersion = unicode(
            settings.value('apiDefaultVersion', 
                consts.FB_GRAPH_DEFAULT_VERSION).toString())
        self.appID = unicode(
            settings.value('appID', consts.FB_CLIENT_ID).toString())

        settings.endGroup()

    def saveData(self):

        self.logger.info("saving data...")

        self.datamanager.saveProfiles()

    def loadData(self):

        self.logger.info("loading user data...")

        self.datamanager.loadSavedProfiles()

    def resetInternalState(self):

        self.logger.debug("resetting internal state...")

        self.connected = False

        self.fetcherTaskState = self.TASK_NOT_STARTED

        self.posterTaskState = self.TASK_NOT_STARTED

        self.clearUserData()

        self.internalStateChanged.emit()

        self.logger.debug("internal state reset")

    def setConnected(self, connected):

        self.logger.debug(
            "setting connection status to : {0}", 
            connected)

        if self.connected != connected:

            self.connected = connected

            self.internalStateChanged.emit()

    def setFetcherTaskState(self, state):

        self.logger.debug(
            "setting fetcher task status to : {0}", 
            state)

        if self.fetcherTaskState != state:

            self.fetcherTaskState = state

            self.internalStateChanged.emit()

    def setPosterTaskState(self, state):

        self.logger.debug(
            "setting poster task status to : {0}", 
            state)

        if self.posterTaskState != state:

            self.posterTaskState = state

            self.internalStateChanged.emit()

    def updateUi(self):

        self.logger.debug("updating ui...")

        colors = ['red', 'green']
        status = ['Disconnected', 'Connected']

        self.ui.connectionStatusLabel.setText(
            colorizeHtmlText(status[self.connected], 
                             colors[self.connected]))

        self.ui.loginButton.setVisible(not self.connected or 
            self.fetcherTaskState != self.TASK_FINISHED)
        self.ui.loginButton.setEnabled(not self.connected)

        self.ui.logoutButton.setVisible(self.connected and 
            self.fetcherTaskState == self.TASK_FINISHED)
        self.ui.logoutButton.setEnabled(self.connected and 
            self.fetcherTaskState == self.TASK_FINISHED)

        self.savePostButton.setEnabled(self.connected and 
            self.fetcherTaskState == self.TASK_FINISHED)

        # self.ui.addPostButton.setEnabled(self.connected and 
        #     self.fetcherTaskState == self.TASK_FINISHED)

        # self.ui.removePostButton.setEnabled(self.connected and 
        #     self.fetcherTaskState == self.TASK_FINISHED)

        self.ui.posterStartButton.setEnabled(self.connected and 
            self.fetcherTaskState == self.TASK_FINISHED and 
            (self.posterTaskState == self.TASK_NOT_STARTED or 
                self.posterTaskState == self.TASK_FINISHED))

        self.ui.posterPauseButton.setEnabled(self.connected and 
            self.fetcherTaskState == self.TASK_FINISHED and 
            self.posterTaskState == self.TASK_RUNNING)

        self.ui.posterResumeButton.setEnabled(self.connected and 
            self.fetcherTaskState == self.TASK_FINISHED and 
            self.posterTaskState == self.TASK_PAUSED)
        
        self.ui.posterCancelButton.setEnabled(self.connected and 
            self.fetcherTaskState == self.TASK_FINISHED and 
            (self.posterTaskState == self.TASK_RUNNING or 
                self.posterTaskState == self.TASK_PAUSED))

        self.logger.debug("ui updated")

    def settings(self):

        self.logger.debug("showing settings dialog...")

        dialog = SettingsDialog(self)

        if dialog.exec_() == QDialog.Accepted:

            self.loadAppSettings()

            QMessageBox.information(self, 
                "Settings", 
                "Restart the application for all changes to take effect.")

        self.logger.debug("settings dialog closed")

    def about(self):

        self.logger.debug("showing about dialog...")

        dialog = QDialog(self)

        ui_dialog = Ui_AboutUi()
        ui_dialog.setupUi(dialog)

        dialog.setWindowTitle("About Poster")

        ui_dialog.appDescriptionLabel.setText(
            consts.APP_ABOUT_TEMPLATE.format(
                appname=consts.__appname__, 
                version=consts.__version__,
                description=consts.__description__,
                copyright=consts.__copyright__,
                author=consts.__author__,
                contact=consts.__email__)
            )

        dialog.exec_()

        self.logger.debug("about dialog closed")

    def showBusyDialog(self, message=None):

        self.logger.debug("showing busy dialog...")

        if not hasattr(self, 'busyDialog'):

            if message is None:

                message = consts.DEFAULT_BUSY_MESSAGE

            self.busyDialog = BusyDialog(message, self)

        elif message is not None:

            self.setBusyMessage(message)

        self.busyDialog.show()

        self.logger.debug("busy dialog shown")

    def hideBusyDialog(self):

        self.logger.debug("hiding busy dialog...")

        if hasattr(self, 'busyDialog'):

            self.busyDialog.hide()

    def setBusyMessage(self, message):

        self.logger.debug("setting busy message...")

        if hasattr(self, 'busyDialog'):

            self.busyDialog.setMessage(message)

    def logText(self, text, args, kwargs):

        msg = unicode(text).format(*args, **kwargs)

        self.ui.appLogText.append(
            QString("[%1] %2").arg(
                QTime.currentTime().toString("HH:mm:ss:zzz")).arg(msg))
        
        scrollBar = self.ui.appLogText.verticalScrollBar()
        scrollBar.setValue(scrollBar.maximum())

