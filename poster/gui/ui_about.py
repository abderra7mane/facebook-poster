# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'poster/rc/ui/about.ui'
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

class Ui_AboutUi(object):
    def setupUi(self, AboutUi):
        AboutUi.setObjectName(_fromUtf8("AboutUi"))
        AboutUi.resize(414, 148)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutUi.sizePolicy().hasHeightForWidth())
        AboutUi.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(AboutUi)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.appLogoLabel = QtGui.QLabel(AboutUi)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appLogoLabel.sizePolicy().hasHeightForWidth())
        self.appLogoLabel.setSizePolicy(sizePolicy)
        self.appLogoLabel.setMinimumSize(QtCore.QSize(130, 130))
        self.appLogoLabel.setMaximumSize(QtCore.QSize(130, 130))
        self.appLogoLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.appLogoLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.appLogoLabel.setText(_fromUtf8(""))
        self.appLogoLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/img/icon.png")))
        self.appLogoLabel.setScaledContents(True)
        self.appLogoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.appLogoLabel.setObjectName(_fromUtf8("appLogoLabel"))
        self.horizontalLayout.addWidget(self.appLogoLabel)
        self.appDescriptionLabel = QtGui.QLabel(AboutUi)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appDescriptionLabel.sizePolicy().hasHeightForWidth())
        self.appDescriptionLabel.setSizePolicy(sizePolicy)
        self.appDescriptionLabel.setMinimumSize(QtCore.QSize(260, 130))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        self.appDescriptionLabel.setFont(font)
        self.appDescriptionLabel.setText(_fromUtf8(""))
        self.appDescriptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.appDescriptionLabel.setObjectName(_fromUtf8("appDescriptionLabel"))
        self.horizontalLayout.addWidget(self.appDescriptionLabel)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)

        self.retranslateUi(AboutUi)
        QtCore.QMetaObject.connectSlotsByName(AboutUi)

    def retranslateUi(self, AboutUi):
        AboutUi.setWindowTitle(_translate("AboutUi", "Dialog", None))

import resources_rc
