from TwitterSearch import *
from string import ascii_letters
import csv
import math
from decimal import *
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError
import json
import sys
import gmplot
import os


def drawMap(d):
    out_dir = "."
    latitutes = [entry[0] for entry in d]
    longitudes = [entry[1] for entry in d]
  
    out_file = os.path.join(out_dir, 'map.html')
    
    gmap = gmplot.GoogleMapPlotter(d.keys()[2][0], d.keys()[2][1], 19)
    
    for key in d.keys():
        color = getColorSentiment(d[key])
        gmap.marker(key[0], key[1], color)


    out_file = os.path.join(out_dir, 'map.html')
    print('Saving [map.html]')
    gmap.draw(out_file)

def getColorSentiment(value):
    #colorize based on sentiment value
    if value >= 0.5:
        return 'blue'
    elif value < 0.5 and value >= 0.25:
        return 'cornflowerblue'
    elif value < 0.25 and value > 0:
        return 'lightblue'
    elif value == 0:
        return 'gray'
    elif value < 0 and value >= -0.25:
        return 'tomato'
    elif value < -0.25 and value >= -0.5:
        return 'r'
    else: 
        return "darkred" 


geolocator = Nominatim()

def load_sentiments():
        """Read the sentiment file and return a dictionary containing the sentiment
        score of each word, a value from -1 to +1.
        """

        with open('./sentiments_better.csv') as sentiment_file:
              scores = [line.split(',') for line in sentiment_file]
              return {word: float(score.strip()) for word, score in scores}

word_sentiments = load_sentiments()

def extract_words(text):
    """Return the words in a tweet, not including punctuation.
    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
    ['cat', 'on', 'my', 'keyboard']
    """
    words = ''
    for i in text: #goes through every character in operand 'text' 
    #and created a list with only words and spaces by adding the letter if 
    #ascii letter to the list, and a space if not
        if i in ascii_letters:
            words += i
        else:
            words += ' '
    return words.split()
    #returns a list containing only the words, as it splits the existing list by blank space, 
        #which leaves only the collection of letters in their respective words

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.
    """
    assert value is not None and (value >= -1 and value <= 1), 'Illegal sentiment value: ' + str(value)
    return value

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    return s != None

def sentiment_value(s): #version of has sentiment that returns the value rather 
#than true or false with the same intended effect
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    return s


def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.
    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    # assert word in word_sentiments, "word not in dict: " + word
    if word not in word_sentiments:
        return make_sentiment(0)
    return make_sentiment(word_sentiments.get(word))


def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.
    If no words in the tweet have a sentiment value, return
    make_sentiment(None).
    >>> t1 = trends.make_tweet("Help, I'm trapped in an autograder factory and I can't get out!".lower(), None, 0, 0)
    >>> t2 = trends.make_tweet('The thing that I love about hating things that I love is that I hate loving that I hate doing it.'.lower(), None, 0, 0)
    >>> t3 = trends.make_tweet('Peter Piper picked a peck of pickled peppers'.lower(), None, 0, 0)
    >>> round(trends.sentiment_value(analyze_tweet_sentiment(t1)), 5)
    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet("berkeley golden bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    tweet = tweet.lower()
    # sent_list = list(sentiment_value(get_word_sentiment(word)) for word in extract_words(tweet) if has_sentiment(get_word_sentiment(word))) 

    sent_list = []

    for word in extract_words(tweet):
        if has_sentiment(get_word_sentiment(word)):
            sent_val = sentiment_value(get_word_sentiment(word))
            sent_list.append(sent_val)
            # print(word + str(sent_val))

    #creates a list of the sentiments for each word in the tweet that has a sentiment all of the words
    if not sent_list: 
    #if the list is empty (no word in the tweet had sentiments) then return a sentiment of None
        print("sentiment is 0")
        return make_sentiment(0)

    total = sum(sent_list)
    length = len(sent_list)
    return make_sentiment(total / length) 
    #returns sentiment for entire tweet by averaging the values in the list 
    #(or the sentiments of the words in the tweet that had sentiments)


def tweet_words(tweet):
    """Return the words in a tweet."""
    return extract_words(tweet_text(tweet))

def mean(numbers):
    return (sum(numbers)) / max(len(numbers), 1)


def get_location(location_str):

    try:
        # print("get_location: " + location_str)
        location = geolocator.geocode(location_str)
        # print(location)
        str(location)
        repr(location)
        if location_str is not None and location_str != '' \
            and location is not None \
            and location.address is not None:
                return location
        return None
    except UnicodeEncodeError as e:
        print("failed")
        return None
    except GeocoderTimedOut as error_msg:
        print ("failed: timeout")
        return None

    except GeocoderServiceError as error_msg:
        print ("failed: service error")
        return None   


def get_tweets(twitter_info, topic_string): #make this have a parameter that accepts any topic!
    assert consumer_key in twitter_info and consumer_secret in twitter_info \
            and access_token in twitter_info and access_token_secret in twitter_info, "Empty Twitter API info"
    assert topic_string != None and topic_string != '', "Empty string"

    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords([topic_string]) # let's define all words we would like to have a look for
        tso.set_language('en') # we want to see English tweets only
        tso.set_include_entities(False) # and don't give us all those entity information

        

        ts = TwitterSearch(
            consumer_key = twitter_info["consumer_key"],
            consumer_secret = twitter_info["consumer_secret"],
            access_token = twitter_info["access_token"],
            access_token_secret = twitter_info["access_token_secret"]
         )
        tweet_search = [tweet for tweet in ts.search_tweets_iterable(tso)]
        print("e")
        return tweet_search

    except TwitterSearchException as e:
        print(e)
        return []

coord_sent_dict = {}


def generate_map(twitter_info, topic_string):

    #start of code

    i = 1
    verified_pos_count = 1
    for tweet in get_tweets(twitter_info, topic_string): 

        text = tweet['text']
        print(text)
        city = tweet['user']['location']
        print(city)
        
        print("processing tweet #" + str(i))
        i = i + 1

        if i > 500:
            break
        
        loc = get_location(city)

        if loc == None:
            continue

        if "United States of America" not in loc.address:
            print("this location is not in America")
            continue

        if verified_pos_count > 50:
            break
        
        sent_value = analyze_tweet_sentiment(text)

        #have an if statement here to filter out the non-US states, do i nest everything?

        print(loc)
        print(sent_value)
        print("verified location within US")
        verified_pos_count = verified_pos_count + 1
        coord_tuple = (loc.latitude, loc.longitude)
        print(loc.latitude)
        print(loc.longitude)



        #this is COORD - SENT VALUE

        """if the dictionary does already contain this key, average this sent val combo"""    
        if coord_tuple in coord_sent_dict:
            coord_sent_dict[coord_tuple].append(sent_value)


        else:    
            """if the dictionary doesn't already contain this key, insert this coord/sent val combo"""
            coord_sent_dict[coord_tuple] = [sent_value]    


    avgDict_2 = {}
    for k,v in coord_sent_dict.iteritems():
        avgDict_2[k] = sum(v)/ float(len(v))    



    negative_counts_2 = 0
    for k,v in avgDict_2.iteritems():
        if v < 0:
            negative_counts_2 = negative_counts_2 + 1
        else:
            continue

    dict_len_2 = len(avgDict_2)

    percentage_neg = float(negative_counts_2) / float(dict_len_2)

    print("percentage that are negative sentiments overall: " + str(percentage_neg))
    print(avgDict_2)
    drawMap(avgDict_2)
