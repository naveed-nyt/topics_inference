from nmf_topics import NMFTopics
from lda_topics import LDATopics

# Location of the emails
EMAIL_DATA_LOCATION = '/Users/206958/Desktop/Term_Topics/'

# Load the email file
email_file = EMAIL_DATA_LOCATION + 'email_export.xlsx'

# Test topics
tester = LDATopics(email_file)

tester.process()

tester.print_topics(words_per_topic=7)
