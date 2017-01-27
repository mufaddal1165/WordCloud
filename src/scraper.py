# -- coding: utf-8 --

import requests
import json
from urllib2 import quote
from urllib2 import urlopen
from bs4 import BeautifulSoup
import sys

def fetch_tweets(filename, query):
    query = quote(query.encode('utf-8'), safe='/)(')
    init_url = 'https://twitter.com/search?q={}&src=typd'.format(query)
    loop_url = 'https://twitter.com/i/search/timeline?vertical=default&q={}&src=typd&include_available_features=1&include_entities=1&reset_error_state=false'.format(query)

    headers = {
        'User-Agent': 'Firefox/10.0.1'
    }

    print 'Sending request to {}'.format(init_url)
    body = requests.get(init_url, headers=headers).text
    print 'Success! Parsing response'

    # get initial max id
    soup = BeautifulSoup(body, 'html.parser')
    div = soup.find(attrs = {'data-max-position': True})
    min_id = div['data-max-position']
    next_id = None

    # get tweets
    tweets = parse_tweets(body)
    with open(filename, 'w') as f:
        f.write(json.dumps(tweets) + '\n')

    # loop for further tweets
    while next_id != min_id:
        print 'Making consecutive request...'
        temp = next_id
        next_id = min_id
        try:
            url = loop_url + '&max_position={}'.format(next_id)
            body = requests.get(url, headers=headers).json()
            print 'Parsing.'
            min_id = body[u'min_position']
            html = body[u'items_html']
            new_tweets = parse_tweets(html)
            with open(filename, 'a') as f:
                f.write(json.dumps(new_tweets) + '\n')
            tweets = tweets + new_tweets
            print 'Tweet count: {}'.format(len(tweets))

        except requests.exceptions.RequestException as e:
            print e
            print('Error occurred. Oldest stored tweet: {}\n. Trying again...'.format(min_id))
            next_id = temp


    return len(tweets)


def parse_tweets(string):
    soup = BeautifulSoup(string, 'html.parser')
    tweets = []
    for tweet in soup.select('div.tweet'):
        tweet_text = get_text(tweet)
        if tweet_text is None:
            continue
        author = get_author(tweet)
        (date, timestamp) = get_time(tweet)
        tweets.append({
            'author': author,
            'date': date,
            'timestamp': timestamp,
            'text': tweet_text
        })

    return tweets


def get_text(tweet):
    text_container = tweet.select('p.js-tweet-text')
    if len(text_container) == 0:
        return None
    text_container = text_container[0]
    return " ".join(text_container.stripped_strings)


def get_author(tweet):
    return tweet['data-screen-name']


def get_time(tweet):
    date_container = tweet.select('._timestamp')[0]
    date = date_container.string
    epoch = date_container['data-time']
    return (date, epoch)


if __name__ == '__main__':
    query = sys.argv[1]
    filename = sys.argv[2]
    print 'Total tweets fetched: {}'.format(fetch_tweets(filename, query))
