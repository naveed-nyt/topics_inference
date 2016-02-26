import sys
import nltk
import re
import os
from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

# Based on code from http://brandonrose.org/clustering

class TextCleaner:

	def __init__(self, text):
		self.text = text

	def tokenize_str(self):
		if self.text is None or type(self.text) not in [str, unicode]:
			return []
		text = self.text.encode('utf-8')
		stop_words = self._get_stop_words_set()
		stemmer = self._get_stemmer()
		text = self._strip_text(text)
		tokens = [word for sentence in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sentence)]
		filtered_tokens = []
		for token in tokens:
			token = token.lower()
			# Filter out non alphabetic and stop words
			if re.search('[a-zA-Z]', token) and token not in stop_words:
				filtered_tokens.append(token)
		stems = [stemmer.stem(t) for t in filtered_tokens]
		return stems

	def _get_stop_words_set(self):
		try:
			stop_words = set(nltk.corpus.stopwords.words('english'))
		except LookupError as err:
			print(err)
			print('Performing nltk.download()')
			nltk.download()
			stop_words = set(nltk.corpus.stopwords.words('english'))
		return stop_words	

	def _get_stemmer(self):
		return SnowballStemmer('english')

	def _strip_text(self, text):
		return self._strip_html_tags(text)

	def _strip_html_tags(self, text):
		return BeautifulSoup(text, 'html.parser').get_text()

if __name__ == '__main__':
	cleaner = TextCleaner('The quick brown fox <html><body>jumps</body></html> over the lazy dog.\nAnd then some more...')
	print cleaner.tokenize_str()