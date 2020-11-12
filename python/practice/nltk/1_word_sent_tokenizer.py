# SOURCE for learning
# https://www.youtube.com/watch?v=FLZvOKSCkxY


# step: 1
# install nltk for PYTHON 3
# pip3 install nltk
#
# import nltk
# nltk.download()
#
# tokenizing  == word tokenizer, sentence tokenizer

# lexicon and corporas
# corpora  - body of texts. example - medical journals, presidential speeches, English language
# lexicon - words and their meanings
# investor-speak .. regular English - speak
# investor speak 'bull' = someone who is positive about the market
# regular speak 'bull' = scary buffalo like animal

from nltk import word_tokenize, sent_tokenize


example_text = """Hello Mr. Vijay, how are you today? The weather is great and Python is awesome.
                The sky is blue. You should work for hackathon."""

print('Word Tokenizer: ', word_tokenize(example_text))
print('Sentence Tokenizer: ', sent_tokenize(example_text))

print('$' * 120)
for i in sent_tokenize(example_text):
    print(i)

print('$' * 120)
for i in word_tokenize(example_text):
    print(i)
print('$' * 120)


