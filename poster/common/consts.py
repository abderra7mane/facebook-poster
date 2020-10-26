#!/usr/bin/env python
#-*- coding: utf-8 -*-


__appname__     = 'Poster'
__description__ = 'Facebook Groups Auto Poster'
__version__     = '1.0'
__company__     = 'Poster Inc.'
__domain__      = 'poster.com'
__author__      = 'Abderrahmane Mokrani'
__email__       = 'm.abderra7mane@gmail.com'
__copyright__   = 'Copyright (C) 2017'



FB_CLIENT_ID = '145634995501895'

FB_GRAPH_URL = 'https://graph.facebook.com/{version}/{node}'
FB_OAUTH_URL = 'https://www.facebook.com/{version}/dialog/oauth'
FB_OAUTH_REDIRECT_URL = 'https://www.facebook.com/connect/login_success.html'

FB_GRAPH_VERSIONS = ['2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8']
FB_GRAPH_DEFAULT_VERSION = FB_GRAPH_VERSIONS[-1]

FB_PERMISSIONS = ['public_profile', 'user_friends', 'email', 'user_about_me', 
                  'user_actions.books', 'user_actions.fitness', 'user_actions.music', 
                  'user_actions.news', 'user_actions.video', 'user_birthday', 
                  'user_education_history', 'user_events', 'user_games_activity', 
                  'user_hometown', 'user_likes', 'user_location', 'user_managed_groups', 
                  'user_photos', 'user_posts', 'user_relationships', 
                  'user_relationship_details', 'user_religion_politics', 'user_tagged_places', 
                  'user_videos', 'user_website', 'user_work_history', 'read_custom_friendlists', 
                  'read_insights', 'read_audience_network_insights', 'read_page_mailboxes', 
                  'manage_pages', 'publish_pages', 'publish_actions', 'rsvp_event', 
                  'pages_show_list', 'pages_manage_cta', 'pages_manage_instant_articles', 
                  'ads_read', 'ads_management', 'business_management', 'pages_messaging', 
                  'pages_messaging_subscriptions', 'pages_messaging_payments', 
                  'pages_messaging_phone_number','manage_notifications', 'read_stream', 
                  'read_mailbox', 'user_groups', 'user_status']

DEFAULT_BUSY_MESSAGE = 'still working...'

USER_NAME_MINLEN = 2
USER_NAME_MAXLEN = 30
USER_NAME_REGEXP = r'^[a-zA-Z]{%d,%d}$' % (USER_NAME_MINLEN, USER_NAME_MAXLEN)
USER_EMAIL_REGEXP = r'^[a-zA-Z0-9._-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'

APP_TRIAL_MAX_USAGE = 10
APP_TRIAL_MAX_DAYS = 5

APP_ABOUT_TEMPLATE = """
<html>
    <head/>
    <body>
        <p align="center">
            <span style="font-size:18pt; font-weight:600;">
                {appname} {version}
            </span>
        </p>
        <p align="center">
            <span style="font-size:12pt;">
                {description}
            </span>
        </p>
        <p align="center">
            <br/>
        </p>
        <p align="center">
            {copyright} - {author}
            <br/>
            Contact: 
            <span style="color:blue; text-decoration:underline;">
                {contact}
            </span>
        </p>
    </body>
</html>
"""