from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))
example_sentence = 'This is an example showing off stop word filtration '

words = word_tokenize(example_sentence)
print("ORIGINAL: ", words)

filtered_sentence = []
print("\nRemoving the stop words from given Sentence \n ")
# for w in words:
#     if w not in stop_words:
#         filtered_sentence.append(w)

filtered_sentence = [w for w in words if w not in stop_words]
print("Filtered: ", filtered_sentence)
