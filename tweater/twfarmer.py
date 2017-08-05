import requests
import sys
from tworder import TwOrder as order


class TwFarmer:
    @staticmethod
    def ripStatusPage(cursor, cookiesJar):
        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&l=en&max_position=%s"
        parUrl = ''
        if 'user' not in order.conf and 'query' not in order.conf:
            raise ValueError("User and Query, at least one of them must be specified.")
        else:
            if 'query' in order.conf and len(order.conf['query'].strip()) > 0:
                parUrl += order.conf['query']
            if 'user' in order.conf and len(order.conf['user'].strip()) > 0:
                parUrl += ' from:' + order.conf['user']
            if 'until' in order.conf and len(order.conf['until'].strip()) > 0:
                parUrl += ' until:' + order.conf['until']
            if 'since' in order.conf and len(order.conf['since'].strip()) > 0:
                parUrl += ' since:' + order.conf['since']
        url = url % (parUrl, cursor)

        headers = {
            'Host': 'twitter.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
            'Accept-Language': "en-US,en;q=0.8",
            'X-Requested-With': "XMLHttpRequest",
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Connection': "keep-alive"
        }
        try:
            r = requests.get(url, headers=headers, cookies=cookiesJar)
            return r.json()
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)

    @staticmethod
    def ripCommentPage(user_name, tweet_id, cursor, cookiesJar):
        url = "https://twitter.com/i/%s/conversation/%s?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false"
        url = url % (user_name, tweet_id, cursor)
        headers = {
            'Host': 'twitter.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
            'Accept-Language': "en-US,en;q=0.8",
            'X-Requested-With': "XMLHttpRequest",
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Connection': "keep-alive"
        }
        try:
            r = requests.get(url, headers=headers, cookies=cookiesJar)
            return r.json()
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)
