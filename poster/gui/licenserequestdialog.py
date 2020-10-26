#-*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .ui_licenserequest import Ui_LicenseRequestDialog
from ..licensing.licenser import Licenser
from ..common import consts


class LicenseRequestDialog(QDialog):
    """
    """
    def __init__(self, parent=None):
        super(LicenseRequestDialog, self).__init__(parent)
        
        self.ui = Ui_LicenseRequestDialog()
        self.ui.setupUi(self)

        self.licenser = Licenser(self)

        self.setInputValidators()
        self.loadSavedDetails()

        self.setWindowTitle(QString("%1 - License Request").arg(consts.__appname__))

    def setInputValidators(self):
        nameValidator = QRegExpValidator(QRegExp(consts.USER_NAME_REGEXP))
        emailValidator = QRegExpValidator(QRegExp(consts.USER_EMAIL_REGEXP))

        self.ui.textFirstName.setValidator(nameValidator)
        self.ui.textLastName.setValidator(nameValidator)
        self.ui.textEmail.setValidator(emailValidator)

    def loadSavedDetails(self):
        self.ui.textFirstName.setText(
                self.licenser.firstName)
        self.ui.textLastName.setText(
                self.licenser.lastName)
        self.ui.textEmail.setText(
                self.licenser.email)

    def checkUserInput(self):
        valid = True
        inputs = [self.ui.textFirstName, 
                  self.ui.textLastName, 
                  self.ui.textEmail]
        for _input in inputs:
            valid = valid and _input.hasAcceptableInput()
            if not valid:
                break
        return valid

    def generateRequest(self):
        if self.checkUserInput():

            self.ui.textRequest.clear()

            firstName = unicode(self.ui.textFirstName.text())
            lastName = unicode(self.ui.textLastName.text())
            email = unicode(self.ui.textEmail.text())

            self.licenser.setUserDetails(firstName, lastName, email)

            request = self.licenser.generateRequest()
            
            if not request:
                QMessageBox.critical(self,
                    "Request Failed",
                    "Failed to generate a license request."
                    # "\n\nReason : %s" % self.licenser.errorString
                    )
                return

            self.ui.textRequest.setPlainText(request)

        else:
            QMessageBox.warning(self, 
                "Request Failed",
                "Please enter all the registration details correctly\n"
                "in the corresponding fields before continuing.")

    def copyRequest(self):
        request = self.ui.textRequest.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(request)
