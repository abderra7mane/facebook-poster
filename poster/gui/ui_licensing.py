# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'poster/rc/ui/licensing.ui'
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

class Ui_LicensingDialog(object):
    def setupUi(self, LicensingDialog):
        LicensingDialog.setObjectName(_fromUtf8("LicensingDialog"))
        LicensingDialog.resize(351, 299)
        LicensingDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(LicensingDialog)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelMessage = QtGui.QLabel(LicensingDialog)
        self.labelMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMessage.setWordWrap(True)
        self.labelMessage.setObjectName(_fromUtf8("labelMessage"))
        self.verticalLayout.addWidget(self.labelMessage)
        self.groupBox = QtGui.QGroupBox(LicensingDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelFirstName = QtGui.QLabel(self.groupBox)
        self.labelFirstName.setObjectName(_fromUtf8("labelFirstName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelFirstName)
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
        self.labelSerial = QtGui.QLabel(self.groupBox)
        self.labelSerial.setObjectName(_fromUtf8("labelSerial"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelSerial)
        self.textLicense = QtGui.QTextEdit(self.groupBox)
        self.textLicense.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textLicense.setTabChangesFocus(True)
        self.textLicense.setAcceptRichText(False)
        self.textLicense.setObjectName(_fromUtf8("textLicense"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.textLicense)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonLicensing = QtGui.QPushButton(LicensingDialog)
        self.buttonLicensing.setObjectName(_fromUtf8("buttonLicensing"))
        self.horizontalLayout.addWidget(self.buttonLicensing)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonOk = QtGui.QPushButton(LicensingDialog)
        self.buttonOk.setDefault(True)
        self.buttonOk.setObjectName(_fromUtf8("buttonOk"))
        self.horizontalLayout.addWidget(self.buttonOk)
        self.buttonCancel = QtGui.QPushButton(LicensingDialog)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelFirstName.setBuddy(self.textFirstName)
        self.labelLastName.setBuddy(self.textLastName)
        self.labelEmail.setBuddy(self.textEmail)
        self.labelSerial.setBuddy(self.textLicense)

        self.retranslateUi(LicensingDialog)
        QtCore.QObject.connect(self.buttonOk, QtCore.SIGNAL(_fromUtf8("clicked()")), LicensingDialog.accept)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), LicensingDialog.reject)
        QtCore.QObject.connect(self.buttonLicensing, QtCore.SIGNAL(_fromUtf8("clicked()")), LicensingDialog.howToLicense)
        QtCore.QMetaObject.connectSlotsByName(LicensingDialog)
        LicensingDialog.setTabOrder(self.textFirstName, self.textLastName)
        LicensingDialog.setTabOrder(self.textLastName, self.textEmail)
        LicensingDialog.setTabOrder(self.textEmail, self.textLicense)
        LicensingDialog.setTabOrder(self.textLicense, self.buttonLicensing)
        LicensingDialog.setTabOrder(self.buttonLicensing, self.buttonOk)
        LicensingDialog.setTabOrder(self.buttonOk, self.buttonCancel)

    def retranslateUi(self, LicensingDialog):
        LicensingDialog.setWindowTitle(_translate("LicensingDialog", "Dialog", None))
        self.labelMessage.setText(_translate("LicensingDialog", "In order to register your copy of this product, please enter your registration details here", None))
        self.labelFirstName.setText(_translate("LicensingDialog", "&First Name", None))
        self.labelLastName.setText(_translate("LicensingDialog", "&Last Name", None))
        self.labelEmail.setText(_translate("LicensingDialog", "&Email", None))
        self.labelSerial.setText(_translate("LicensingDialog", "Li&cense", None))
        self.buttonLicensing.setText(_translate("LicensingDialog", "How to license", None))
        self.buttonOk.setText(_translate("LicensingDialog", "&Ok", None))
        self.buttonCancel.setText(_translate("LicensingDialog", "Cancel", None))

