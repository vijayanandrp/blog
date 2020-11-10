"""
POS tag list:

CC	coordinating conjunction
CD	cardinal digit
DT	determiner
EX	existential there (like: "there is" ... think of it like "there exists")
FW	foreign word
IN	preposition/subordinating conjunction
JJ	adjective	'big'
JJR	adjective, comparative	'bigger'
JJS	adjective, superlative	'biggest'
LS	list marker	1)
MD	modal	could, will
NN	noun, singular 'desk'
NNS	noun plural	'desks'
NNP	proper noun, singular	'Harrison'
NNPS	proper noun, plural	'Americans'
PDT	predeterminer	'all the kids'
POS	possessive ending	parent's
PRP	personal pronoun	I, he, she
PRP$	possessive pronoun	my, his, hers
RB	adverb	very, silently,
RBR	adverb, comparative	better
RBS	adverb, superlative	best
RP	particle	give up
TO	to	go 'to' the store.
UH	interjection	errrrrrrrm
VB	verb, base form	take
VBD	verb, past tense	took
VBG	verb, gerund/present participle	taking
VBN	verb, past participle	taken
VBP	verb, sing. present, non-3d	take
VBZ	verb, 3rd person sing. present	takes
WDT	wh-determiner	which
WP	wh-pronoun	who, what
WP$	possessive wh-pronoun	whose
WRB	wh-abverb	where, when
"""


import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer


# PunktSentenceTokenizer is the unsupervised machine learning,
# so you can actually train it on any body of text that you use

# training PunktSentenceTokenizer
train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

custom_sent_tokenizer = PunktSentenceTokenizer(train_text=train_text)
tokenized = custom_sent_tokenizer.tokenize(text=sample_text)

"""
Chunking in Natural Language Processing (NLP) is the process by which we group various words
together by their part of speech tags.

One of the most popular uses of this is to group things by what are called "noun phrases."
We do this to find the main subjects and descriptive words around them,
but chunking can be used for any combination of parts of speech.

+ = match 1 or more
? = match 0 or 1 repetitions.
* = match 0 or MORE repetitions
. = Any character except a new line
"""


def process_content():
	try:
		for sent in tokenized[:5]:
			# sentence into list of words
			words = nltk.word_tokenize(sent)
			tagged = nltk.pos_tag(words)
			
			chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
			
			chunkParser = nltk.RegexpParser(chunkGram)
			chunked = chunkParser.parse(tagged)
			
			chunked.draw()
	
	except Exception as error:
		print(str(error))

if __name__ == "__main__":
	process_content()
