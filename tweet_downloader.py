#!/usr/bin/env python
# encoding: utf-8

# Original code: https://gist.github.com/yanofsky/5436496

import tweepy # https://github.com/tweepy/tweepy
import csv
import sys
import os.path
import datetime
import time

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

# print "tweepy version: %s"%(tweepy.__version__)

def get_tweets(screen_name):

	# Inits
	latest = 1		# Fake start in the very past
	csvtweets = []		# Empty set

	# Define path for CSV files
	csvpath = 'tweets'
	if not os.path.exists(csvpath):
		os.makedirs(csvpath)

	# Define CSV filename
	csvfilename = os.path.join(csvpath, '%s_tweets.csv'%(screen_name))

	# If CSV file already exists, get and append only new tweets
	if os.path.exists(csvfilename):
		print "CSV file found for user: %s"%(screen_name)
		print "Downloading NEW tweets..."

		# Read tweets stored into CSV
		with open(csvfilename, 'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				if row[0] != 'screen_name':
					csvtweets.append(row)
		# Close csvfile
		f.close

		# Get latest tweet_id
		# created_at is on column 4
		# tweet_id   is on column 8
		latest = csvtweets[0][8]
		print "- latest tweet_id of user %s (%s)"%(screen_name, latest)
		print "- written on {}".format(csvtweets[0][4])

	else:
		print "CSV file NOT found for user: %s"%(screen_name)
		print "Downloading ALL tweets...\n"

	# Twitter only allows access to a users
	# most recent 3240 tweets with this method

	# Authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	# Initialize a list to hold all the tweepy Tweets
	alltweets = []

	# Check if we are rate-limited
	rate = api.rate_limit_status()
	reset = rate['resources']['statuses']['/statuses/user_timeline']['reset']
	limit = rate['resources']['statuses']['/statuses/user_timeline']['limit']
	remaining = rate['resources']['statuses']['/statuses/user_timeline']['remaining']
	# Parse the UTC time
	reset = datetime.datetime.fromtimestamp(reset)
	print "{} of {} requests remaining until: {}".format(remaining, limit, reset)

	# Wait till we are ready (wait if over 50% of limit used)
	#if (remaining != limit):
	if (remaining < (limit * 0.50)):
		# Calculate a delay and sleep ...
		delay = int((reset - datetime.datetime.now()).total_seconds()) + 3
		print "Sleeping for {} seconds...".format(delay)
		time.sleep(delay)

	# Make request for user statuses
	print "Getting tweets of user: %s"%(screen_name)
	alltweets = [[
		tweet.user.screen_name,
		tweet.user.name.encode("utf-8"),
		tweet.user.id_str,
		tweet.user.description.encode("utf-8"),
		tweet.created_at,
		tweet.created_at.year,
		tweet.created_at.month,
		tweet.created_at.day,
		tweet.id_str,
		tweet.text.encode("utf-8")
	] for tweet in tweepy.Cursor(
		api.user_timeline,
		screen_name=screen_name,
		since_id=latest,
		monitor_rate_limit=True,
		wait_on_rate_limit=True,
		wait_on_rate_limit_notify=True).items()]

	# Print count of new tweets
	print "%s tweets downloaded\n"%(len(alltweets))

	# Insert tweets read from CSV
	alltweets.extend(csvtweets)

	# Write the csv
	with open(csvfilename, 'wb') as f:
		# Build writer
		writer = csv.writer(f)
		# Write CSV header
		writer.writerow(["screen_name","name","twitter_id","description","created_at","year","month","date","tweet_id","tweet"])
		# Write tweets to CSV
		writer.writerows(alltweets)
	# Close file
	f.close

	# pass
	pass



# Let's go
if __name__ == '__main__':

	# Pass in the username of the account you want to download
	# get_tweets("cberetta")

	if len(sys.argv) >= 2:
		get_tweets(sys.argv[1])
	else:
		print "Usage: tweet_downloader.py [screen_name]"



#EOF
