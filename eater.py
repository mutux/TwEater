from tworder import TwOrder
from tweater import TwEater
# from twchef import TwChef
# from pymongo import MongoClient
from datetime import datetime
import json


# Write tweets batch to a file in folder dir
def digest_2_file(tweets, dir):
    t = datetime.now()
    fn = dir + '/' + str(t.microsecond + (t.second + t.day * 86400) * 10**6) + '.json'
    print ' ------ Saved to file: ' + fn + ' ------'
    with open(fn, 'w') as f:
        json.dump(tweets, f)


# Write file to MongoDB collection
def digest_2_mongo(tweets, col):
    print ' ------ Save to MongoDB ------'
    col.insert_many(tweets)


if __name__ == "__main__":
    print "\n " + unicode(datetime.now())
    # Initialize the parameters
    TwOrder.order('tworder.conf')
    # TwOrder.order(user='BarackObama')

    # Write tweets to json file
    TwEater.eatTweets(digest_2_file, 'out')

    # Collect replies of specific tweet_id of a user, username is case-sensitive
    # print TwChef.shopComments('BarackObama', '876456804305252353')

    # Write tweets to Mongo Collection
    # client = MongoClient()
    # TwEater.eatTweets(digest_2_mongo, client.test.tweets)

    print " " + unicode(datetime.now())
    print " Done!"
