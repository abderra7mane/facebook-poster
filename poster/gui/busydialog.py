#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .ui_busydialog import Ui_BusyDialog


class BusyDialog(QDialog):
    """
    """

    def __init__(self, message, parent=None):
        super(BusyDialog, self).__init__(parent, Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.ui = Ui_BusyDialog()
        self.ui.setupUi(self)

        self.ui.busyMessage.setText(message)

        self.ui.busyIcon.setMovie(QMovie(":/img/loading.gif"))
        self.ui.busyIcon.movie().start()

        self.setWindowTitle("Operation in progress")

    def setMessage(self, message):

        self.ui.busyMessage.setText(message)

    def closeEvent(self, event):

        event.ignore()

    def keyPressEvent(self, event):

        if (event.key() == Qt.Key_Escape):
            event.ignore()
        else:
            super(BusyDialog, self).keyPressEvent(event)

    def mouseDoubleClickEvent(self, event):

        #### to be removed ####

        self.reject()

