
"""
1222688
322455

2 - True
"""

import re

n1 = '1222688'
n2 = '322455'

m1 = re.findall(r'(\d){3}\1', n1)
m2 = re.findall(r'(\d){2}\1', n2)

if list(set(m1).intersection(set(m2))):
    print(True)
else:
    print(False)
