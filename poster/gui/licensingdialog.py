#-*- coding: utf-8 -*-

import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .ui_licensing import Ui_LicensingDialog
from .licenserequestdialog import LicenseRequestDialog
from ..licensing.licenser import Licenser
from ..common import consts


class LicensingDialog(QDialog):
    """
    """
    def __init__(self, parent=None):
        super(LicensingDialog, self).__init__(parent)
        
        self.ui = Ui_LicensingDialog()
        self.ui.setupUi(self)

        self.licenser = Licenser(self)

        self.setInputValidators()
        self.loadSavedDetails()

        self.setWindowTitle(QString("%1 - Registration").arg(consts.__appname__))

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

    def accept(self):
        if self.checkUserInput():
            
            firstName = unicode(self.ui.textFirstName.text())
            lastName = unicode(self.ui.textLastName.text())
            email = unicode(self.ui.textEmail.text())
            license = unicode(self.ui.textLicense.toPlainText())

            self.licenser.setUserDetails(firstName, lastName, email)
            licenseObj = self.licenser.checkUserLicense(license)
            
            if not licenseObj:
                QMessageBox.warning(self, 
                    "Registration Failed",
                    "Invalid registration details.\n"
                    "Please enter the correct registration details "
                    "before continuing.\n\n" 
                    "Reason : %s" % self.licenser.errorString)
                
                return
            else:
                self.licenser.setUserLicense(license)

                requestObj = licenseObj.request

                QMessageBox.information(self, 
                    "Registration Succeeded",
                    "Thank your for your purchasing this product.\n\n"
                    "License Details:\n\n"
                    "   User Name : %s\n"
                    "   Email : %s\n"
                    # "   Hostname : %s\n"
                    # "   HDD Serial : %s\n"
                    # "   BIOS Serial : %s\n"
                    # "   CPU ID : %s\n"
                    # "   Interface MAC : %s\n"
                    "\n"
                    "   Valid From : %s\n"
                    "   Valid Until : %s\n"
                    "   Valid For : %d days" % (
                        requestObj.firstName + ' ' + requestObj.lastName,
                        requestObj.email,
                        # requestObj.hostname,
                        # requestObj.hdd_sn,
                        # requestObj.bios_sn,
                        # requestObj.cpu_id,
                        # requestObj.mac,
                        time.ctime(licenseObj.begin),
                        time.ctime(licenseObj.expire),
                        licenseObj.duration / (24*3600)
                    ))

                QMessageBox.information(self, 
                    "License Terms",
                    "Please note that this license is only valid for "
                    "one installation on one machine and may be "
                    "invalidated if the system configuration changes.")

                del requestObj
                del licenseObj

                super(LicensingDialog, self).accept()

        else:
            QMessageBox.warning(self, 
                "Registration Failed",
                "Please enter all the registration details correctly\n"
                "in the corresponding fields before continuing.")

    def checkUserInput(self):
        valid = True
        inputs = [self.ui.textFirstName, self.ui.textLastName, 
                  self.ui.textEmail]
        for _input in inputs:
            valid = valid and _input.hasAcceptableInput()
            if not valid:
                break
        if valid:
            license = self.ui.textLicense.toPlainText().trimmed()
            valid = not license.isEmpty()
        return valid

    def howToLicense(self):
        dialog = LicenseRequestDialog(self)
        dialog.exec_()
