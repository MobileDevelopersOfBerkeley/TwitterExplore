#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-search-geo
#  - performs a search for tweets close to New Cross, and outputs
#    them to a CSV file.
#-----------------------------------------------------------------------

from twitter import *

import sys
import csv

latitude = 37.8719	# geographical centre of search
longitude = 122.2585	# geographical centre of search
max_range = 10 			# search range in kilometres
num_results = 500		# minimum results to obtain
# outfile = "output.csv"

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {
	'consumer_key':'bxWIlmDDU7FeYohLgTaQ9BVI2',

    'consumer_secret' : 'TZNru9ij7gRtziFDWhoSNsdnhmJpI8El02Oq6hp0qV9PnagVnE', 
    'access_token_key' :'1649068904-To4mRkvhkRJ1XNhOXHwjmPPRO0vjY0vy3lB6h7n', 
    'access_token_secret':'Ssao2gBZxCojcvvFJkrZUffTMBK9e5rrJY6J7eXNvaUJN'
}
# execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		        auth = OAuth(config['access_token_key'], 
		        	config['access_token_secret'], 
		        	config['consumer_key'], 
		        	config['consumer_secret'])
		        )


# api = twitter.Api(consumer_key='bxWIlmDDU7FeYohLgTaQ9BVI2',

#     consumer_secret='TZNru9ij7gRtziFDWhoSNsdnhmJpI8El02Oq6hp0qV9PnagVnE', 
#     access_token_key='1649068904-To4mRkvhkRJ1XNhOXHwjmPPRO0vjY0vy3lB6h7n', 
#     access_token_secret='Ssao2gBZxCojcvvFJkrZUffTMBK9e5rrJY6J7eXNvaUJN')


#-----------------------------------------------------------------------
# open a file to write (mode "w"), and create a CSV writer object
#-----------------------------------------------------------------------
# csvfile = file(outfile, "w")
# csvwriter = csv.writer(csvfile)

#-----------------------------------------------------------------------
# add headings to our CSV file
#-----------------------------------------------------------------------
row = [ "user", "text", "latitude", "longitude" ]
# csvwriter.writerow(row)

#-----------------------------------------------------------------------
# the twitter API only allows us to query up to 100 tweets at a time.
# to search for more, we will break our search up into 10 "pages", each
# of which will include 100 matching tweets.
#-----------------------------------------------------------------------
result_count = 0
last_id = None
while result_count <  num_results:
	#-----------------------------------------------------------------------
	# perform a search based on latitude and longitude
	# twitter API docs: https://dev.twitter.com/docs/api/1/get/search
	#-----------------------------------------------------------------------
	query = twitter.search.tweets(q = "", geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count = 100, max_id = last_id)

	for result in query["statuses"]:
		#-----------------------------------------------------------------------
		# only process a result if it has a geolocation
		#-----------------------------------------------------------------------
		if result["geo"]:
			user = result["user"]["screen_name"]
			text = result["text"]
			text = text.encode('ascii', 'replace')
			latitude = result["geo"]["coordinates"][0]
			longitude = result["geo"]["coordinates"][1]

			# now write this row to our CSV file
			row = [ user, text, latitude, longitude ]
			print("Lat: " + str(latitude))
			print("Long: " + str(longitude))
			# csvwriter.writerow(row)
			result_count += 1
		last_id = result["id"]

	#-----------------------------------------------------------------------
	# let the user know where we're up to
	#-----------------------------------------------------------------------
	print "got %d results" % result_count
	break

#-----------------------------------------------------------------------
# we're all finished, clean up and go home.
#-----------------------------------------------------------------------
# csvfile.close()

# print "written to %s" % outfile