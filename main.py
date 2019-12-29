from API import Reddit, InstagramBot
from Caption import Caption
from SubmissionValidator import SubmissionValidator
import urllib.request
import requests
import schedule
import time

def getMeme(reddit):
	memes = reddit.fetch_submissions('memeSubreddits.txt')
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
	caption = Caption("memeHashtags.txt", "memeCaptions.txt")
	is_valid_size = submission_validator.is_correct_image_size(selectedMeme)
	while not is_valid_size: 
		print("No good: Fetching new meme")
		selectedMeme = getMeme(reddit)
		is_valid_size = submission_validator.is_correct_image_size(selectedMeme)
	print('attempting to post')
	bot = InstagramBot(image = "memeImage.jpg", caption = caption.text)
	bot.execute()




schedule.every().day.at("9:00").do(main)
schedule.every().day.at("15:57").do(main)
schedule.every().day.at("18:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute