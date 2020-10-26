# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'poster/rc/ui/busydialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_BusyDialog(object):
    def setupUi(self, BusyDialog):
        BusyDialog.setObjectName(_fromUtf8("BusyDialog"))
        BusyDialog.resize(312, 144)
        BusyDialog.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        BusyDialog.setStyleSheet(_fromUtf8("QWidget {\n"
"    background-color: #DADADA;\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(BusyDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.busyMessage = QtGui.QLabel(BusyDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("OCR-A"))
        font.setPointSize(14)
        self.busyMessage.setFont(font)
        self.busyMessage.setText(_fromUtf8(""))
        self.busyMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.busyMessage.setObjectName(_fromUtf8("busyMessage"))
        self.verticalLayout.addWidget(self.busyMessage)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.busyIcon = QtGui.QLabel(BusyDialog)
        self.busyIcon.setMinimumSize(QtCore.QSize(200, 80))
        self.busyIcon.setMaximumSize(QtCore.QSize(200, 80))
        self.busyIcon.setText(_fromUtf8(""))
        self.busyIcon.setScaledContents(True)
        self.busyIcon.setObjectName(_fromUtf8("busyIcon"))
        self.horizontalLayout.addWidget(self.busyIcon)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(BusyDialog)
        QtCore.QMetaObject.connectSlotsByName(BusyDialog)

    def retranslateUi(self, BusyDialog):
        BusyDialog.setWindowTitle(_translate("BusyDialog", "Dialog", None))

