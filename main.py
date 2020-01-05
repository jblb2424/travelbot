from API import Reddit, InstagramBot
from Caption import Caption
from SubmissionValidator import SubmissionValidator
import urllib.request
import requests
import schedule
import time
import random

def getMeme(reddit):
	memes = reddit.fetch_submissions('memeMeta/memeSubreddits.txt')
	meme= memes[0]
	image = urllib.request.urlopen(meme.url)
	Picture_request = requests.get(meme.url)
	if Picture_request.status_code == 200:
		with open("memeImage.jpg", 'wb') as f:
			f.write(Picture_request.content)
	return image

def main():
	print('Retrieving post')
	reddit = Reddit()
	selectedMeme=getMeme(reddit)
	submission_validator = SubmissionValidator()
	caption = Caption("memeMeta/memeHashtags.txt", "memeMeta/memeCaptions.txt")
	is_valid_size = submission_validator.is_correct_image_size(selectedMeme)
	while not is_valid_size: 
		print("No good: Fetching new meme")
		selectedMeme = getMeme(reddit)
		is_valid_size = submission_validator.is_correct_image_size(selectedMeme)
	print('attempting to post')
	bot = InstagramBot(image = "memeImage.jpg", caption = caption.text)
	bot.execute()



# r1 = random.randint(59)
# r2 = random.randint(59)
# r3 = random.randint(59)
# r4 = random.randint(59)
#Heroku time is EST +5 HOURS
schedule.every().day.at("14:00").do(main)
schedule.every().day.at("19:00").do(main)
schedule.every().day.at("23:00").do(main)
schedule.every().day.at("01:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute