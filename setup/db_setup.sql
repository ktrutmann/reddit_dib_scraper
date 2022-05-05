CREATE TABLE posts (
	post_id VARCHAR(10) PRIMARY KEY,
	user_id VARCHAR(20) NOT NULL,
	time_posted TIMESTAMP(0) NOT NULL,
	permalink VARCHAR NOT NULL,
	content_url VARCHAR,
	post_title VARCHAR NOT NULL,
	chart_type VARCHAR, -- These we will have to fill in later
	topic VARCHAR,
	animated BOOLEAN)
;

CREATE TABLE post_scans (
	record_id SERIAL PRIMARY KEY,
	post_id VARCHAR(50) REFERENCES posts (post_id),
	scan_timestamp TIMESTAMP [0] NOT NULL,
	upvotes INT,
	upvote_ratio REAL,
	n_comments INT,
	hot_position INT
);

