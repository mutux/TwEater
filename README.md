# TwEater
A Python way to collect **MORE** Tweets and their **REPLIES** from Twitter than the official API.
Currently only **Python 2.7.x** is supported.

The motivation is to collect tweets for **Text Mining** or NLP tasks, such as message understanding, talking bot, opinion Mining, information extraction, event detection & tracking, tweet ranking, and so on.

Therefore, not only the tweet text and basic attributes, but also **conversations**, **emojis**, links, mentions, hashtags are all necessary to be able to collected by it.

Also, official API imposes limits on time and amount of the tweets you can collect, try TwEater!

## Examples
Look into the **eater.py**, it's a simple example of using this bot.
First, you need place your order either by a configuration file, or by **K=V** parameters:
```
TwOrder.order('order.conf')
```
Or
```
TwOrder.order(user='BarackObama')
```
Two methods **digest_2_file** and **digest_2_mongo** are provided to process data after collecting them, either store them in a file or in a MongoDB, or even process them on the fly, it's up to you. You can define **your own** processing function.

Then, go harvest tweets together with replies (emojis are also collected, very important for sentiment analysis):
```
TwEater.eatTweets(digest_2_file, 'test')
```
If you just want get the replies of someone's `username` some tweet `tweet_id`, this will return a json array.
```
print TwChef.shopComments('BarackObama', '876456804305252353')
```

## Parameters
The example values for the 9 parameters is as follows, which can be seen from file `order.conf`:
```
    {
      "user": "",
      "query": "calorie OR eat",
      "since": "2017-06-10",
      "until": "2017-07-19",
      "max_tweets": 10,
      "max_comments": 0,
      "bufferlength": 100,
      "near": "Montréal, Québec",
      "within": "5km",
      "lang": "en"
    }
```

#### Note:
**`user` and `query`, at least one of them must be specified.**
  - `user`: specifies which user you want collect, **default ""**
  - `query`: either a keyword or a hashtag you care about, **default ""**
  - `since`: the start time of the tweets you want, **default ""**
  - `until`: the end time of the tweets you want, **default ""**
  - `max_tweets`: how many tweets you want collect for this query and/or user, **default 1**
  - `max_comment`: how many replies you want for each tweet if there is any, **default 1**
  - `bufferlength`: process and clear the data in a reasonably sized batch before you run out of memory, **default 100**
  - `near`: a location where the tweets are posted do you need, **default ""**.
  - `within`: has to be used together with `near`, specifying the radius of the location, **default ""**.
  - `lang`: specify the language of the tweets you need, only English and French are suppored at the moment, **default "en"**.

## [MuTuX](http://www.mutux.com "MuTux's Home")
For the benefits of learners or researchers, don't abuse it!
Have fun!
