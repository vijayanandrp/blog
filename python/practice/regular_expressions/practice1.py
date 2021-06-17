# substitute string into numbers
# a-m = 0
# n-z = 1


text = 'string'
import re
text = re.sub('([n-z])', '1', re.sub('([a-m])', '0', text))
print(text)
