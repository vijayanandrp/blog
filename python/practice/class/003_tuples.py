#!/usr/bin/env python

"""
Like string object, tuple object also immutable. The values cannot be changed.
"""

print(" tuple Concepts ")
# ==========================================================================
print('=' * 5, 'Available functions ', '=' * 5)
#  available function of tuple objects
for func in dir(tuple):
    if not (func.startswith('__') and func.endswith('__')):
        print('[*] {}'.format(func))

print(" CRUD ")
print('=' * 5, 'Create tuple object ', '=' * 5)

# empty tuple
tuple1 = tuple()
tuple2 = ()
my_tuple = (1, 2, 3, 4, 5, 5, 5, 5, 6,)

print(tuple1, tuple2, my_tuple, type(my_tuple))
# ==========================================================================
print('=' * 5, 'Access tuple object ', '=' * 5)
"""
Forward index and backward index
 0, 1, 2, 3
(1, 2, 3, 4)
-4, -3, -2, -1
"""
print(my_tuple[1])  # get the index value = 1
print(my_tuple[1:5])  # get the index value from
print(my_tuple[-1])  # get the last element

# ==========================================================================
print('=' * 5, 'Add/Modify/Remove value to tuple object ', '=' * 5)
my_tuple = my_tuple + (7, 8, 9)
print(my_tuple)

print('index')
print(my_tuple.index(1))  # to get index of the value
print(my_tuple.index(9))

print('count')
print(my_tuple.count(5))  # get total occurrence of the value

print('=' * 5, 'Operations on tuple object ', '=' * 5)
print(my_tuple + my_tuple)
print(my_tuple * 2)

print(max(my_tuple), min(my_tuple), len(my_tuple))

print(2 in my_tuple)


