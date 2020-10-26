
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from .ui_settings import Ui_SettingsDialog
from ..common import consts


class SettingsDialog(QDialog):
    """
    """
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self.settings = dict()

        self.loadSettings()
        self.updateUi()

        self.setWindowTitle("Settings")

    def loadSettings(self):

        settings = QSettings()

        settings.beginGroup('app')

        self.settings['showAll'] = settings.value(
                'showAll', False).toBool()

        self.settings['showLikes'] = settings.value(
                'showLikes', False).toBool()

        self.settings['appID'] = unicode(settings.value(
                'appID', consts.FB_CLIENT_ID).toString())

        versions = settings.value('apiVersions', 
                                  consts.FB_GRAPH_VERSIONS).toList()
        
        self.settings['apiVersions'] = [
                unicode(item.toString()) for item in versions]
        
        self.settings['apiDefaultVersion'] = unicode(
            settings.value('apiDefaultVersion', 
                consts.FB_GRAPH_DEFAULT_VERSION).toString())

        self.settings['showAdvancedWarning'] = settings.value(
                'showAdvancedWarning', True).toBool()

        settings.endGroup()

    def saveSettings(self):

        settings = QSettings()

        settings.beginGroup('app')

        for key, value in self.settings.items():
            settings.setValue(key, value)

        settings.endGroup()

    def updateSettings(self):

        self.settings['showAll'] = self.ui.showAllGroupsCheckBox.isChecked()
        self.settings['showLikes'] = self.ui.showLikesCheckBox.isChecked()
        
        self.settings['appID'] = unicode(
                self.ui.appIDText.text())
        self.settings['apiDefaultVersion'] = unicode(
                self.ui.apiVersionsCombo.currentText())

    def updateUi(self):

        self.ui.showAllGroupsCheckBox.setChecked(self.settings['showAll'])
        self.ui.showLikesCheckBox.setChecked(self.settings['showLikes'])

        self.ui.appIDText.setText(self.settings['appID'])

        index = 0

        for i, item in enumerate(sorted(self.settings['apiVersions'])):
            self.ui.apiVersionsCombo.addItem(item)

            if item == self.settings['apiDefaultVersion']:
                index = i

        self.ui.apiVersionsCombo.setCurrentIndex(index)

    def accept(self):

        self.updateSettings()
        self.saveSettings()
        
        super(SettingsDialog, self).accept()

    def enableAdvancedSettings(self, enable):

        if enable and self.settings['showAdvancedWarning']:

            msgBox = QMessageBox(self)

            msgBox.setWindowTitle("Attention")
            
            msgBox.setIcon(QMessageBox.Warning)
            
            msgBox.setText(
                "Making modifications to the settings under this section may \n"
                "result in the application being non-functional.\n\n"
                "It is discouraged to make any modifications unless you really\n"
                "know what you are doing!")

            okButton = msgBox.addButton(
                "Ok", QMessageBox.AcceptRole)

            cancelButton = msgBox.addButton(
                "Cancel", QMessageBox.DestructiveRole)
            
            dontShowButton = msgBox.addButton(
                "Don't show again", QMessageBox.ActionRole)

            msgBox.setDefaultButton(cancelButton)

            msgBox.exec_()

            if msgBox.clickedButton() == cancelButton:

                self.ui.enableAdvancedButton.setChecked(False)

                return

            if msgBox.clickedButton() == dontShowButton:

                self.settings['showAdvancedWarning'] = False

                self.saveSettings()

        self.ui.advancedSettingsBox.setEnabled(enable)
