import praw
import json
import random
import time
from selenium import webdriver
import os
import time
import csv
import gender_guesser.detector
import requests, json
import urllib
import re
from database import Database
from datetime import datetime
from datetime import timedelta


with open('keys.json', 'r') as keys:
	auth_json=keys.read()
auth = json.loads(auth_json)




#### Interface for my different bots ####

class PexelsBot:
	def __init__(self):
		self.key = '563492ad6f91700001000001825edc5fd02e49f1b0a5f7ee6c92e9f3'
		self.base_url = 'https://api.pexels.com/v1/search?query=travel&per_page=10000'
		self.pages = 125

	def __get_location(self, url):
		html = requests.get(url).text
		location = re.search(r"(?<=<span class='js-photo-page-photographer-card-location' style=''> · ).*(?=</span>)", html)
		return location

	def fetch_post(self):
		page_select = random.randint(0, self.pages)
		request = requests.get(self.base_url + '&page=' + str(page_select), headers={'Authorization': self.key}).json()
		photos = request['photos']
		rand_idx = random.randint(0, len(photos) -1)
		rand_photo = photos[rand_idx]
		
		##Get post url and regular url for scraping location
		medium_photo_url = rand_photo['src']['medium']
		original_post_url = rand_photo['url']
		location = self.__get_location(original_post_url)
		print(location)
		return medium_photo_url


class GooglePlacesBot:
	def __init__(self):
		self.key = 'AIzaSyCQUHJvOYF7fiCp3EF4xht_y4ASOvpV6LU'
		self.base_place_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?key=' + self.key
		self.base_photo_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=1600&maxheight=1600&key=' + self.key


	def __fetch_photo(self, photo_reference):
		extended_url = '&photoreference=' + photo_reference
		full_url = self.base_photo_url + extended_url
		picture_request = requests.get(full_url)
		if picture_request.status_code == 200:
			with open("travelImage.jpg", 'wb') as f:
				f.write(picture_request.content)

	#ensures we don't pick a photo that isn't like a store
	def is_valid_photo_type(self, types):
		with open('type_blacklist.txt') as f:
			blacklist = f.read().splitlines() 
		is_invalid_type = len(set(types) & set(blacklist))  == 0
		return is_invalid_type

	#saves new picture to directory and returns name
	def fetch_place(self):

		#Establish db connection to fetch and saved used photos
		db = Database()

		with open('cities.csv') as f:

			photo_reference = 'init'
			final_city = 'init'
			final_country = 'init'
			final_name = 'init'
			final_address = 'init'
			final_types = 'init'

			#check db to see if the post we grabbed is old
			while photo_reference == 'init' or db.photo_used(photo_reference):
				reader = csv.reader(f)
				chosen_row = random.choice(list(reader))
				city, country = chosen_row[0].strip().replace(" ", "%20"), chosen_row[1].strip().replace(" ", "%20")
				print(city)
				print(country)
				extended_url = '&location=' + country + '&query='+city+'+point+of+interest&language=en'
				full_url = self.base_place_url + extended_url
				data = requests.get(full_url).json()
				results = data['results']
				if not results:
					return {"no_photos": True}

				used_indexes = set()
				random_result_idx = random.randint(0, len(results) -1)
				used_indexes.add(random_result_idx)
				
				result = results[random_result_idx]
				name = result['name']
				address = result["formatted_address"]
				types = result.get('types')

				print(full_url)
				print(types)


				#Not all results have a photo - keep looking for one
				#If no photo is found - return an error. This city has no photos
				while not result.get('photos') or not self.is_valid_photo_type(types):
					random_result_idx = random.randint(0, len(results) -1)
					
					used_indexes.add(random_result_idx)
					result = results[random_result_idx]
					types = result.get('types')
					if len(used_indexes) == len(results):
						return {"no_photos": True}
				

				photo_reference = result['photos'][0]['photo_reference']
				# print(photo_reference)
				self.__fetch_photo(photo_reference)

				final_city = chosen_row[0].strip()
				fial_country = chosen_row[1].strip()
				final_name = name
				final_address = address
				final_types = types
				time.sleep(5)
			
			#At this point we found the photo we want
			#save and return
			db.save_photo(photo_reference)
			return {
				"city": final_city,
				"country": fial_country,
				"name": final_name,
				"address": final_address
			}



