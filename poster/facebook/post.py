#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4.QtCore import *


class Post(QObject):
    """
    A Single Post.
    """

    def __init__(self, type, data, parent=None):
        """
        parameters

            type        post type : text, link, image

            data        a dict() object.
                        items include :

                            message :   post message text

                            link    :   a link to post

                            image   :   if type is link it must 
                                        be a url to a picture file

                                        if type is image it can be : 
                                            - url to a remote picture
                                            - path to a local picture

                            name    :   it type is link, overwrites 
                                        the title in the link preview
        """

        super(Post, self).__init__(parent)

        self.type = type

        self.data = data

