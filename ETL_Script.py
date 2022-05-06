###############################################################################
#####-------------------- Reddit Scraper ETL Script ----------------------#####
#                                                                             #
# Author: Kevin Trutmann (k.trutmann@gmail.com)                               #
#                                                                             #
# This script connects to the Reddit API and gets the top 100 posts from      #
# r/dataisbeautiful's hot as well as new page.                                #
# It then extracts some key information and loads this data into a            #
# database for later analysis.                                                #
###############################################################################

import praw
import pandas as pd
import psycopg2
import os
import time


# Extract: --------------------

# Get a "Reddit" object to talk to the API:
reddit = praw.Reddit(
	client_id=os.environ['praw_client_id'],
	client_secret=os.environ['praw_client_secret'],
	refresh_token=os.environ['praw_refresh_token'],
	user_agent='Get posts from r/dataisbeautiful (by u/ktrutmann)')

# Get top 100 posts of hot and new page:
hot_page = reddit.subreddit('dataisbeautiful').hot(limit=100)
new_page = reddit.subreddit('dataisbeautiful').new(limit=100)

# Praw lazy-loads objects. Force it to make an actual API call:
for i in hot_page:
	pass
for i in new_page:
	pass


# Transform: --------------------

# A helper function to make things cleaner:
def extract_reddit_data(listings, var_to_extract):
	final_list = []
	for this_listing in listings:
		final_list.extend([getattr(this_post, var_to_extract) for
			this_post in this_listing._listing])

	return final_list

post_df = pd.DataFrame(dict(
	post_id=extract_reddit_data([hot_page, new_page], 'id'),
	user_name=extract_reddit_data([hot_page, new_page], 'author'),
	time_posted=extract_reddit_data([hot_page, new_page], 'created_utc'),
	permalink=extract_reddit_data([hot_page, new_page], 'permalink'),
	content_url=extract_reddit_data([hot_page, new_page], 'url'),
	post_title=extract_reddit_data([hot_page, new_page], 'title')))
scan_df = pd.DataFrame(dict(
	post_id=extract_reddit_data([hot_page, new_page], 'id'),
	scan_timestamp=[int(time.time())] *
		(len(hot_page._listing) + len(new_page._listing)),
	upvotes=extract_reddit_data([hot_page, new_page], 'ups'),
	upvote_ratio=extract_reddit_data([hot_page, new_page], 'upvote_ratio'),
	n_comments=extract_reddit_data([hot_page, new_page], 'num_comments'),
	hot_position=[i for i, _ in enumerate(hot_page._listing)] +
		[0 for _ in new_page._listing]))

# Drop the first post, as it is always the pinned one.
post_df = post_df.iloc[1:, :]
scan_df = scan_df.iloc[1:, :]

# Remove duplicates which occur on new and hot:
post_df.drop_duplicates(inplace=True)
scan_df.drop_duplicates(inplace=True, keep='first') # First entry is from hot page


# Load: --------------------

db_connection = psycopg2.connect(os.environ['DATABASE_URL'])
db_cursor = db_connection.cursor()

for this_data in post_df.itertuples(index=False, name=None):
	db_cursor.execute('''INSERT INTO posts (
		post_id, user_id, time_posted, permalink, content_url, post_title)
		VALUES(%s, %s, TO_TIMESTAMP(%s)::TIMESTAMP, %s, %s, %s)
		ON CONFLICT DO NOTHING''',
	 	this_data)

for this_data in scan_df.itertuples(index=False, name=None):
	db_cursor.execute('''INSERT INTO post_scans (
		post_id, scan_timestamp, upvotes, upvote_ratio,
		n_comments, hot_position)
		VALUES(%s, TO_TIMESTAMP(%s)::TIMESTAMP, %s, %s, %s, %s)''',
	 	this_data)

db_connection.commit()
db_cursor.close()
db_connection.close()