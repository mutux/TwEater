# -*- coding: utf-8 -*-
import requests
from tworder import TwOrder as order


class TwFarmer:
    @staticmethod
    def ripStatusPage(cursor, sess):
        lang = 'en'
        parUrl = ''
        if 'user' not in order.conf and 'query' not in order.conf:
            raise ValueError("User and Query, at least one of them must be specified.")
        else:
            if 'query' in order.conf and len(order.conf['query'].strip()) > 0:
                parUrl += " " + order.conf['query']
            if 'user' in order.conf and len(order.conf['user'].strip()) > 0:
                parUrl += ' from:' + order.conf['user'].encode('utf-8')
            if 'until' in order.conf and len(order.conf['until'].strip()) > 0:
                parUrl += ' until:' + order.conf['until']
            if 'since' in order.conf and len(order.conf['since'].strip()) > 0:
                parUrl += ' since:' + order.conf['since']
            if 'near' in order.conf and len(order.conf['near'].strip()) > 0:
                if 'within' in order.conf and len(order.conf['within'].strip()) > 0:
                    parUrl += " near:\"" + order.conf['near'].encode('utf-8') + "\" within:" + order.conf['within']
            if 'lang' in order.conf and len(order.conf['lang'].strip()) > 0:
                lang = order.conf['lang'].strip()
        # print parUrl
        # print cursor

        # english
        headers_en = {
            'User-Agent': 'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00',
            'Accept-Language': "en-CA,en;q=0.8",
            'X-Requested-With': "XMLHttpRequest"
        }

        # french
        headers_fr = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept-Language': "fr-CA,fr;q=0.8",
            'X-Requested-With': "XMLHttpRequest"
        }

        # english
        url_en = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&l=en&max_position=%s"

        # french
        url_fr = u"https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&l=fr&max_position=%s"
        if lang == 'fr':
            url = url_fr
            headers = headers_fr
        else:
            url = url_en
            headers = headers_en
        # print url
        url = url % (parUrl.decode('utf-8'), cursor)

        try:
            # print unicode(url).encode('utf8')
            r = sess.get(url.encode('utf-8'), headers=headers)
            # print r.url
            # print 'TEXT: -------------------------'
            # print r.text
            # print 'JSON: -------------------------'
            # print r.json()
            # print '-------------------------\n\n\n'
            return r.json()
        except requests.exceptions.RequestException as e:
            print 'url: ', unicode(url).encode('utf8')
            print e

    @staticmethod
    def ripCommentPage(user_name, tweet_id, cursor, sess):
        lang = 'en'
        if 'lang' in order.conf and len(order.conf['lang'].strip()) > 0:
            lang = order.conf['lang'].strip()

        url = "https://twitter.com/i/%s/conversation/%s?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false"
        url = url % (user_name, tweet_id, cursor)
        # english
        headers_en = {
            'User-Agent': 'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00',
            'Accept-Language': "en-CA,en;q=0.8",
            'X-Requested-With': "XMLHttpRequest"
        }

        # french
        headers_fr = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept-Language': "fr-CA,fr;q=0.8",
            'X-Requested-With': "XMLHttpRequest"
        }

        if lang == 'fr':
            headers = headers_fr
        else:
            headers = headers_en

        try:
            r = sess.get(url, headers=headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print 'url: ', url
            print e
