
Conducts a sentiment analysis of a topic string using tweets from Twitter.
Generates a map of the US that color codes these sentiments.

Example of how to use this package:

$ python -i api_call.py
>>> d = {'consumer_key' : 'INSERT CONSUMER KEY',
            'consumer_secret' : 'INSERT CONSUMER SECRET',
            'access_token' : 'INSERT ACCESS TOKEN',
            'access_token_secret' : 'INSERT TOKEN SECRET'}
>>> generate_map(d, "Trump")
...

Saving [map.html]


Now you should open the map.html in your browser and enjoy the marker map!
