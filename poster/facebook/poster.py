#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from PyQt4.QtCore import *

from .graph import FBGraph
from ..common.utils import weightedChoice
from ..logging import logger


class Poster(QObject):
    """
    Posting Scheduler.
    """

    # scheduler started
    started = pyqtSignal()

    # scheduler finished
    finished = pyqtSignal(bool)

    # task paused
    paused = pyqtSignal()

    # task resumed
    resumed = pyqtSignal()

    # errors
    error = pyqtSignal(unicode)

    # task progress
    progress = pyqtSignal(int)


    DEFAULT_WIGHT = 100

    WEIGHT_FACTOR = 0.5


    def __init__(self, access_token, 
                       tasks, 
                       minDelay, maxDelay, 
                       sleepTime, sleepAfter, 
                       stopOnErrors=True, 
                       # postLikeHuman = False,
                       session=requests.Session(), 
                       parent=None):
        """
        parameters

            access_token    user access token

            tasks           a dict() object mapping task id 
                            to task object.

            minDelay        minimum delay between posts
            
            maxDelay        maximum delay between posts

            sleepTime       sleep time after 'sleepAfter' 
                            successful posts
            
            sleepAfter      number of successful posts
                            to sleep after

            stopOnErrors    whether or not to stop if errors 
                            where encountered
        """

        super(Poster, self).__init__(parent)

        self.access_token = access_token

        self.session = session
        
        self.graph = FBGraph(access_token, self.session)

        self.tasks = tasks

        self.minDelay = minDelay
        self.maxDelay = maxDelay

        self.sleepTime = sleepTime
        self.sleepAfter = sleepAfter

        self.stopOnErrors = stopOnErrors

        weights = [self.DEFAULT_WIGHT] * len(self.tasks)

        self.weightedTasks = dict(zip(self.tasks.keys(), weights))

        self.totalPosts = sum(
            self.tasks[taskId].totalPosts for taskId 
                                          in self.tasks)
        self.totalPublishedPosts = 0
        self._progress = 0

        self._paused = False
        self._stopped = False

        self.mutex = QMutex()
        self.pauseCondition = QWaitCondition()

        self.logger = logger.getLogger()

    def updateAccessToken(self, access_token):

        self.logger.debug('[poster] updating access token...')

        self.graph.setAccessToken(access_token)

    def setRepublishLastFlag(self, republish):

        self.logger.debug('[poster] setting republish last flag...')

        self.republishLastFlag = republish

    def start(self):

        self.logger.debug("[poster] poster task started...")
        self.logger.debug("[poster] {0} tasks scheduled", len(self.tasks))
        self.logger.debug("[poster] {0} posts in total", self.totalPosts)
        
        self.started.emit()

        qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))

        while self.hasMoreTasks():

            self.logger.debug('[poster] got more tasks')

            self.checkPaused()

            if self.checkStopped():

                self.logger.debug('[poster] stopped')
                
                return

            if hasattr(self, 'republishLastFlag') and \
                    self.republishLastFlag:

                self.logger.debug('[poster] republishing last post...')

                result = self.republishLast()

                self.republishLastFlag = False

            else:

                self.logger.debug('[poster] publishing new post...')

                result = self.publishNext()

            self.logger.debug("[poster] last task target : {0}", self.lastTarget)
            self.logger.debug("[poster] task result : {0}", result)

            if not result:

                self.logger.debug('[poster] got publishing error')

                self.error.emit(self.tasks[self.lastTaskId].errorString)

                self.wait()

                if hasattr(self, 'republishLastFlag') and \
                        self.republishLastFlag:

                    continue

                elif self.stopOnErrors:

                    self.stopOnError()

                    return

                elif self.checkStopped():

                    self.logger.debug('[poster] stopping after error')

                    return

                else:

                    pass

            if result:
                
                self.logger.debug("[poster] post published successfully")
            
            else:
                self.logger.debug("[poster] publish error, continuing...")

            self.updateSchedule()

            if not self.hasMoreTasks():

                self.logger.debug('[poster] no more tasks, terminating...')

                break

            self.sleepAfterPublish()

        self.logger.debug("[poster] poster task finished.")

        self.finished.emit(True)

    def publishNext(self):

        self.logger.debug('[poster] publishing next post...')

        taskId = self.nextTaskId()

        self.logger.debug("[poster] next task id : %d" % taskId)

        task = self.tasks[taskId]

        result = task.publishNext(self.graph)

        self.lastTaskId = taskId

        self.lastTarget = task.lastTarget

        return result

    def republishLast(self):

        self.logger.debug('[poster] republishing last post...')

        self.logger.debug("[poster] restart task id : %d" % self.lastTaskId)

        task = self.tasks[self.lastTaskId]

        result = task.republishLast(self.graph)

        return result

    def wait(self):

        self.logger.debug('[poster] waiting...')

        self.mutex.lock()

        self.pauseCondition.wait(self.mutex)

        self.mutex.unlock()

    def stop(self):

        self.logger.debug('[poster] stopping...')

        self.mutex.lock()

        if self._stopped:

            self.mutex.unlock()

            return

        self._paused = False

        self._stopped = True

        self.mutex.unlock()

        self.pauseCondition.wakeAll()

    def stopOnError(self):

        self.logger.debug('[poster] stopping on error...')

        self.stop()

        self.finished.emit(False)

    def pause(self):

        self.logger.debug('[poster] pausing...')

        self.mutex.lock()

        if self._paused:
            
            self.mutex.unlock()
            
            return

        self._paused = True

        self.mutex.unlock()

        self.pauseCondition.wakeAll()

    def resume(self):

        self.logger.debug('[poster] resuming...')

        self.mutex.lock()

        if not self._paused:

            self.mutex.unlock()

            self.pauseCondition.wakeAll()

            return

        self._paused = False

        self.mutex.unlock()

        self.pauseCondition.wakeAll()

        self.resumed.emit()

    def hasMoreTasks(self):

        return (len(self.weightedTasks) > 0)

    def nextTaskId(self):

        self.logger.debug('[poster] choosing next task...')

        taskId = weightedChoice(self.weightedTasks.items())

        return taskId

    def updateSchedule(self):

        self.logger.debug('[poster] updating schedule...')

        if self.tasks[self.lastTaskId].isFinished():

            self.logger.debug("[poster] task %d finished" % self.lastTaskId)

            self.removeTask(self.lastTaskId)

        else:

            self.weightedTasks[self.lastTaskId] *= self.WEIGHT_FACTOR

            for taskId in self.weightedTasks.keys():

                self.tasks[taskId].updateWeight(self.lastTarget)

        self.totalPublishedPosts += 1

        self.updateProgress()

    def updateProgress(self):

        self.logger.debug('[poster] updating progress...')
        
        _progress = (self.totalPublishedPosts * 100) / \
                     self.totalPosts

        if _progress != self._progress:

            self._progress = _progress

            self.progress.emit(self._progress)

    def appendTask(self, task):
        """
        Append a new task to the schedule.
        """

        self.logger.debug('[poster] appending new task...')

        self.tasks[task.id] = task

        self.weightedTasks[task.id] = self.DEFAULT_WIGHT

        self.totalPosts += task.totalPosts

        self.updateProgress()

    def removeTask(self, taskId):
        """
        Remove a task from the schedule.
        """

        self.logger.debug('[poster] removing task : {0}', taskId)

        if self.weightedTasks.has_key(taskId):

            self.weightedTasks.pop(taskId)


    def checkPaused(self):

        self.logger.debug('[poster] checking if paused...')

        self.mutex.lock()

        if self._paused:

            self.paused.emit()

            self.pauseCondition.wait(self.mutex)

        self.mutex.unlock()

    def checkStopped(self):

        self.logger.debug('[poster] checking if stopped...')

        self.mutex.lock()

        if self._stopped:

            self.mutex.unlock()

            self.finished.emit(False)
            
            return True

        self.mutex.unlock()
        
        return False

    def sleepAfterPublish(self):

        self.logger.debug('[poster] sleeping after publishing...')

        self.mutex.lock()

        if self._stopped:

            self.mutex.unlock()

            return

        if (self.totalPublishedPosts % self.sleepAfter) == 0:

            _t = self.sleepTime

        else:
            _diff = abs(self.maxDelay - self.minDelay)
            
            _t = (qrand() % _diff) + self.minDelay

        self.logger.debug("[poster] sleeping for %d secs" % _t)

        self.pauseCondition.wait(self.mutex, _t * 1000)

        self.mutex.unlock()


