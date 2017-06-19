from tweater import TwEater
# from pymongo import MongoClient
from datetime import datetime
import json


# Write tweets to file
def t2f(tweets, file):
    print ' ------ Saved to file: ' + file + ' * Stats * ------'
    with open(file, 'w+') as f:
        json.dump(tweets, f)


# Write file to MongoDB collection
def t2m(tweets, col):
    print ' ------ Save to MongoDB * Stats * ------'
    col.insert_many(tweets)


if __name__ == "__main__":
    print "\n " + unicode(datetime.now())
    # Initialize a eator with parameters
    me = TwEater('tweater.conf')
    # me = TwEater(user='barackobama')

    # Collect comments of specific tweet_id fo user
    # print me.eatComments('barackobama', '876456804305252353')

    # Write tweets to json file
    me.eatTweets(t2f, 'eater.json')

    # Write tweets to Mongo Collection
    # client = MongoClient()
    # me.eatTweets(t2m, client.test.tweets)

    print " " + unicode(datetime.now())
    print " Done!"
