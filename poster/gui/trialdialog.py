#-*- coding: utf-8 -*-

from PyQt4.QtGui import *


class TrialDialog(QMessageBox):
    """
    """
    def __init__(self, parent=None):
        super(TrialDialog, self).__init__(parent)

        self.setText("This is the trial version of Facebook Groups Auto Poster.\n\n"
                     "The trial version presents some usage limitations and locked features.\n"
                     "To unlock all the features available, please consider buying a license key.")
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle("Trial Period")

        self.okButton = self.addButton("Ok", QMessageBox.AcceptRole)
        self.activateButton = self.addButton("Activate now", QMessageBox.ActionRole)
        self.setDefaultButton(self.activateButton)

    def clickedOption(self):
        if self.clickedButton() == self.okButton:
            return "ok"
        elif self.clickedButton() == self.activateButton:
            return "activate"
        else:
            return None