class InstagramBot:
	def __init__(self, image = None, caption = None):
		self.username = auth["instagram_username"]
		self.password = auth["instagram_password"]
		self.follow_limit = 400
		self.image = image
		self.caption = caption
		self.driver = self.__initialize_driver()

	def __initialize_driver(self):
		mobile_emulation = { "deviceName": "iPhone 6" }
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
		chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		chrome_options.add_argument('--profile-directory=Default') 
		# chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--no-sandbox")
		return webdriver.Chrome(executable_path="./chromedriver", desired_capabilities = chrome_options.to_capabilities())

	def __get_user_metadata(self, account_name, person_name, source):
		d = gender_guesser.detector.Detector()
		is_private = len(self.driver.find_elements_by_class_name("rkEop")) > 0
		media_count = self.driver.find_elements_by_class_name("g47SY")[0].text
		followers = self.driver.find_elements_by_class_name("g47SY")[1].text
		following = self.driver.find_elements_by_class_name("g47SY")[2].text
		follow_time = datetime.now()
		split_name = person_name.split()
		if len(split_name) > 0:
			gender = 'unknown'
		gender = d.get_gender(split_name[0])
		print(account_name)
		print(person_name)
		print(is_private)
		print(media_count)
		print(gender)
		print(followers)
		print(following)	
		return {
			'account_name': account_name,
			'person_name': person_name,
			'is_private': is_private,
			'media_count': media_count,
			'gender': gender,
			'followers': followers,
			'following': following,
			'follow_time': follow_time,
			'source': source
		}

	def scrape_follows(self):
		global time
		db = Database()
		with open('memeMeta/memeAccounts.txt') as f:
			accounts = f.readlines()
			for i in range(3):
				account = accounts[random.randint(0, len(accounts) -1)]
				time.sleep(random.randint(25, 30))
				
				print("attempting to follow")
				self.driver.get('https://www.instagram.com/' + account )
				time.sleep(random.randint(5,8))
				followers_button = self.driver.find_elements_by_class_name("_81NM2")[1]
				followers_button.click()
				time.sleep(random.randint(5, 8))
				# followers= self.driver.find_elements_by_class_name("FPmhX")
				
				#find number of followers
				
				#scroll down the page
				for i in range(30):
				    self.driver.execute_script("document.querySelector('._6xe7A').parentNode.scrollTop=1e100")
				    time.sleep(random.randint(2,5))

				rows = self.driver.find_elements_by_class_name("wo9IH")
				print('number or rows = ' + str(len(rows)))
				for i in range(100):
					idx = random.randint(0, len(rows) -1)
					row = rows[idx]
					account_name = row.find_element_by_class_name("d7ByH").text
					person_name = row.find_element_by_class_name("wFPL8").text
					db.save_pending_follow(account_name, person_name)
					rows.remove(row)
		db.close_connection()
				

	def login(self):
		self.driver.get('https://www.instagram.com/accounts/login/')
		time.sleep(random.randint(5, 8))
		form = self.driver.find_element_by_tag_name('form')
		self.driver.find_elements_by_tag_name('input')[0].send_keys(self.username)
		self.driver.find_elements_by_tag_name('input')[1].send_keys(self.password)
		form.submit()
		time.sleep(random.randint(5, 8))
		cancel_again = self.driver.find_element_by_class_name("sqdOP")
		cancel_again.click()
		time.sleep(random.randint(5, 8))
		omg_not_another_cancel = self.driver.find_element_by_class_name("aOOlW")
		omg_not_another_cancel.click()
		time.sleep(random.randint(5, 8))
		print('logged in')

	def __post(self):
		print('attempting to post')
		new_post = self.driver.find_element_by_class_name("q02Nz")
		new_post.click()
		time.sleep(4)
		inputs = self.driver.find_elements_by_tag_name("input")
		inputs[0].send_keys(os.getcwd()+"/travelImage.jpg")
		time.sleep(3)
		try: 
			next_btn = self.driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
		except:
			self.driver.get('https://www.instagram.com/accounts/login/')
			self.__post()
		time.sleep(5)
		caption_field = self.driver.find_element_by_xpath("//textarea[@aria-label='Write a caption…']")
		caption_field.send_keys(self.caption)
		time.sleep(5)
		share_btn = self.driver.find_element_by_xpath("//button[contains(text(),'Share')]").click()
		print('Successfully Posted!')
		time.sleep(5)
		self.driver.close()		

	def unfollow(self, db):
		now = datetime.now()
		few_days = timedelta(days = 5)
		few_day_offset = now - few_days
		to_unfollow = db.find_stale_following(few_day_offset)
		for account_name in to_unfollow:
			print(account_name)
			self.driver.get('https://www.instagram.com/' + account_name[0])
			
			unfollow_prompt = self.driver.find_element_by_class_name("_5f5mN")
			unfollow_prompt.click()
			confirm_unfollow = self.driver.find_element_by_xpath('//button[text()="Unfollow"]')
			confirm_unfollow.click()

		db.delete_stale_following()

	def follow(self, account, db):
		global time
		print("attempting to follow")
		self.driver.get('https://www.instagram.com/' + account )
		time.sleep(random.randint(5,8))
		followers_button = self.driver.find_elements_by_class_name("_81NM2")[1]
		followers_button.click()
		time.sleep(random.randint(5, 8))
		# followers= self.driver.find_elements_by_class_name("FPmhX")
		
		#find number of followers
		
		#scroll down the page
		for i in range(30):
		    self.driver.execute_script("document.querySelector('._6xe7A').parentNode.scrollTop=1e100")
		    time.sleep(random.randint(500,1000)/1000)

		rows = self.driver.find_elements_by_class_name("wo9IH")
		print('number or rows = ' + str(len(rows)))
		idx = random.randint(0, len(rows) -1)
		row = rows[idx]
		account_name = row.find_element_by_class_name("d7ByH").text
		person_name = self.driver.find_element_by_class_name("wFPL8").text


		self.driver.get('https://www.instagram.com/' + account_name)
		time.sleep(random.randint(5, 8))
		#### Collect Metadata ####
		metadata = self.__get_user_metadata(account_name, person_name, account)
		#### Initiate the Follow ####
		follow_btn = self.driver.find_element_by_class_name("ffKix")
		follow_btn.click()

		#Save the follow
		db.save_follower(account_name, datetime.now())


	def execute(self):
		self.login()
		self.__post()


		

		

















