from PIL import Image
#Class encapsulating set of rules a submission must pass in order to be posted
class SubmissionValidator:
	def __init__(self):
		self.valid_aspect_ratios = [1, 1.25, 1.77]

	def is_correct_image_size(self, image):
		width, height = Image.open(image).size
		aspect_ratio = width / height
		for valid_ratio in self.valid_aspect_ratios:
			if abs(aspect_ratio - valid_ratio) < .2: return True
		return False
	
	def is_funny(self):
		pass
	
	def is_sfw(self):
		pass