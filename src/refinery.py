import nltk
import json
import twython
import sys
import os
import itertools
import nltk
from nltk.tokenize import TweetTokenizer
import re

def get_json_from_file(filepath,count=None):
    tweet_list=[]
    with open(filepath,"r") as fp:
        if count is None:
            while True:
                line = fp.readline()
                if line == "":
                    break;
                tweet_list.append(json.loads(line))
            return tweet_list
        for i in range(count):
            line = fp.readline()
            if line is not "":
                tweet_list.append(json.loads(fp.readline()))
            else:
                break
    return tweet_list

def get_text_from_tweets(tweets):
    tweets_text = []
    tweets_flattened = itertools.chain.from_iterable(tweets)
    for tweet in tweets_flattened:
        tweets_text.append(tweet['text'])
    return tweets_text

def clean_tweets_text(tweets_text):
    # remvoe digits and special characters
    tweets_without_digits= map(lambda expr:re.sub('\d|#|@|%|$|_|\?','',expr),tweets_text)
    tweets_period_adjust = map(lambda expr:re.sub('\.','. ',expr),tweets_without_digits)
    tweets_small_case = map(lambda expr:expr.lower(),tweets_period_adjust)
    clean_tweets = []
    for tweet in tweets_small_case:
        #removes URL from tweets
        #gap has been introduced after 'pic.' to settle for the space introduced after tweets_period_adjust 
        idx = re.search('http|fb.|pic. twitter', tweet, flags=0)
        if idx == None:
            clean_tweets.append(tweet)
        else:
            #the tweet is truncated from the beginning of the url
            clean_tweets.append(tweet[:idx.start()])
    return clean_tweets

def print_tweets(tweets):
    for i,tweet in enumerate(clean_tweets):
        print(i,": ",tweet)

def get_clean_tweets(filepath):
    tweets = get_json_from_file(filepath)
    tweets_text = get_text_from_tweets(tweets)
    clean_tweets = clean_tweets_text(tweets_text)
    return clean_tweets
