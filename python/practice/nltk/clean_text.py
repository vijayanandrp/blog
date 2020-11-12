#!/usr/bin/env python3.5
# encoding: utf-8


"""
    source: http://stanford.edu/~rjweiss/public_html/IRiSS2013/text2/notebooks/cleaningtext.html
    Create a new list of review_texts called clean_reviews that are:

    tokenized
    free of punctuation
    free of stopwords
    stemmed or lemmatized
    
"""

from nltk.tokenize import word_tokenize # tokenize sentence to words
from nltk.corpus import stopwords   # remove the filler words
# stemming and lemmatizing
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import re
import string

# -------------------------------------------------------------------------

# Create some raw text
incoming_reports = ["We are attacking on their left flank but are losing many men.",
                    "We cannot see the enemy army. Nothing else to report.",
                    "We are ready to attack but are waiting for your orders."]


# apply the word tokenizer to each element of list called incoming_reports
tokenized_reports = [word_tokenize(report) for report in incoming_reports]

print("\n Tokenized sentence", '\n','-'*10)
for token_report in tokenized_reports:
    print(token_report)

# -------------------------------------------------------------------------
regex = re.compile('[%s]' % re.escape(string.punctuation))

tokenized_reports_no_punctuation = []

for review in tokenized_reports:
    new_review = []
    for token in review:
        new_token = regex.sub(u'', token)
        if not new_token == u'':
            new_review.append(new_token)
    
    tokenized_reports_no_punctuation.append(new_review)

print("\n No Punctuation", '\n','-'*10)
for token_report in tokenized_reports_no_punctuation:
    print(token_report)

# -------------------------------------------------------------------------
tokenized_reports_no_stopwords =[]

for report in tokenized_reports_no_punctuation:
    new_term_vector = []
    for word in report:
        if not word in stopwords.words('english'):
            new_term_vector.append(word)
    tokenized_reports_no_stopwords.append(new_term_vector)

print("\n No stopwords", '\n','-'*10)
for token_report in tokenized_reports_no_stopwords:
    print(token_report)

# -------------------------------------------------------------------------
porter = PorterStemmer()
snowball = SnowballStemmer('english')
wordnet = WordNetLemmatizer()

preprocessed_docs = []

for doc in tokenized_reports_no_stopwords:
    final_doc = []
    for word in doc:
        # final_doc.append(porter.stem(word))
        final_doc.append(snowball.stem(word))
        # final_doc.append(wordnet.lemmatize(word))
    preprocessed_docs.append(final_doc)
        
print("\n After stemming/lemmatizing", '\n','-'*10)
for token_report in preprocessed_docs:
    print(token_report)

# -------------------------------------------------------------------------
