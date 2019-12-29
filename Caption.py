import random
class Caption:
	def __init__(self, hashtag_file = '', body_file = ''):
		self.text = self.get_body(body_file) + "\n\n\n\n\n" +self.get_hashtag_string(hashtag_file)

	def get_hashtag_string(self, file_name):
		return ' '.join(hashtag.strip() for hashtag in open(file_name))

	def get_body(self, file_name):
		texts = [text.strip() for text in open(file_name)]
		idx = random.randint(0, len(texts))
		return texts[idx] 