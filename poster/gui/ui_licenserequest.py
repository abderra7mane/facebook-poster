# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'poster/rc/ui/licenserequest.ui'
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

class Ui_LicenseRequestDialog(object):
    def setupUi(self, LicenseRequestDialog):
        LicenseRequestDialog.setObjectName(_fromUtf8("LicenseRequestDialog"))
        LicenseRequestDialog.resize(388, 345)
        self.verticalLayout = QtGui.QVBoxLayout(LicenseRequestDialog)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelMessage = QtGui.QLabel(LicenseRequestDialog)
        self.labelMessage.setWordWrap(True)
        self.labelMessage.setObjectName(_fromUtf8("labelMessage"))
        self.verticalLayout.addWidget(self.labelMessage)
        self.groupBox = QtGui.QGroupBox(LicenseRequestDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.textFirstName = QtGui.QLineEdit(self.groupBox)
        self.textFirstName.setMinimumSize(QtCore.QSize(250, 0))
        self.textFirstName.setObjectName(_fromUtf8("textFirstName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.textFirstName)
        self.labelLastName = QtGui.QLabel(self.groupBox)
        self.labelLastName.setObjectName(_fromUtf8("labelLastName"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelLastName)
        self.textLastName = QtGui.QLineEdit(self.groupBox)
        self.textLastName.setMinimumSize(QtCore.QSize(250, 0))
        self.textLastName.setObjectName(_fromUtf8("textLastName"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.textLastName)
        self.labelEmail = QtGui.QLabel(self.groupBox)
        self.labelEmail.setObjectName(_fromUtf8("labelEmail"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelEmail)
        self.textEmail = QtGui.QLineEdit(self.groupBox)
        self.textEmail.setMinimumSize(QtCore.QSize(250, 0))
        self.textEmail.setObjectName(_fromUtf8("textEmail"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.textEmail)
        self.labelFirstName = QtGui.QLabel(self.groupBox)
        self.labelFirstName.setObjectName(_fromUtf8("labelFirstName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelFirstName)
        self.verticalLayout.addWidget(self.groupBox)
        self.textRequest = QtGui.QTextEdit(LicenseRequestDialog)
        self.textRequest.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textRequest.setTabChangesFocus(True)
        self.textRequest.setReadOnly(True)
        self.textRequest.setAcceptRichText(False)
        self.textRequest.setObjectName(_fromUtf8("textRequest"))
        self.verticalLayout.addWidget(self.textRequest)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonGenerate = QtGui.QPushButton(LicenseRequestDialog)
        self.buttonGenerate.setDefault(True)
        self.buttonGenerate.setObjectName(_fromUtf8("buttonGenerate"))
        self.horizontalLayout.addWidget(self.buttonGenerate)
        self.buttonCopy = QtGui.QPushButton(LicenseRequestDialog)
        self.buttonCopy.setObjectName(_fromUtf8("buttonCopy"))
        self.horizontalLayout.addWidget(self.buttonCopy)
        self.buttonClose = QtGui.QPushButton(LicenseRequestDialog)
        self.buttonClose.setObjectName(_fromUtf8("buttonClose"))
        self.horizontalLayout.addWidget(self.buttonClose)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelLastName.setBuddy(self.textLastName)
        self.labelEmail.setBuddy(self.textEmail)
        self.labelFirstName.setBuddy(self.textFirstName)

        self.retranslateUi(LicenseRequestDialog)
        QtCore.QObject.connect(self.buttonClose, QtCore.SIGNAL(_fromUtf8("clicked()")), LicenseRequestDialog.reject)
        QtCore.QObject.connect(self.buttonGenerate, QtCore.SIGNAL(_fromUtf8("clicked()")), LicenseRequestDialog.generateRequest)
        QtCore.QObject.connect(self.buttonCopy, QtCore.SIGNAL(_fromUtf8("clicked()")), LicenseRequestDialog.copyRequest)
        QtCore.QMetaObject.connectSlotsByName(LicenseRequestDialog)
        LicenseRequestDialog.setTabOrder(self.textFirstName, self.textLastName)
        LicenseRequestDialog.setTabOrder(self.textLastName, self.textEmail)
        LicenseRequestDialog.setTabOrder(self.textEmail, self.textRequest)
        LicenseRequestDialog.setTabOrder(self.textRequest, self.buttonGenerate)
        LicenseRequestDialog.setTabOrder(self.buttonGenerate, self.buttonCopy)
        LicenseRequestDialog.setTabOrder(self.buttonCopy, self.buttonClose)

    def retranslateUi(self, LicenseRequestDialog):
        LicenseRequestDialog.setWindowTitle(_translate("LicenseRequestDialog", "Dialog", None))
        self.labelMessage.setText(_translate("LicenseRequestDialog", "<html><head/><body><p>In order to register your copy of this product :</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enter your registration details here</li><li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Click the button below to generate a license request</li><li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Include this request in your contact message with us</li></ul></body></html>", None))
        self.labelLastName.setText(_translate("LicenseRequestDialog", "&Last Name", None))
        self.labelEmail.setText(_translate("LicenseRequestDialog", "&Email", None))
        self.labelFirstName.setText(_translate("LicenseRequestDialog", "&First Name", None))
        self.buttonGenerate.setText(_translate("LicenseRequestDialog", "Generate", None))
        self.buttonCopy.setText(_translate("LicenseRequestDialog", "Copy", None))
        self.buttonClose.setText(_translate("LicenseRequestDialog", "Close", None))

