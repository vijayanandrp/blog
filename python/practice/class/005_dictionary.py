#!/usr/bin/env python
from pprint import pprint

"""
Dictionary is collections of unordered sets of objects like list.
Starts with { and ends with }.
Unique key - value pairs data structure.
"""

print(" Dictionary Concepts ")
# ==========================================================================
print('=' * 5, 'Available functions ', '=' * 5)
# _ available function of dict objects
for func in dir(dict):
    if not (func.startswith('__') and func.endswith('__')):
        print('[*] {}'.format(func))

print(" CRUD ")
print('=' * 5, 'Create Dictionary object ', '=' * 5)

# empty dict
dict1 = {}
dict2 = dict()

# dictionary with integer keys
my_dict = {1: 'apple',
           2: 'ball'}

# dictionary with mixed keys
my_dict2 = {'name': 'John', 1: [2, 4, 3]}

# using dict()
my_dict3 = dict({'company': 'apple', 'role': 'CEO'})

# from sequence having each item as a pair
my_dict4 = dict([(1, 'apple'), (2, 'ball')])

x = ('name', 'age', 'dept', 'roll_no')
y = None
this_dict = my_dict3.fromkeys(x, y)

print("this_dict is ", this_dict)
print('dict1 is ', dict1)
print('dict2 is ', dict2)
print('my_dict is ', my_dict)
print('my_dict2 is ', my_dict2)
print('my_dict3 is ', my_dict3)
print('my_dict4 is ', my_dict4)

# ==========================================================================
print('=' * 5, 'Access Dictionary object ', '=' * 5)
my_data = {'name': 'John',
           'dept': 'Information Technology',
           'age': 26,
           'scores': [50, 67, 88, 90, 99]
           }

print(my_data['name'], type(my_data.get('name')))
print(my_data.get('age'), type(my_data.get('age')))
print(my_data.get('scores')[-1], type(my_data.get('scores')))
print(my_data.get('unknown'), type(my_data.get('unknown')))  # returns None

# ==========================================================================
print('=' * 5, 'Add value Dictionary object ', '=' * 5)
my_data['town'] = 'Chennai'  # create key town and assign chennai
my_data['name'] = "Victor"  # updates if key is present already

print(my_data['town'])

x = my_data.setdefault('color', 'Red')
print('x = ', x)
print(my_data['color'])

pprint(my_data)

print('*' * 25)
# get items
for key, value in my_data.items():
    print(key, '=', value)

# get only keys
print(my_data.keys())
# get only values
print(my_data.values())

my_data.setdefault('unknown')
# my_data['unknown'] = None
print(my_data)
# exit()
# ==========================================================================
print('=' * 5, 'Update Dictionary object ', '=' * 5)
my_data['name'] = "Victor"  # updates if key is present already
my_data['country'] = 'India'
my_data['pin'] = 600125
print(my_data['name'], my_data['country'], my_data['pin'])

# ==========================================================================
print('=' * 5, 'Copy Dictionary object ', '=' * 5)
my_data1 = my_data.copy()
print(my_data1)

my_data1 = {**my_data}
print(my_data1)

# ==========================================================================
print('=' * 5, 'Merge Dictionary object ', '=' * 5)
my_data.update(my_dict3)
print(my_data)

new_dict = {**my_data, **my_dict3}
print(new_dict)

# ==========================================================================
print('=' * 5, 'Find/Remove Dictionary object ', '=' * 5)
my_data.pop('scores')
print(my_data)

my_data.popitem()
print(my_data)

# ==========================================================================
print('=' * 5, 'Clear all values Dictionary object ', '=' * 5)
my_data.clear()
print(my_data)

del my_data

try:
    print(my_data)
except Exception as error:
    print(error)

exit()
