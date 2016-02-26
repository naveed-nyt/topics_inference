import sys
import nltk
import re
import os
from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup

# Based on code from http://brandonrose.org/clustering

def _get_stop_words_set():
	try:
		stop_words = set(nltk.corpus.stopwords.words('english'))
	except LookupError as err:
		print(err)
		print('Performing nltk.download()')
		nltk.download()
		stop_words = set(nltk.corpus.stopwords.words('english'))
	return stop_words	

def _get_stemmer():
	return SnowballStemmer('english')

def _strip_html_tags(text):
	return BeautifulSoup(text, 'html.parser').get_text()

def tokenize_str(text):
	stop_words = _get_stop_words_set()
	stemmer = _get_stemmer()
	text = _strip_html_tags(text)
	tokens = [word for sentence in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sentence)]
	filtered_tokens = []
	for token in tokens:
		token = token.lower()
		# Filter out non alphabetic and stop words
		if re.search('[a-zA-Z]', token) and token not in stop_words:
			filtered_tokens.append(token)
	stems = [stemmer.stem(t) for t in filtered_tokens]
	return stems

if __name__ == '__main__':
	print tokenize_str('The quick brown fox <html><body>jumps</body></html> over the lazy dog.\nAnd then some more...')