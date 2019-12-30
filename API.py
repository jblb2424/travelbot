import praw
import json
import random
import time
from selenium import webdriver
import os


with open('keys.json', 'r') as keys:
	auth_json=keys.read()
auth = json.loads(auth_json)

#Simple Wrapper to capture relevant memes
class Reddit:
	def __init__(self):
		self.fetcher = praw.Reddit(
			client_id=auth["client_id"],
			client_secret=auth["client_secret"], 
			password=auth["password"],
			user_agent=auth["user_agent"],
			username=auth["username"]
		)

	def __fetchSubreddits(self, file_name):
		subreddit_file= open(file_name)
		subreddits = []
		for s in subreddit_file:
			subreddits.append(s.strip())
		return subreddits



	def fetch_submissions(self, file_name):
		submissions = []
		subreddits = self.__fetchSubreddits(file_name)
		for i in range(1):
			idx = random.randint(0, len(subreddits)-1)
			random_subreddit = subreddits[idx]
			subreddit = self.fetcher.subreddit(random_subreddit)
			rising = subreddit.rising(limit=1)
			for submission in rising:
				submissions.append(submission)
		return submissions


class InstagramBot:
	def __init__(self, image, caption):
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
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--no-sandbox")
		return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), desired_capabilities = chrome_options.to_capabilities())


	def __login(self):
		self.driver.get('https://www.instagram.com/accounts/login/')
		time.sleep(5)
		form = self.driver.find_element_by_tag_name('form')
		self.driver.find_elements_by_tag_name('input')[0].send_keys(self.username)
		self.driver.find_elements_by_tag_name('input')[1].send_keys(self.password)
		form.submit()
		time.sleep(5)
		cancel_again = self.driver.find_element_by_class_name("GAMXX")
		cancel_again.click()
		time.sleep(5)
		omg_not_another_cancel = self.driver.find_element_by_class_name("aOOlW")
		omg_not_another_cancel.click()
		time.sleep(5)

	def __post(self):
		new_post = self.driver.find_element_by_class_name("q02Nz")
		new_post.click()
		time.sleep(4)
		inputs = self.driver.find_elements_by_tag_name("input")
		inputs[0].send_keys(os.getcwd()+"/memeImage.jpg")
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
		time.sleep(5)
		self.driver.close()

	def execute(self):
		self.__login()
		self.__post()
		

	def unfollow(self):
		pass

	def follow(self):
		pass

		

















