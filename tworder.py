import json
import sys


class TwOrder:
    # Default Values
    conf = {
        'user': '',
        'query': '',
        'since': '',
        'until': '',
        'max_tweets': 1,
        'max_comments': 1,
        'bufferlength': 100
    }

    @staticmethod
    def order(*args, **kwargs):
        # Using configuration filename parameter
        if len(args) == 1:
            filename = args[0]
            with open(filename, 'r') as f:
                TwOrder.conf = json.load(f)
        # Using KV parameters
        else:
            if 'user' in kwargs:
                TwOrder.conf['user'] = kwargs['user']
            if 'query' in kwargs:
                TwOrder.conf['query'] = kwargs['query']
            if 'since' in kwargs:
                TwOrder.conf['since'] = kwargs['since']
            if 'until' in kwargs:
                TwOrder.conf['until'] = kwargs['until']
            if 'max_tweets' in kwargs:
                TwOrder.conf['max_tweets'] = kwargs['max_tweets']
            if 'max_comments' in kwargs:
                TwOrder.conf['max_comments'] = kwargs['max_comments']
            if 'bufferlength' in kwargs:
                TwOrder.conf['bufferlength'] = kwargs['bufferlength']
        if len(TwOrder.conf['query']) == 0 and len(TwOrder.conf['user']) == 0:
            print "Parameter query and user cannot be empty simutaneously!\nUsage: TwOrder(query=\"Father's Day\")"
            sys.exit(1)
