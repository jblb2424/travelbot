import praw
import json

with open('keys.json', 'r') as keys:
	auth_json=keys.read()
auth = json.loads(auth_json)

fetcher = praw.Reddit(
	client_id=auth["client_id"],
	client_secret=auth["client_secret"], 
	password=auth["password"],
	user_agent=auth["user_agent"],
	username=auth["username"]
)

subreddit = fetcher.subreddit('memes')
rising = subreddit.rising(limit=1)
for submission in rising:
	print(submission)