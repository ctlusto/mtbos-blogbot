#!/usr/bin/env python

# Take a local YAML file with a curated list of blogs
# containing the author's twitter handle and the url to the
# syndicated XML feed and update a Firebase data store.
#
# Only push new records; blogs already in the data store are ignored.
# It's basically just a simple way to update Firebase consistently
# with new feeds to follow, without having to edit the store directly.
#
# Also take a current snapshot of the feed's ETag and/or
# Last-Modified headers so that the main script can make
# conditional GET requests and only download full feeds when
# the returned XML has been altered (i.e. something new has been
# been published) since the last request.
#
# (Note: In a few edge cases the ETag check produces false positives,
# so cache a url to the most recent post as an extra safety valve against
# repeatedly tweeting the same stale link.)
#
# Expects each blog to be a separate YAML document of the form:
# ---
# owner: '@handle_1
# feed_url: 'http://awesomeblog.com/path/to/feed'
# ---
# owner: '@handle_2'
# feed_url: 'http://otherawesomeblog.com/path/to/another/feed/'
# ... 
#
# Firebase records have sanitized urls as keys and contain
# data about the owner, feed url, and last modification:
# httpawesomeblogcompathtofeed
#     |
#     +-- etag: "\"a762a25c-f561-4ba1-b1db-02816c06e5b0\""
#     |
#     +-- modified: "Wed, 06 Jan 2016 16:21:20 GMT"
#     |
#     +-- owner: '@handle_1'
#     |
#     +-- url: 'http://awesomeblog.com/path/to/feed'
#     |
#     +-- link: 'http://awesomeblog.com/posts/2016/4'

import feedparser
import yaml
import re
from os import path
from firebase import firebase
from strongetags import stripweak
from config import (FIREBASE_URL,
                    FIREBASE_SECRET)

annoying_punctuation = re.compile(r'[/.:?=]')

def loadblogs(filename):
    """
    Fetch the blogroll from a YAML file

    Return a dictionary generator
    """

    stream = file(filename, 'r')
    data = yaml.load_all(stream)
    return data


def sanitize_url(urlstring):
    """
    Return a string representation of a url without punctuation
    """

    # A blog's url is the best unique identifier for the data store
    # (some Twitter handles have more than one blog), but certain
    # punctuation in a string throws an error in Firebase when
    # you attempt to use that string as a key.
    return annoying_punctuation.sub('', urlstring)


def update_firebase():
    """
    Update the Firebase store from blogroll.yaml

    Add any blogs in the YAML file that aren't already
    in the Firebase store, along with its owner and the
    latest ETag or Last-Modified data from the feed.
    """

    # Firebase instance and auth param
    fb = firebase.FirebaseApplication(FIREBASE_URL, None)
    auth = {'auth': FIREBASE_SECRET}

    # Current blogroll.yaml and FB store
    yamlpath = path.join(path.dirname(__file__), '..', 'blogroll.yaml')
    blogroll = loadblogs(yamlpath)
    fb_store = fb.get('blogs/', None, params=auth)
    updates = 0

    print 'Migrating to database...'

    # Check the blogroll against Firebase
    for blog in blogroll:
        url = blog['feed_url']
        clean_url = sanitize_url(url)
        if not fb_store:
            fb_store = {'blogs': None}
        if not clean_url in fb_store:
            feed_data = feedparser.parse(url)
            if not feed_data.bozo: # Ignore malformed XML
                print 'Adding %s to the database.' % url
                updates += 1
                modified = feed_data.get('modified')
                etag = feed_data.get('etag')
                normalized_tag = None
                if etag is not None:
                    normalized_tag = stripweak(etag)

                fb_store[clean_url] = {
                    'owner': blog['owner'],
                    'modified': modified,
                    'etag': normalized_tag,
                    'url': url,
                    'latest_link': feed_data.entries[0].get('link')
                }

    # Actually push updates to Firebase
    if updates:
        fb.patch('blogs/', fb_store, params=auth)
        print 'Updated %d records.' % updates

if __name__ == '__main__':
    update_firebase()
