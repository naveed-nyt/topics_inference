from __future__ import print_function

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from email_reader import EmailLoader
from text_cleaner import TextCleaner

NUM_TOPICS = 10
NUM_WORDS_PER_TOPIC = 5

class NMFTopics:
	# Constructor
	def __init__(self, filename):
		# Member variables
		self.email_data = []
		self.nmf = None
		self.feature_names = None
		self.num_topics = NUM_TOPICS
		self.num_words_per_topic = NUM_WORDS_PER_TOPIC

		# Load emails from full path to file
		emails = EmailLoader(filename).get_email_dict_array()

		# Process emails into a list of email body contents
		self.email_data = []

		for email_rec in emails:
			if email_rec['body']:
				# Clean the text and add to list
				cleaner = TextCleaner(email_rec['body'])

				self.email_data.append(" ".join(cleaner.tokenize_str()))

	## Public methods ##
	def process(self, topics=None):
		# Check if default numbers should be used
		if topics is None:
			topics = self.num_topics
			
		# Calculate term frequency-inverse document frequency for NMF
		tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
		tfidf = tfidf_vectorizer.fit_transform(self.email_data)

		# Fit the NMF model to data samples
		self.nmf = NMF(n_components=topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)

		# Set the feature name (words)
		self.feature_names = tfidf_vectorizer.get_feature_names()

	def print_topics(self, words_per_topic=None):
		# Check if default number of words per topics should be used
		if words_per_topic is None:
			words_per_topic = self.num_words_per_topic

		self._print_topics(self.nmf, self.feature_names, words_per_topic)

	## Private methods ##
	def _print_topics(self, model, feature_names, words_per_topic):
	    for topic_idx, topic in enumerate(model.components_):
	        print("Topic #%d:" % topic_idx)
	        print(" ".join([feature_names[i]
	                        for i in topic.argsort()[:-words_per_topic - 1:-1]]))

	    print()
