import requests
from tworder import TwOrder as order
from twchef import TwChef
from twfarmer import TwFarmer


class TwEater:
    @staticmethod
    def eatTweets(digester, bpargs):
        # Set default values of parameters.
        max_tweets = 1
        bufferlength = 100
        if 'max_tweets' in order.conf and order.conf['max_tweets'] > 0:
            max_tweets = order.conf['max_tweets']
        if 'bufferlength' in order.conf and order.conf['bufferlength'] > 0:
            bufferlength = order.conf['bufferlength']
        total = 0
        bufferTotal = 0
        bufferall = 0

        cursor = ''
        buffer_tweets = []
        cookiejar = requests.cookies.RequestsCookieJar()
        has_more = True

        while has_more is True and total < max_tweets:
            page = TwFarmer.ripStatusPage(cursor, cookiejar)
            cnt_c, has_more, cursor, page_tweets = TwChef.cookPage(page, isComment=False)
            total += len(page_tweets)
            buffer_tweets.extend(page_tweets)

            bufferTotal += cnt_c + len(page_tweets)
            if bufferTotal >= bufferlength:
                bufferall += bufferTotal
                digester(buffer_tweets, bpargs)
                print ' Total tweets: ' + str(total) + ', this time tweets: ' + str(len(buffer_tweets)) + '.\n Total items: ' + str(bufferall) + ', this time items: ' + str(bufferTotal) + '.\n'
                buffer_tweets = []
                bufferTotal = 0
        if bufferTotal > 0:
            bufferall += bufferTotal
            digester(buffer_tweets, bpargs)
            print ' Total tweets: ' + str(total) + ', this time tweets: ' + str(len(buffer_tweets)) + '.\n Total items: ' + str(bufferall) + ', this time items: ' + str(bufferTotal) + '.\n'
            buffer_tweets = []
            buffer_tweets = []
            bufferTotal = 0
        return total
