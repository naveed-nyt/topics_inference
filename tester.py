import sys
from nmf_topics import NMFTopics
from lda_topics import LDATopics

# Location of the emails
EMAIL_DATA_LOCATION = '/Users/206958/Desktop/Term_Topics/'

if __name__ == '__main__':
	# Get command line params
	model_type = sys.argv[1]
	email_file = sys.argv[2]

	# Load the proper model
	if model_type.lower() == 'nmf':
		processor = NMFTopics(EMAIL_DATA_LOCATION + email_file)
	else:
		processor = LDATopics(EMAIL_DATA_LOCATION + email_file)

	# Process the topics
	processor.process()

	processor.print_topics(words_per_topic=7)
