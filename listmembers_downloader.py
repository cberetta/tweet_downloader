#!/usr/bin/env python
# encoding: utf-8

import tweepy # https://github.com/tweepy/tweepy
import csv
import os.path

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def get_list_members(screen_name, list_name):

	# Define CSV filename and check if already exists
	csvfilename = '%s-members-of-%s.csv'%(screen_name, list_name)
	if os.path.exists(csvfilename):
		print "Cannot overwrite %s"%(csvfilename)
		print "Aborted!\n"
		return

	# Authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	# Initialize a list to hold all the members
	allmembers = []

	# Make request for members list
	print "Getting members of list <%s> from user: %s"%(list_name, screen_name)
	allmembers =[[
		member.screen_name,
		member.name.encode("utf-8"),
		member.id_str,
		member.description.encode("utf-8")
		] for member in tweepy.Cursor(api.list_members, screen_name, list_name).items()]

	# Write the csv
	with open(csvfilename, 'wb') as f:
		# Build writer
		writer = csv.writer(f)
		# Write CSV header
		writer.writerow(["screen_name","name","twitter_id","description"])
		# Write tweets to CSV
		writer.writerows(allmembers)
	# Close file
	f.close

	# pass
	pass



# Let's go
if __name__ == '__main__':
	# Pass in the username of the account you want to download
	get_list_members("cberetta", "la-pina")



#EOF
