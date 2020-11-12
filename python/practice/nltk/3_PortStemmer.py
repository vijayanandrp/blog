#!/usr/bin/env python

# Stemmer to find the root word

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# As we gonna process only words, sentence tokenizer is not needed

ps = PorterStemmer()

example_words = ["Python","Pythoner","Pythonic","Pythoned","Pythonly"]

for word in example_words:
	print(ps.stem(word))

print("=" * 120)

new_text = "It is very important to be pythonly while you are pythoning with python. " \
		"All pythoners have pythoned poorly atleast once"

words = word_tokenize(new_text)
print(new_text)
portstem_sent = [ps.stem(w) for w in words]
print(" ".join(portstem_sent))
