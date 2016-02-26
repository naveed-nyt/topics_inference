from __future__ import print_function

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from email_reader import EmailLoader

n_samples = 2000
n_features = 1000
n_topics = 10
n_top_words = 5

class NMFTopics:
	# Constructor
	def __init__(self, filename):
		# Load emails from full path to file
		emails = EmailLoader(filename).get_email_dict_array()

		# Process emails into a list of email body contents
		self.email_data = []

		for email_rec in emails:
			if email_rec['body']:
				self.email_data.append(email_rec['body'])

	## Public methods ##
	def process(self):
		# Calculate term frequency-inverse document frequency for NMF
		tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
		tfidf = tfidf_vectorizer.fit_transform(self.email_data)

		# Fit the NMF model to data samples
		nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)

		# Print the topics
		tfidf_feature_names = tfidf_vectorizer.get_feature_names()
		self._print_topics(nmf, tfidf_feature_names, n_top_words)

	## Private methods ##
	def _print_topics(self, model, feature_names, n_top_words):
	    for topic_idx, topic in enumerate(model.components_):
	        print("Topic #%d:" % topic_idx)
	        print(" ".join([feature_names[i]
	                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
	    print()
