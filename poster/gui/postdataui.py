#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .ui_postdata import Ui_PostDataUi
from ..facebook.post import Post
from ..facebook.postertask import PosterTask
from ..common.utils import colorizeHtmlText, truncateString
import resources_rc


class PostDataUi(QWidget):
    """
    The widget interface for the post data.
    """

    TRIAL_MAX_TARGETS = 10

    POST_TYPES = ['text', 'link', 'image']


    def __init__(self, post=None, 
                       showAll=False, 
                       showLikes=False, 
                       isTrial=False,
                       parent=None):
        super(PostDataUi, self).__init__(parent)

        self.ui = Ui_PostDataUi()
        self.ui.setupUi(self)

        self.showAll = showAll
        self.showLikes = showLikes

        self.isTrial = isTrial

        if not self.showLikes:
            index = self.ui.postTargetsTabWidget.indexOf(
                self.ui.tabLikes)
            self.ui.postTargetsTabWidget.removeTab(index)

        self.ui.postTypeButtonGroup.setId(
            self.ui.postTypeText, 0)

        self.ui.postTypeButtonGroup.setId(
            self.ui.postTypeLink, 1)
        
        self.ui.postTypeButtonGroup.setId(
            self.ui.postTypeImage, 2)

        if post is not None:
            self.loadPostData(post)

        self.ui.groupsListWidget.itemChanged.connect(
                            self.updateSelectedGroups)
        self.ui.pagesListWidget.itemChanged.connect(
                            self.updateSelectedPages)
        self.ui.likesListWidget.itemChanged.connect(
                            self.updateSelectedLikes)

    def __getattribute__(self, attribute):

        if attribute == 'type':

            return self.POST_TYPES[
                    self.ui.postTypeButtonGroup.checkedId()]

        elif attribute == 'message':

            return self.ui.postMessageText.toPlainText()

        elif attribute == 'name':

            return self.ui.postNameText.text()

        elif attribute == 'link':

            return self.ui.postLinkText.text()

        elif attribute == 'image':

            return self.ui.postPictureText.text()

        else:
            return super(PostDataUi, self).__getattribute__(attribute)

    def loadPostData(self, post):

        types = ['text', 'link', 'image']

        try:
            _id = types.index(post.type)
        
        except ValueError:
            
            return

        self.ui.postTypeButtonGroup.button(_id).setChecked(True)
        self.postTypeChanged(_id)

        self.ui.postMessageText.setText(post.data['message'])
        self.ui.postLinkText.setText(post.data['link'])
        self.ui.postPictureText.setText(post.data['image'])
        self.ui.postNameText.setText(post.data['name'])

    def postTypeChanged(self, buttonId):

        postType = self.type

        itemsList = [
            self.ui.postMessageText, 
            self.ui.postNameText, 
            self.ui.postLinkText, 
            self.ui.postPictureText,
            self.ui.postPictureChooserButton
        ]

        if postType == 'text':
            
            actionsList = [True, False, False, False, False]

        elif postType == 'link':
            
            actionsList = [True, True, True, True, False]
        
        else:
            actionsList = [True, False, False, True, True]

        for item, enable in zip(itemsList, actionsList):
            
            item.setEnabled(enable)

    def choosePostPicture(self):

        fileName = QFileDialog.getOpenFileName(self, 
            "Choose Picture", 
            ".", 
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")

        if fileName.isNull():
            return

        self.ui.postPictureText.setText(fileName)

    def updateUserGroups(self, user_groups):

        groupsListWidget = self.ui.groupsListWidget

        groupsListWidget.clear()

        groupsCount = len(user_groups)

        for group in user_groups:

            if not self.showAll and \
                    group['privacy'].upper() != 'OPEN':
                continue

            item = QListWidgetItem()

            item.setText(group['name'])

            try:
                item.setToolTip(truncateString(group['description']))
            
            except KeyError:
                item.setToolTip(group['name'])

            data = '{}|{}|{}'.format('group', 
                                     group['id'], 
                                     group['privacy'])
            
            item.setData(Qt.UserRole, data)
            
            if group['privacy'].upper() == 'OPEN':
                
                icon = QIcon(':/img/lock-open.png')
            
            else:
                icon = QIcon(':/img/lock-closed.png')

            item.setIcon(icon)

            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            
            item.setCheckState(Qt.Unchecked)

            groupsListWidget.addItem(item)

        self.updateSelectedGroups()

    def updateSelectedGroups(self):

        groupsListWidget = self.ui.groupsListWidget

        groupsCount = groupsListWidget.count()
        selectedGroupsCount = self.getSelectedItemsCount(groupsListWidget)

        self.ui.totalGroupsLabel.setText("Total Groups : {0}/{1}".format(
                                colorizeHtmlText(selectedGroupsCount, 'green'),
                                colorizeHtmlText(groupsCount, 'red')))

    def updateUserPages(self, user_pages):

        pagesListWidget = self.ui.pagesListWidget

        pagesListWidget.clear()

        pagesCount = len(user_pages)

        for page in user_pages:

            item = QListWidgetItem()

            item.setText(page['name'])

            data = '{}|{}|{}'.format('page', 
                                     page['id'], 
                                     page['access_token'])
            
            item.setData(Qt.UserRole, data)
            
            try:
                item.setToolTip(truncateString(page['about']))
            
            except KeyError:
                item.setToolTip(page['name'])

            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            
            item.setCheckState(Qt.Unchecked)

            pagesListWidget.addItem(item)

        self.updateSelectedPages()

    def updateSelectedPages(self):

        pagesListWidget = self.ui.pagesListWidget

        pagesCount = pagesListWidget.count()
        selectedPagesCount = self.getSelectedItemsCount(pagesListWidget)

        self.ui.totalPagesLabel.setText("Total Pages : {0}/{1}".format(
                                colorizeHtmlText(selectedPagesCount, 'green'),
                                colorizeHtmlText(pagesCount, 'red')))

    def updateUserLikes(self, user_likes):

        if not self.showLikes:
            return

        likesListWidget = self.ui.likesListWidget

        likesListWidget.clear()

        likesCount = len(user_likes)

        self.ui.totalLikesLabel.setText("Total Likes : {0}/{1}".format(
                                self.getSelectedItemsCount(likesListWidget),
                                colorizeHtmlText(likesCount, 'red')))

        for page in user_likes:

            item = QListWidgetItem()

            item.setText(page['name'])

            data = '{}|{}'.format('like', page['id'])
            
            item.setData(Qt.UserRole, data)
            
            try:
                item.setToolTip(truncateString(page['about']))
            
            except KeyError:
                item.setToolTip(page['name'])

            if page['can_post']:
                
                icon = QIcon(':/img/lock-open.png')
            
            else:
                icon = QIcon(':/img/lock-closed.png')

            item.setIcon(icon)

            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            
            item.setCheckState(Qt.Unchecked)

            likesListWidget.addItem(item)

        self.updateSelectedLikes()

    def updateSelectedLikes(self):

        likesListWidget = self.ui.likesListWidget

        likesCount = likesListWidget.count()
        selectedLikesCount = self.getSelectedItemsCount(likesListWidget)

        self.ui.totalLikesLabel.setText("Total Likes : {0}/{1}".format(
                                colorizeHtmlText(selectedLikesCount, 'green'),
                                colorizeHtmlText(likesCount, 'red')))

    def savePost(self):

        if self.type == 'text' and self.message.isEmpty():

            self.errorString = "Empty message field."
            
            return False

        elif self.type == 'link' and self.link.isEmpty():

            self.errorString = "Empty link field."
            
            return False

        elif self.type == 'image' and self.image.isEmpty():

            self.errorString = "Empty image field."
            
            return False

        targets = self.getSelectedTargets()

        if not targets:

            self.errorString = "No target has been selected"

            return False

        elif self.isTrial and len(targets) > self.TRIAL_MAX_TARGETS:

            self.errorString = ("You cannot select more than %d targets in "
                                "the trial version." % (self.TRIAL_MAX_TARGETS))

            return False

        self.post = self.getPost()

        self.targets = targets

        return True

    def getPost(self):

        data = {
            'message' : unicode(self.message), 
            'name' : unicode(self.name), 
            'link' : unicode(self.link), 
            'image' : unicode(self.image)
        }

        return Post(self.type, data)

    def getPosterTask(self):

        if not hasattr(self, 'post') or self.post is None:

            return

        if not hasattr(self, 'targets') or self.targets is None:

            return

        task = PosterTask(0, self.post, self.targets)

        return task

    def getSelectedTargets(self):

        targets = dict()

        targets.update(self.getSelectedGroups())
        targets.update(self.getSelectedPages())
        targets.update(self.getSelectedLikes())

        return targets

    def getSelectedGroups(self):

        result = dict()

        selectedItemsData = self.getSelectedItemsData(
            self.ui.groupsListWidget)

        for itemData in selectedItemsData:

            type, id, privacy = itemData.split('|')

            result[id] = { 'type' : type, 'privacy' : privacy }

        return result

    def getSelectedPages(self):

        result = dict()

        selectedItemsData = self.getSelectedItemsData(
            self.ui.pagesListWidget)

        for itemData in selectedItemsData:

            type, id, access_token = itemData.split('|')

            result[id] = {
                'type' : type, 
                'access_token' : access_token
            }

        return result


    def getSelectedLikes(self):

        result = dict()

        selectedItemsData = self.getSelectedItemsData(
            self.ui.likesListWidget)

        for itemData in selectedItemsData:

            type, id = itemData.split('|')

            result[id] = { 'type' : type }

        return result

    def getSelectedItemsData(self, listWidget):

        result = list()

        for row in range(listWidget.count()):

            item = listWidget.item(row)

            if item.checkState() == Qt.Checked:

                data = unicode(item.data(Qt.UserRole).toString())

                result.append(data)

        return result

    def getSelectedItemsCount(self, listWidget):

        count = 0

        for row in range(listWidget.count()):

            item = listWidget.item(row)

            if item.checkState() == Qt.Checked:

                count += 1

        return count

    def clearUserData(self):

        self.ui.groupsListWidget.clear()
        self.ui.totalGroupsLabel.setText("Total Groups : 0")

        self.ui.pagesListWidget.clear()
        self.ui.totalPagesLabel.setText("Total Pages : 0")
        
        self.ui.likesListWidget.clear()
        self.ui.totalLikesLabel.setText("Total Likes : 0")

        self.post = None
        self.targets = None

    def filterGroups(self, filterString):

        self.filterItems(self.ui.groupsListWidget, filterString)

    def filterPages(self, filterString):

        self.filterItems(self.ui.pagesListWidget, filterString)

    def filterLikes(self, filterString):

        self.filterItems(self.ui.likesListWidget, filterString)

    def filterItems(self, listWidget, filterString):

        itemCount = listWidget.count()

        for row in range(itemCount):

            item = listWidget.item(row)

            itemText = item.text()

            if itemText.contains(filterString, Qt.CaseInsensitive):

                item.setHidden(False)

            else:
                item.setHidden(True)

    def selectAllVisibleGroups(self, checked):

        self.selectAllVisibleItems(self.ui.groupsListWidget, checked)

    def selectAllVisiblePages(self, checked):

        self.selectAllVisibleItems(self.ui.pagesListWidget, checked)

    def selectAllVisibleLikes(self, checked):

        self.selectAllVisibleItems(self.ui.likesListWidget, checked)

    def selectAllVisibleItems(self, listWidget, checked):

        checkStates = [Qt.Unchecked, Qt.Checked]

        itemCount = listWidget.count()

        for row in range(itemCount):

            item = listWidget.item(row)

            if not item.isHidden():

                item.setCheckState(checkStates[checked])
