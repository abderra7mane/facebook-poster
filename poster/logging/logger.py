#-*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtSignal


DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50


def getLogger():
    return Logger()


class Logger(QObject):
    """ 
    """

    class __impl(QObject):
        """
        """
        logMessage = pyqtSignal(unicode, tuple, dict)

        def __init__(self, parent=None):
            QObject.__init__(self, parent)
            self.setLevel(DEBUG)

        def setLevel(self, level):
            self.level = level

        def log(self, level, msg, *args, **kwargs):
            if level >= self.level:
                self.logMessage.emit(msg, args, kwargs)

        def debug(self, msg, *args, **kwargs):
            self.log(DEBUG, msg, *args, **kwargs)

        def info(self, msg, *args, **kwargs):
            self.log(INFO, msg, *args, **kwargs)

        def warning(self, msg, *args, **kwargs):
            self.log(WARNING, msg, *args, **kwargs)

        def error(self, msg, *args, **kwargs):
            self.log(ERROR, msg, *args, **kwargs)

        def critical(self, msg, *args, **kwargs):
            self.log(CRITICAL, msg, *args, **kwargs)

        def registerHandler(self, handler):
            self.logMessage.connect(handler)

        def removeHandler(self, handler):
            self.logMessage.disconnect(handler)

    __instance = None

    def __init__(self, parent=None):
        super(Logger, self).__init__(parent)

        if Logger.__instance is None:
            Logger.__instance = Logger.__impl()

        self.__dict__['_Logger__instance'] = Logger.__instance

    def __getattr__(self, attr):
        return getattr(Logger.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(Logger.__instance, attr, value)
