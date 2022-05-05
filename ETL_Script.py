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
	user_agent='script by u/ktrutmann')

# Get top 100 posts of hot and new page:
hot_page = reddit.subreddit('dataisbeautiful').hot(limit=100)
new_page = reddit.subreddit('dataisbeautiful').new(limit=100)

# Praw lazy-loads objects. Force it to make an actual API call:
for i in hot_page:
	pass
for i in new_page:
	pass


# Transform: --------------------

# TODO: (1) Add the new page posts!
post_df = pd.DataFrame(dict(
	post_id=[post.id for post in hot_page._listing],  # TODO: (2) Or name? Check which one retreives the post!
	user_id=[post.author_fullname for post in hot_page._listing],
	time_posted=[post.created_utc for post in hot_page._listing],
	permalink=[post.permalink for post in hot_page._listing],
	content_url=[post.url for post in hot_page._listing],
	post_title=[post.title for post in hot_page._listing]))
scan_df = pd.DataFrame(dict(post_id=[post.id for post in hot_page._listing],
	scan_timestamp=[int(time.time())] * len(hot_page._listing), 
	upvotes=[post.ups for post in hot_page._listing],
	upvote_ratio=[post.upvote_ratio for post in hot_page._listing],
	n_comments=[post.num_comments for post in hot_page._listing],
	hot_position=[i for i, _ in enumerate(hot_page._listing)]))

# Drop the first post, as it is always the pinned one.
post_df = post_df.iloc[1:, :]
scan_df = scan_df.iloc[1:, :]


# Load: --------------------

db_connection = psycopg2.connect(os.environ['DATABASE_URL'])
db_cursor = db_connection.cursor()

# TODO: (3) Implement the loading of the data.

db_connection.commit()
db_connection.close()