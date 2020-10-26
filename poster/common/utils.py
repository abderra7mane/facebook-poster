#!/usr/bin/env python
#-*- coding: utf-8 -*-

from urlparse import parse_qs
import random
import requests
from PyQt4.QtCore import *


def is_iterable(obj):
    return (isinstance(obj, list) or 
            isinstance(obj, tuple))


def getSyncFile(url, cookies=None):
    """
    Download a file synchronously using http.
    """

    try:
        response = requests.get(url, cookies=cookies)
    
    except requests.ConnectionError:
        error = "Failed to establish a connection to the host."
        
        return False, error
    
    except requests.RequestException as e:
        error = e.message
        
        return False, error

    return True, response.content

def weightedChoice(choices):

    if not choices:
        return

    total = sum(weight for item, weight in choices)

    choice = random.uniform(0, total)

    upto = 0

    for item, weight in choices:

        if (upto + weight) >= choice:

            return item

        upto += weight

def qtCookie_to_dict(qtCookie):

    cookie = {
        'version' : 0,
        'name' : unicode(qtCookie.name()),
        'value' : unicode(qtCookie.value()),
        'port' : None,
        'domain' : unicode(qtCookie.domain()), 
        'path' : unicode(qtCookie.path()), 
        'secure' : qtCookie.isSecure(), 
        'expires' : QDateTime.currentDateTime().secsTo(qtCookie.expirationDate()), 
        'discard' : qtCookie.isSessionCookie(), 
        'comment' : None,
        'comment_url' : None,
        'rest' : {'HttpOnly' : qtCookie.isHttpOnly()},
        'rfc2109' : False
    }

    return cookie

def qtCookies_to_list(qtCookies):

    cookies = list()

    for qtCookie in qtCookies:

        cookies.append(qtCookie_to_dict(qtCookie))

    return cookies

def colorizeHtmlText(text, color):

    pattern = QString("<span style='color: %1;'>%2</span>")
    
    return pattern.arg(color).arg(text)

def truncateString(text, maxLength=80):

    text = unicode(text)

    if len(text) <= maxLength:
        return text

    else:
        return text[0 : maxLength - 3] + '...'

def fetchTokenFromUrl(url):
    """
    Fetch the access token from the redirect url.
    """
    
    fragment = unicode(url.fragment())
    result = parse_qs(fragment)

    if result.has_key('access_token'):

        return result['access_token'][0]

def fetchErrorFromUrl(url):
    """
    Fetch the error string from the redirect url.
    """
    
    query = unicode(QString(url.encodedQuery()))
    result = parse_qs(query)

    if result.has_key('error'):

        error = result['error'][0]
        
        if result.has_key('error_description'):
            
            error_description = \
                result['error_description'][0]
        
        else:
            error_description = error
        
        return error, error_description

    return None, None

