#### TODO ####
'''
Schedule follows and unfollows
expand post possibilities
logging and try catching
Metadata for followers
emails on errors
'''

####



from API import InstagramBot, PexelsBot, GooglePlacesBot
from Caption import Caption
from SubmissionValidator import SubmissionValidator
import urllib.request
import requests
import schedule
import time
import random
import re
from datetime import timedelta, datetime
import threading
from database import Database

def main():
	google = GooglePlacesBot()
	ret_photo_meta = google.fetch_place()
	fetch_count = 1

	if ret_photo_meta.get("no_photos"):
		print('error: No good photo found')
		print('bad city')
		
	#try to get photos from another city
	#cap it at 3 to be frugal for the photos api
	while ret_photo_meta.get("no_photos") and fetch_count < 3:
		print('attempting another fetch')
		ret_photo_meta = google.fetch_place()
		fetch_count += 1
		if fetch_count == 3:
			return


	# ret_photo_meta = {
	# 			"city": "New York",
	# 			"country": "New York",
	# 			"name": "Central Park"
	# 		}

	caption = Caption(ret_photo_meta['city'], ret_photo_meta['country'], ret_photo_meta['name'], ret_photo_meta['address'], "memeMeta/memeHashtags.txt", "memeMeta/memeCaptions.txt")
	bot = InstagramBot(image = "travelImage.jpg", caption = caption.text)
	bot.execute()


def mass_follow():
	bot = InstagramBot(image = "memeImage.jpg", caption = '')	
	bot.login()
	db = Database()
	bot.scrape_follows()
	# with open('memeMeta/memeAccounts.txt') as f:
	# 	accounts = f.readlines()
	# 	for i in range(350):
	# 		random_acct = accounts[random.randint(0, len(accounts) -1)]
	# 		bot.follow(random_acct, db)
	# 		time.sleep(random.randint(25, 30))
	# db.close_connection()

def mass_unfollow():
	bot = InstagramBot(image = "memeImage.jpg", caption = '')
	bot.login()
	db = Database()
	bot.unfollow(db)
	db.close_connection()


#Helper function to determine random posts within a range of an hour 
def schedule_random_posts():
	r1 = random.randint(00, 59)
	r2 = random.randint(00, 59)
	r3 = random.randint(00, 59)

	s1 = round(random.uniform(0, 59), 6)
	s2 = round(random.uniform(0, 59), 6)
	s3 = round(random.uniform(0, 59), 6)


	now = now = datetime.now()
	t1 = now + timedelta(hours=4, minutes = r1, seconds = s1)
	t2 = now + timedelta(hours=8, minutes = r2, seconds = s2)
	t3 = now + timedelta(hours=13, minutes = r3, seconds = s3)

	delay1 = (t1 - now).total_seconds()
	delay2 = (t2 - now).total_seconds()
	delay3 = (t3 - now).total_seconds()

	threading.Timer(delay1, main).start()
	threading.Timer(delay2, main).start()
	threading.Timer(delay3, main).start()


schedule.every().day.at("00:00").do(schedule_random_posts)
schedule.every().day.at("00:00").do(mass_follow)



# main()
# while True:
#     schedule.run_pending()
#     time.sleep(60) # wait one minute


##Heroku time is EST +5 HOURS

# main()
mass_follow()
#mass_unfollow()


#test db
# db = Database()
# db.delete_pending_follows()