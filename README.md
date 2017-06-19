# TwEater
A Python way to collect **MORE** Tweets and their **REPLIES** from Twitter than the official API.

The motivation is to collect tweets for **Text Mining** or NLP tasks, such as message understanding, talking bot, opinion Mining, information extraction, event detection & tracking, tweet ranking, and so on.

Therefore, not only the tweet text and basic attributes, but also **conversations**, **emojis**, links, mentions, hashtags are all necessary to be able to collected by it.

Also, official API imposes limits on time and amount of the tweets you can collect, but TwEater does not!

## Examples
You can create an instance with arbituray number of **K=V** parameters:
```
me = TwEater(user='barackobama')
```
You can also create an instance with a configuration **file** (an example configuration file is provided)
```
me = TwEater('tweater.conf')
```
Two methods **t2f** and **t2m** are provided to process data after collecting them, either store them in a file or in a MongoDB, or even process them on the fly, it's up to you. You can define **your own** processing function.

Then, go harvest tweets together with replies (emojis are also collected, very important for sentiment analysis):
```
me.eatTweets(t2f, 'out.json')
```
If you just want get the replies of someone's `username` some tweet `tweet_id`, this will return a json array.
```
print me.eatComments('barackobama', '876456804305252353')
```

## Parameters
The example values for the 7 parameters:
```
    user=""
    query="Father's day"
    since="2017-06-18"
    until="2017-06-19"
    max_tweets=100
    max_comments=50
    bufferlength=500
```

#### Note:
**`user` and `query`, at least one of them must be specified.**
  - `user`: specifies which user you want collect
  - `query`: either a keyword or a hashtag you care about
  - `since`: the start time of the tweets you want, default ""
  - `until`: the end time of the tweets you want, default ""
  - `max_tweets`: how many tweets you want collect for this query and/or user, default 100.
  - `max_comment`: how many replies you want for each tweet if there is any, default 10.
  - `bufferlength`: process and clear the data in a reasonable sized batch before you run out of memory, default 100.

## Finally
Kindly keep in mind: 'Please, don't abuse it, for the benefit of learners or researchers!'
Have fun!
