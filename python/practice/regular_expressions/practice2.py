
"""

PLACEMENT =  ACPLENMET

([A-Za-z])([A-Za-z])
"""

text = 'PLACEMENT'
import re
x = re.sub('([A-Za-z][A-Za-z])([A-Za-z][A-Za-z])', r'\2\1', text)
print(x)
x = re.sub('(\w\w)(\w\w)', r'\2\1', text)
print(x)
