from datetime import datetime
from pyquery import PyQuery
from twfarmer import TwFarmer
from tworder import TwOrder as order
import requests


class TwChef:
    @staticmethod
    def cookPage(page, isComment=False):
        cursor = ''
        items = []
        # cnt_cp: Number of comments implies by this page
        # if this page is comment page, no 2-order comments will be retured
        # that means cnt_cp = 0
        cnt_cp = 0
        has_more = False
        if 'items_html' in page and len(page['items_html'].strip()) == 0:
            return cnt_cp, has_more, cursor, items
        has_more = page['has_more_items']
        cursor = page['min_position']
        tweets = PyQuery(page['items_html'])('div.js-stream-tweet')
        if len(tweets) == 0:
            return cnt_cp, has_more, cursor, items
        for tweetArea in tweets:
            tweet_pq = PyQuery(tweetArea)
            cnt_c, twe = TwChef.cookTweet(tweet_pq, isComment)
            items.append(twe)
            cnt_cp += cnt_c
        return cnt_cp, has_more, cursor, items

    @staticmethod
    def cookTweet(tweetq, isComment=False):
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
        if len(links) > 0:
            hashtags = []
            mentions = []
            for link in links:
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

        # Process optional Geo area of a tweet
        twe["geo"] = ''
        geoArea = tweetq('span.Tweet-geo')
        if len(geoArea) > 0:
            twe["geo"] = geoArea.attr('title')

        # Process comments area if any
        if not isComment and twe['replies'] > 0:
            cn, twe['comments'] = TwChef.shopComments(twe['user'], twe['id'])
            cnt_c = len(twe['comments'])

        # Finally return a json of a tweet
        return cnt_c, twe

    @staticmethod
    def shopComments(user_name, tweet_id):
        max_comments = 1
        if 'max_comments' in order.conf and order.conf['max_comments'] > 0:
            max_comments = order.conf['max_comments']

        cnt_c = 0
        cursor = ''
        cookiejar = requests.cookies.RequestsCookieJar()
        total = 0
        has_more = True
        comments = []
        while has_more is True and total < max_comments:
            page = TwFarmer.ripCommentPage(user_name, tweet_id, cursor, cookiejar)
            cnt_cp, has_more, cursor, pageTweets = TwChef.cookPage(page, isComment=True)
            comments.extend(pageTweets)
            total += len(pageTweets)
            cnt_c += cnt_cp
        # cnt_c should be 0
        return cnt_c, comments
