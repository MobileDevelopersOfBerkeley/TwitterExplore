from TwitterSearch import *
try:

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['Ivanka', 'Trump']) # let's define all words we would like to have a look for
    tso.set_language('en') # we want to see English tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'bxWIlmDDU7FeYohLgTaQ9BVI2',
        consumer_secret = 'TZNru9ij7gRtziFDWhoSNsdnhmJpI8El02Oq6hp0qV9PnagVnE',
        access_token = '1649068904-To4mRkvhkRJ1XNhOXHwjmPPRO0vjY0vy3lB6h7n',
        access_token_secret = 'Ssao2gBZxCojcvvFJkrZUffTMBK9e5rrJY6J7eXNvaUJN'
     )

     # this is where the fun actually starts :)
    coordinates = []
    for tweet in ts.search_tweets_iterable(tso):
        # print(tweet)
        # break
        # if type(tweet["geo"]["coordinates"]) is NoneType:
        #     continue

        # print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) ) 
        # lat = tweet["geo"]["coordinates"][0]
        # lon = tweet["geo"]["coordinates"][1]
        # print("Tweet's latitude: " + lat)
        # print("Tweet's longitude: " + lon)
        # break
        if tweet['geo']:
            print "longitude = " + tweet["geo"]["coordinates"][1]
        else:
            print("didn't print geo")

        break


except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)