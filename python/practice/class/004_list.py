#!/usr/bin/env python

"""
Python knows a number of compound data types, used to group together other values. 
The most versatile is the list,
 which can be written as a list of comma-separated values (items) between square brackets.
Lists might contain items of different types, but usually the items all have the same type.
list is mutable. 
tuple is immutable. (no add and no deletion)
"""

print(" List Concepts ")
# ==========================================================================
print('=' * 5, 'Available functions ', '=' * 5)
#  available function of list objects
for func in dir(list):
    if not (func.startswith('__') and func.endswith('__')):
        print('[*] {}'.format(func))

print(" CRUD ")
print('=' * 5, 'Create List object ', '=' * 5)

# empty list
list1 = list()
list2 = []
my_list = [1, 2, 3, 4, 5]
my_list2 = [i for i in range(10, 21, 1)]

print(list1, list2, my_list, my_list2)
# ==========================================================================
print('=' * 5, 'Access list object ', '=' * 5)
"""
Forward index and backward index
 0, 1, 2, 3
[1, 2, 3, 4]
-4, -3, -2, -1
"""
print(my_list[1])  # get the index value = 1
print(my_list[1:4])  # get the index value from
print(my_list[-1])  # get the last element
print(my_list2[::-1])  # get element in reverse order
print(my_list2[:-2:-1])  # get element in reverse order between -1 to -2
print(my_list2[2::-1])  # get element in reverse order from index = 2

# ==========================================================================
print('=' * 5, 'Add/Modify/Remove value to list object ', '=' * 5)
my_list.append(6)
my_list.append(7)
temp = [8, 9, 1, 1, 1]
my_list.extend(temp)  # my_list += temp
my_list.append(222)
print(my_list)
my_list.insert(0, 111)  # modify the value at the given index
# my_list[0] = 111
print(my_list)

print('index')
print(my_list.index(111))  # to get index of the value
print(my_list.index(1))
print('count')
print(my_list.count(1))  # get total occurrence of the value

print('pop')
my_list.pop()
my_list.pop()
print(my_list)
my_list.pop(2)  # remove the value from an given index. Default is -1
print(my_list)

print('sorting ASC')
my_list.sort()  # sorting
print(my_list)
print('sorting DESC')
my_list.sort(reverse=True)  # sorting
print(my_list)

print('remove')
my_list.remove(111)  # find and remove the value
my_list.remove(1)  # if more than 2 elements, removes the first occurrence
print(my_list)

my_list.reverse()  # reverse order
print(my_list)

my_list.clear()  # delete all values
print(my_list)
exit()
