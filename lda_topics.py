from __future__ import print_function

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from email_reader import EmailLoader

NUM_FEATURES = 1000
NUM_TOPICS = 10
NUM_WORDS_PER_TOPIC = 5

class LDATopics:
	# Constructor
	def __init__(self, filename):
		# Member variables
		self.email_data = []
		self.lda = None
		self.feature_names = None
		self.num_topics = NUM_TOPICS
		self.num_words_per_topic = NUM_WORDS_PER_TOPIC
		self.num_features = NUM_FEATURES

		# Load emails from full path to file
		emails = EmailLoader(filename).get_email_dict_array()

		# Process emails into a list of email body contents
		for email_rec in emails:
			if email_rec['body']:
				self.email_data.append(email_rec['body'])

	## Public methods ##
	def process(self, topics=None, features=None):
		# Check if default numbers should be used
		if topics is None:
			topics = self.num_topics
			
		if features is None:
			features = self.num_features

		# Calculate term frequency for LDA
		tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=features, stop_words='english')
		tf = tf_vectorizer.fit_transform(self.email_data)

		# Fit the LDA model to data samples
		self.lda = LatentDirichletAllocation(n_topics=topics, max_iter=5, learning_method='online', learning_offset=50., random_state=0)

		self.lda.fit(tf)

		# Set the feature name (words)
		self.feature_names = tf_vectorizer.get_feature_names()

	def print_topics(self, words_per_topic=None):
		# Check if default number of words per topics should be used
		if words_per_topic is None:
			words_per_topic = self.num_words_per_topic

		self._print_topics(self.lda, self.feature_names, words_per_topic)

	## Private methods ##
	def _print_topics(self, model, feature_names, words_per_topic):
	    for topic_idx, topic in enumerate(model.components_):
	        print("Topic #%d:" % topic_idx)
	        print(" ".join([feature_names[i]
	                        for i in topic.argsort()[:-words_per_topic - 1:-1]]))

	    print()
