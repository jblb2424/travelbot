import random
class Caption:
	def __init__(self, city, country, name, address, hashtag_file = '', body_file = ''):
		self.city = city
		self.country= country
		self.name = name
		self.text = self.get_body(body_file) + "\n\n\n\n\n" +self.get_hashtag_string(hashtag_file)

	def get_hashtag_string(self, file_name):
		return ' '.join(hashtag.strip() for hashtag in open(file_name)) + ' #' + self.country + " #" + self.city

	def get_body(self, file_name):
		texts = [text.strip() for text in open(file_name)]
		idx = random.randint(0, len(texts)-1)

		return "~~~~ " + self.name + " ~~~~" + "\n" + self.city + " " + self.country +  "\n" + texts[idx]