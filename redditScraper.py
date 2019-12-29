from Reddit import Reddit
from SubmissionValidator import SubmissionValidator
import urllib.request


def main():
	reddit = Reddit()
	memes = reddit.fetchMemeUrls()
	submission_validator = SubmissionValidator()
	for meme in memes:
		image = urllib.request.urlopen(meme.url)
		is_valid_size = submission_validator.is_correct_image_size(image)
		






main()


