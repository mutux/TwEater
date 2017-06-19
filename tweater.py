import requests
import json
import sys
from datetime import datetime
from pyquery import PyQuery


class TwEater:
    def __init__(self, *args, **kwargs):
        self.conf = {}
        if len(args) == 1:
            confN = args[0]
            # print confN
            with open(confN, 'r') as f:
                self.conf = json.load(f)
        else:
            if 'user' in kwargs:
                self.conf['user'] = kwargs['user']
            if 'query' in kwargs:
                self.conf['query'] = kwargs['query']
            if 'since' in kwargs:
                self.conf['since'] = kwargs['since']
            if 'until' in kwargs:
                self.conf['until'] = kwargs['until']
            if 'max_tweets' in kwargs:
                self.conf['max_tweets'] = kwargs['max_tweets']
            if 'max_comments' in kwargs:
                self.conf['max_comments'] = kwargs['max_comments']
            if 'bufferlength' in kwargs:
                self.conf['bufferlength'] = kwargs['bufferlength']
        # print self.conf

    def eatTweets(self, digester, bpargs):
        # Set default values of parameters.
        max_tweets = 100
        bufferlength = 1000
        if 'max_tweets' in self.conf:
            max_tweets = self.conf['max_tweets']
        if 'bufferlength' in self.conf:
            bufferlength = self.conf['bufferlength']
        total = 0
        bufferTotal = 0
        bufferall = 0

        cursor = ''
        buffer_tweets = []
        cookiejar = requests.cookies.RequestsCookieJar()
        has_more = True
        # print has_more is True

        while has_more is True and total < max_tweets:
            page = self.ripStatusPage(cursor, cookiejar)
            # print done
            cnt_c, has_more, cursor, page_tweets = self.cookPage(page, isComment=False)
            # print len(page_tweets)
            total += len(page_tweets)
            buffer_tweets.extend(page_tweets)

            bufferTotal += cnt_c + len(page_tweets)
            if digester and bufferTotal >= bufferlength:
                bufferall += bufferTotal
                digester(buffer_tweets, bpargs)
                print ' Total tweets: ' + str(total) + ', this time tweets: ' + str(len(buffer_tweets)) + '.\n Total items: ' + str(bufferall) + ', this time items: ' + str(bufferTotal) + '.\n'
                buffer_tweets = []
                bufferTotal = 0
            # print has_more is True
        # print total
        if digester and bufferTotal > 0:
            bufferall += bufferTotal
            digester(buffer_tweets, bpargs)
            print ' Total tweets: ' + str(total) + ', this time tweets: ' + str(len(buffer_tweets)) + '.\n Total items: ' + str(bufferall) + ', this time items: ' + str(bufferTotal) + '.\n'
            buffer_tweets = []
            buffer_tweets = []
            bufferTotal = 0
        return total

    def eatComments(self, user_name, tweet_id):
        max_comments = 100
        if 'max_comments' in self.conf:
            max_comments = self.conf['max_comments']

        cnt_c = 0
        cursor = ''
        cookiejar = requests.cookies.RequestsCookieJar()
        total = 0
        has_more = True
        comments = []
        while has_more is True and total < max_comments:
            page = self.ripCommentPage(user_name, tweet_id, cursor, cookiejar)
            # print page
            cnt_cp, has_more, cursor, pageTweets = self.cookPage(page, isComment=True)
            comments.extend(pageTweets)
            total += len(pageTweets)
            cnt_c += cnt_cp
        # print has_more is True
        # print pageTweets
        # cnt_c should be 0
        return cnt_c, comments

    def cookPage(self, page, isComment=False):
        cursor = ''
        items = []
        # cnt_cp: Number of comments implies by this page
        # if this page is comment page, no 2-order comments will be retured
        # that means cnt_cp = 0
        cnt_cp = 0
        has_more = False
        if len(page['items_html'].strip()) == 0:
            return cnt_cp, has_more, cursor, items
        has_more = page['has_more_items']
        cursor = page['min_position']
        tweets = PyQuery(page['items_html'])('div.js-stream-tweet')
        if len(tweets) == 0:
            return cnt_cp, has_more, cursor, items
        for tweetArea in tweets:
            tweet_pq = PyQuery(tweetArea)
            cnt_c, twe = self.cookTweet(tweet_pq, isComment)
            items.append(twe)
            cnt_cp += cnt_c
        return cnt_cp, has_more, cursor, items

    def cookTweet(self, tweetq, isComment=False):
        """
        "" Read the document, and parse it with PyQuery
        """
        # Number of Comments needs to be pass back
        # Number of Tweets is 1, don't need to be pass back
        # Will return number of comments, and the tweet itself
        cnt_c = 0
        twe = {}
        twe["user"] = tweetq.attr("data-screen-name")

        # Process attributes of a tweet div
        twe["replies"] = int(tweetq("span.ProfileTweet-action--reply span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
        twe["retweets"] = int(tweetq("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
        twe["favorites"] = int(tweetq("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
        twe['timestamp'] = int(tweetq("small.time span.js-short-timestamp").attr("data-time"))
        twe["date"] = datetime.fromtimestamp(twe['timestamp']).strftime("%Y-%m-%d %H:%M")
        twe["id"] = tweetq.attr("data-tweet-id")
        twe["permalink"] = "https://twitter.com" + tweetq.attr("data-permalink-path")

        # Process text area of a tweet div
        textdiv = tweetq("p.js-tweet-text")

        # Process links in a tweet div, including url, hashtags, and mentions contained in the tweet
        links = textdiv('a')
        # print 'HTML: ' + textdiv.html().encode('utf-8')
        if len(links) > 0:
            hashtags = []
            mentions = []
            for link in links:
                # print PyQuery(link)
                textUrl = PyQuery(link).attr('data-expanded-url')
                textHashtag = PyQuery(link)('a.twitter-hashtag')('b')
                if len(textHashtag) > 0:
                    hashtags.append('#' + textHashtag.text().encode('utf-8'))
                textMention = PyQuery(link)('a.twitter-atreply')('b')
                if len(textMention) > 0:
                    mentions.append('@' + PyQuery(textMention).text().encode('utf-8'))
            twe['textUrl'] = ''
            if textUrl is not None:
                twe['textUrl'] = textUrl
            twe['hashtags'] = hashtags
            twe['mentions'] = mentions

        # Process Emojis in a tweet Div
        emojis = textdiv('img.Emoji--forText')
        emojilist = []
        if len(emojis) > 0:
            for emo in emojis:
                textEmoji = PyQuery(emo)
                # print textEmoji
                if textEmoji is not None:
                    emoji = {}
                    emoji['face'] = textEmoji.attr('alt').encode('utf-8')
                    emoji['url'] = textEmoji.attr('src').encode('utf-8')
                    emoji['title'] = textEmoji.attr('title').encode('utf-8')
                    emojilist.append(emoji)
        twe['emojis'] = emojilist

        # Process Text in a tweet Div
        textq = textdiv.remove('a').remove('img')
        if textq is not None:
            twe["text"] = textq.text().encode('utf-8')
            # print twe["text"]

        # Process optional Geo area of a tweet
        twe["geo"] = ''
        geoArea = tweetq('span.Tweet-geo')
        if len(geoArea) > 0:
            twe["geo"] = geoArea.attr('title')

        # Process comments area if any
        if not isComment and twe['replies'] > 0:
            cn, twe['comments'] = self.eatComments(twe['user'], twe['id'])
            cnt_c = len(twe['comments'])

        # Finally return a json of a tweet
        # print twe
        return cnt_c, twe

    def ripStatusPage(self, cursor, cookiesJar):
        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&l=en&max_position=%s"
        parUrl = ''
        if 'user' not in self.conf and 'query' not in self.conf:
            raise ValueError("User and Query, at least one of them must be specified.")
        else:
            if 'query' in self.conf and len(self.conf['query'].strip()) > 0:
                parUrl += self.conf['query']
            if 'user' in self.conf and len(self.conf['user'].strip()) > 0:
                parUrl += ' from:' + self.conf['user']
            if 'until' in self.conf and len(self.conf['until'].strip()) > 0:
                parUrl += ' until:' + self.conf['until']
            if 'since' in self.conf and len(self.conf['since'].strip()) > 0:
                parUrl += ' since:' + self.conf['since']
        url = url % (parUrl, cursor)
        # print url

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept-Language': "en-US,en;q=0.8",
            'X-Requested-With': "XMLHttpRequest",
        }
        try:
            r = requests.get(url, headers=headers, cookies=cookiesJar)
            return r.json()
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)

    def ripCommentPage(self, user_name, tweet_id, cursor, cookiesJar):
        url = "https://twitter.com/i/%s/conversation/%s?include_available_features=1&include_entities=1&l=en&max_position=%s&reset_error_state=false"
        # print url % (user_name, tweet_id, cursor)
        url = url % (user_name, tweet_id, cursor)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept-Language': "en-US,en;q=0.8",
            'X-Requested-With': "XMLHttpRequest",
        }
        try:
            r = requests.get(url, headers=headers, cookies=cookiesJar)
            return r.json()
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)
