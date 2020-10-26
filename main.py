#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from functools import partial
from PyQt4.QtCore import Qt, QString, QFile, QTimer
from PyQt4.QtGui import QApplication, QSystemTrayIcon, QIcon, QPixmap, QSplashScreen

from poster.gui.posterui import PosterUi
from poster.gui.trialdialog import TrialDialog
from poster.gui.fakelicensedialog import FakeLicenseDialog
from poster.gui.licensingdialog import LicensingDialog
from poster.licensing.licenser import Licenser
from poster.logging import logger
from poster.common import consts
import poster.gui.resources_rc


if __name__ == '__main__':

    logger_levels = {
        '-log-debug' : logger.DEBUG,
        '-log-info' : logger.INFO,
        '-log-warning' : logger.WARNING,
        '-log-error' : logger.ERROR,
        '-log-critical' : logger.CRITICAL
    }

    _level = logger_levels['-log-info']

    for arg in sys.argv:
        if arg in logger_levels:
            _level = logger_levels[arg]

    for lvl in logger_levels:
        if lvl in sys.argv:
            sys.argv.remove(lvl)

    _logger = logger.getLogger()
    _logger.setLevel(_level)

    app = QApplication(sys.argv)

    app.setOrganizationName(consts.__company__)
    app.setOrganizationDomain(consts.__domain__)
    app.setApplicationName(consts.__appname__)
    app.setApplicationVersion(consts.__version__)

    app.setWindowIcon(QIcon(':/img/icon.png'))

    ##

    splash_pix = QPixmap(':/img/splash.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())

    # styleFile = QFile(':/qss/style.qss')

    # if styleFile.open(QFile.ReadOnly):
    #     stylesheet = QString(styleFile.readAll())
    #     app.setStyleSheet(stylesheet)

    # if QSystemTrayIcon.isSystemTrayAvailable():
    #     app.setQuitOnLastWindowClosed(False)

    licenser = Licenser()

    while True:
        splash.show()

        licensed = licenser.hasLicense()
        license_valid = licensed and licenser.checkUserLicense()
        trial_active = licenser.isTrialActive()

        if licensed and license_valid:
            trial_active = False
            break

        elif licensed and not license_valid:
            trial_active = False
            licensed = False
            dialog = FakeLicenseDialog()
            splash.finish(dialog)
            dialog.exec_()

        if trial_active:
            dialog = TrialDialog()
            splash.finish(dialog)
            dialog.exec_()
            if dialog.clickedOption() == "activate":
                pass
            else:
                break

        if not licensed:
            dialog = LicensingDialog()
            splash.finish(dialog)
            if dialog.exec_():
                continue
            else:
                break

    if trial_active or (licensed and license_valid):
        splash.show()
        window = PosterUi(trial_active)
        window.show()
        QTimer.singleShot(1000, partial(splash.finish, window))

    ##################################################################################
    ##
    ##                      disable not implemented features
    ##
        window.ui.postLikeHumanCheckBox.setVisible(False)
    ##
    ##################################################################################
    else:
        QTimer.singleShot(0, app.quit)

    sys.exit(app.exec_())

