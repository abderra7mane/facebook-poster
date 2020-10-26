#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4.QtCore import *

from ..common.utils import weightedChoice
from .exceptions import FBGraphError
from ..logging import logger


class PosterTask(QObject):
    """
    A Scheduled Task for Poster.
    """

    DEFAULT_WIGHT = 100

    WEIGHT_FACTOR = 0.5


    def __init__(self, id, post, targets, parent=None):
        """
        parameters

            id          application generated task id

            post        Post() objcet

            targets     a dict() object mapping target id
                        to a dict() of target details.

                        details include:
                            
                            type    :   user, group, page, like

                            privacy :   group privacy policy 
                                        if type is set to group
                                        
                                        possible values : open, closed

                            access_token    :   page access token 
                                                if type is set to page
        """

        super(PosterTask, self).__init__(parent)

        self.id = id

        self.post = post

        self.targets = targets

        self.totalPosts = len(self.targets)

        weights = [self.DEFAULT_WIGHT] * self.totalPosts

        self.weightedTargets = dict(zip(self.targets.keys(), weights))

        self.totalPublishedPosts = 0

        self.logger = logger.getLogger()

    def setId(self, id):

        self.logger.debug("[task] setting task id : {0}", id)

        self.id = id

    def addTargets(self, targets):

        self.logger.debug("[task] adding {0} new targets...", len(targets))

        self.targets.update(targets)

        weights = [self.DEFAULT_WIGHT] * len(targets)

        weightedTargets = dict(zip(targets.keys(), weights))

        self.weightedTargets.update(weightedTargets)

        self.totalPosts = len(self.targets)

    def publishNext(self, graph):

        self.logger.debug("[task] publishing next post...")

        targetId = self._nextTargetId()

        return self.publishToTarget(targetId, graph)

    def republishLast(self, graph):

        self.logger.debug("[task] republishing last post...")

        return self.publishToTarget(self.lastTarget, graph)

    def publishToTarget(self, targetId, graph):

        self.logger.debug("[task] next target : {0}", targetId)

        target = self.targets[targetId]

        targetType = target['type']

        self.logger.debug("[task] target type : {0}", targetType)

        args = dict()

        if targetType == 'user':
            
            pass

        elif targetType == 'group':

            pass

        elif targetType == 'page':

            args['access_token'] = target['access_token']

        else:
            assert (targetType == 'like')

            args['version'] = '2.3'

        postType = self.post.type

        self.logger.debug("[task] post type : {0}", postType)

        if postType == 'text':

            result = self.publishAsText(graph, targetId, **args)

        elif postType == 'link':

            result = self.publishAsLink(graph, targetId, **args)

        else:
            assert postType == 'image'

            result = self.publishAsImage(graph, targetId, **args)

        self.lastTarget = targetId

        if result:

            self.totalPublishedPosts += 1

            self.logger.debug("[task] post published successfully")

            self.weightedTargets.pop(targetId)

        return result

    def _nextTargetId(self):

        self.logger.debug("[task] choosing next target...")

        targetId = weightedChoice(self.weightedTargets.items())

        return targetId

    def publishAsText(self, graph, targetId, **args):

        self.logger.debug("[task] publishing post as text...")

        message = self.post.data['message']

        try:
            return graph.put_message(targetId, message, **args)

        except FBGraphError as e:

            self.errorString = e.message

    def publishAsLink(self, graph, targetId, **args):

        self.logger.debug("[task] publishing post as link...")

        data = self.post.data

        assert data.has_key('link')

        args.update(data)

        try:
            return graph.put_link(targetId, **args)

        except FBGraphError as e:

            self.errorString = e.message

    def publishAsImage(self, graph, targetId, **args):

        self.logger.debug("[task] publishing post as image...")

        image = self.post.data['image']

        args['message'] = self.post.data['message']

        try:
            return graph.put_image(targetId, image, **args)

        except FBGraphError as e:

            self.errorString = e.message

    def updateWeight(self, target):

        self.logger.debug("[task] updating posts' weights...")

        if self.weightedTargets.has_key(target):

            self.weightedTargets[target] *= self.WEIGHT_FACTOR

    def isFinished(self):

        return (len(self.weightedTargets) == 0)

