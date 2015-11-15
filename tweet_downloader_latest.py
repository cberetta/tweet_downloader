#!/usr/bin/env python
# encoding: utf-8

# Original code: https://gist.github.com/yanofsky/5436496

import tweepy # https://github.com/tweepy/tweepy
import csv
import os.path

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def get_latest_tweets(screen_name):

	# Define CSV filename and check if already exists
	csvfilename = '%s_tweets.csv'%(screen_name)
	if not os.path.exists(csvfilename):
		print "%s not found. Cannot proceed."%(csvfilename)
		print "Run tweet_downloader_all.py first."
		print "Aborted!\n"
		return

	# Read tweets stored into CSV
	csvtweets = []
	with open(csvfilename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] != 'screen_name':
				csvtweets.append(row)
	# Close csvfile
	f.close
	# Get latest tweet_id
	latest = csvtweets[0][8]	# tweet_id is on column 8
	print "latest tweet_id:%s"%(latest)

	# Twitter only allows access to a users 
	# most recent 3240 tweets with this method

	# Authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	# Initialize a list to hold all the tweepy Tweets
	alltweets = []

	# Make initial request for most recent tweets since latest id (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name=screen_name, since_id=latest, count=200)

	# Check if we found some new tweets
	if len(new_tweets) == 0:
		print "No new tweets found for user: %s"%(screen_name)
		return

	# Save most recent tweets
	alltweets.extend(new_tweets)

	# Save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	# Keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "Getting tweets before %s for user: %s"%(oldest, screen_name)

		# All subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name=screen_name, since_id=latest, count=200, max_id=oldest)

		# Save most recent tweets
		alltweets.extend(new_tweets)

		# Update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far..."%(len(alltweets))

	# Transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[
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
		] for tweet in alltweets]

	# Insert tweets read from CSV
	outtweets.extend(csvtweets)

	# Write the csv
	with open(csvfilename, 'wb') as f:
		# Build writer
		writer = csv.writer(f)
		# Write CSV header
		writer.writerow(["screen_name","name","twitter_id","description","created_at","year","month","date","tweet_id","tweet"])
		# Write tweets to CSV
		writer.writerows(outtweets)
	# Close file
	f.close

	# pass
	pass



# Let's go
if __name__ == '__main__':
	# Pass in the username of the account you want to download
	get_latest_tweets("cberetta")



#EOF
