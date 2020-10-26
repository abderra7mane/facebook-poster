#-*- coding: utf-8 -*-

from PyQt4.QtGui import *


class FakeLicenseDialog(QMessageBox):
    """
    """
    def __init__(self, parent=None):
        super(FakeLicenseDialog, self).__init__(parent)

        self.setText("The license used to register this product is fake, "
                     "has expired \nor the system configuration has changed.\n\n"
                     "Please reenter the correct registration details "
                     "or buy a new license.")
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("Registration Failed")
