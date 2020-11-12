print("Hello World!")

#!/usr/bin/env python

"""
# Coll. of keys that reflects changes.
<view> = <dict>.keys()
# Coll. of values that reflects changes.
<view> = <dict>.values()
# Coll. of key-value tuples.
<view> = <dict>.items()

# Returns default if key is missing.
value  = <dict>.get(key, default=None)
# Returns and writes default if key is missing.
value  = <dict>.setdefault(key, default=None)
# Creates a dict with default value of type.
<dict> = collections.defaultdict(<type>)
# Creates a dict with default value 1.
<dict> = collections.defaultdict(lambda: 1)

<dict>.update(<dict>)
# Creates a dict from coll. of key-value pairs.
<dict> = dict(<collection>)
# Creates a dict from two collections.
<dict> = dict(zip(keys, values))
# Creates a dict from collection of keys.
<dict> = dict.fromkeys(keys [, value])

# Removes item or raises KeyError.
value = <dict>.pop(key)
# Filters dictionary by keys.
{k: v for k, v in <dict>.items() if k in keys}

Counter


 from collections import Counter
 colors = ['blue', 'red', 'blue', 'red', 'blue']
 counter = Counter(colors)
 counter['yellow'] += 1
Counter({'blue': 3, 'red': 2, 'yellow': 1})
 counter.most_common()[0]
('blue', 3)
"""

print(" Dictionary concepts")