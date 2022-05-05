# reddit_dib_scraper
A project to scrape r/dataisbeautiful


# Codebook:
The data in the database is organized as follows:

Post Table:
| Variable Name         | Explanation                                               | Coding                               |
|-----------------------|-----------------------------------------------------------|--------------------------------------|
| post_id (Primary Key) | Reddit's internal ID for the post                         | String                               |
| user_id               | Reddit's internal user id string                          | String                               |
| time_posted           | Timestamp of when the post was originally created         | Timestamp without timezone           |
| permalink             | The URL to the post                                       | String                               |
| content_url           | If available, the URL to the content itself               | String                               |
| post_title            | The title of the post                                     | String                               |
| chart_type            | Manually added. What type of chart does the post contain? | String                               |
| topic                 | Manually added. What topic is the visualization about?    | String                               |
| animated              | Is the post a still image or animated?                    | Bool, 1 = animation, 0 = still image |


Scan Table:
| Variable Name           | Explanation                                                               | Coding                              |
|-------------------------|---------------------------------------------------------------------------|-------------------------------------|
| record_id (Primary Key) | Serial Number                                                             | Integer                             |
| post_id (Foreign Key)   | Reddit's internal ID for the post                                         | String                              |
| scan_timestamp          | Timestamp of when the scan took place                                     | Timestamp without timezone          |
| upvotes                 | Numer of upvotes of the post at the time of scanning                      | Integer                             |
| upvote_ratio            | The ratio between up and downvotes at the time of scanning                | Float                               |
| n_comments              | Number of Comments at the time of scanning                                | Integer                             |
| hot_position            | What rank in the hot page is this post displayed at the time of scanning? | Integer,  0 = post only on new page |

