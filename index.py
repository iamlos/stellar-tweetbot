#!/usr/bin/env python
# CONFIGURATION

BOT_ACCOUNT         = '' # e.g. 'pjan_stellar'
STELLAR_FEED_URL    = '' # e.g. 'http://stellar.io/pjan/flow/feed'

CONSUMER_KEY        = ''
CONSUMER_SECRET     = ''
ACCESS_TOKEN        = ''
ACCESS_TOKEN_SECRET = ''

HISTORY_FILE        = 'history.dat'

RETWEET             = True
TWEET_OTHERS        = False

# THE SCRIPT

import xml.etree.ElementTree as ET
import urllib2
import re
import os

import tweepy


def touchopen(filename, *args, **kwargs):
    open(filename, "a").close() # "touch" file
    return open(filename, *args, **kwargs)


class tweetbot:

    def __init__(self, twitter_key, twitter_secret, username, token, token_secret, feed_url, history_file):
        self.username = username
        self.auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
        self.auth.set_access_token(token, token_secret)
        self.twitter = tweepy.API(self.auth)
        self.feed_url = feed_url
        self.history_file = history_file

    def update(self, retweet=True, tweet=False):
        feed = self._readFeed(self.feed_url)
        links = self._readLinks(feed)
        history = self._readHistory(self.history_file)
        new_links = self._identifyNew(links, history)
        for link in new_links:
            if (retweet and link['source'] == 'twitter'):
                try:
                    self.twitter.retweet(link['tweet_id'])
                except:
                    pass
            elif (tweet):
                try:
                    self.twitter.update_status('%s - %s' % (link['title'], link['href']))
                except:
                    pass
        self._updateHistory(new_links, self.history_file)

    def _readFeed(self, feed_url):
        response = urllib2.urlopen(feed_url)
        feed_string = response.read()
        feed = ET.fromstring(feed_string)
        return feed

    def _readLinks(self, feed):
        entries = feed.findall("{http://www.w3.org/2005/Atom}entry")
        links = []
        for entry in entries:
            href = entry.find("{http://www.w3.org/2005/Atom}link").get('href')
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            m = re.match(r"^.+/twitter.com\/[a-zA-Z0-9_]+\/status\/([0-9]+)", href)
            if (m):
                links.append({'source': 'twitter', 'href': href, 'tweet_id': m.group(1)})
            else:
                links.append({'source': 'other', 'href': href, 'title': title})

        return links

    def _identifyNew(self, links, history):
        new_links = []
        for link in links:
            if not link['href'] in history:
                new_links.append(link)
        return new_links

    def _readHistory(self, history_file):
        handle = touchopen(os.path.abspath(os.path.dirname(__file__)) + '/' + history_file, "r")
        url_list = []
        for line in handle:
            url_list.append(line.rstrip('\n'))
        handle.close()
        return url_list

    def _updateHistory(self, new_links, history_file):
        handle = touchopen(os.path.abspath(os.path.dirname(__file__)) + '/' +  history_file, 'a+')
        for link in new_links:
            handle.write('%s\n' % link['href'])
        handle.close()


# Run the script

tb = tweetbot(CONSUMER_KEY, CONSUMER_SECRET, BOT_ACCOUNT, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, STELLAR_FEED_URL, HISTORY_FILE)
tb.update(RETWEET, TWEET_OTHERS)
