"""
Find a string starts with vowel in a sentence.
"""

text = "A simple life is a happy for me"

import re

print(re.findall(r'\b[(aeiou)].*?\b', text.lower()))
