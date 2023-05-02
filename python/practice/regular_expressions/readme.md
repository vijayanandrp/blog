Regular expressions workouts 



 **Function** | **Description**                                                   
--------------|-------------------------------------------------------------------
 **findall**  | Returns a list containing all matches                             
 **search**   | Returns a Match object if there is a match anywhere in the string 
 **split**    | Returns a list where the string has been split at each match      
 **sub**      | Replaces one or many matches with a string       
 
 
https://cheatography.com/davechild/cheat-sheets/regular-expressions/

https://docs.python.org/3/library/re.html

https://res.cloudinary.com/dyd911kmh/image/upload/v1665049611/Marketing/Blog/Regular_Expressions_Cheat_Sheet.pdf


https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285

gsub is the normal sub in python - that is, it does multiple replacements by default.

The method signature for `re.sub is sub(pattern, repl, string, count=0, flags=0)`

If you want it to do a single replacement you specify count=1:

```python
In [2]: re.sub('t', 's', 'butter', count=1)
Out[2]: 'buster'
re.I is the flag for case insensitivity:

In [3]: re.sub('here', 'there', 'Here goes', flags=re.I)
Out[3]: 'there goes'
You can pass a function that takes a match object:

In [13]: re.sub('here', lambda m: m.group().upper(), 'Here goes', flags=re.I)
Out[13]: 'HERE goes'

result = re.sub(r"(\d.*?)\s(\d.*?)", r"\1 \2", string1)


import re
strings = ["Important text,      !Comment that could be removed", "Other String"]
[re.sub("(,[ ]*!.*)$", "", x) for x in strings]





>>> re.sub(r'(foo)', r'\1123', 'foobar')
'J3bar'

This works:

>>> re.sub(r'(foo)', r'\1hi', 'foobar')
'foohibar'

re.sub(r'(foo)', r'\g<1>123', 'foobar')
Relevant excerpt from the docs:

# In addition to character escapes and backreferences as described above, \g will use the substring matched by the group named name, as defined by the (?P...) syntax. \g uses the corresponding group number; \g<2> is therefore equivalent to \2, but isn’t ambiguous in a replacement such as \g<2>0. \20 would be interpreted as a reference to group 20, not a reference to group 2 followed by the literal character '0'. The backreference \g<0> substitutes in the entire substring matched by the RE.


>>> re.sub(r"\b\w",lambda m: m[0].upper(),"i am your")
'I Am Your'


>>> def my_replace(match):
...     match = match.group()
...     return match + str(match.index('e'))
...
>>> string = "The quick @red fox jumps over the @lame brown dog."
>>> re.sub(r'@\w+', my_replace, string)
'The quick @red2 fox jumps over the @lame4 brown dog.'




I wasn't aware you could pass a function to a re.sub() either. Riffing on @Janne Karila's answer to solve a problem I had, the approach works for multiple capture groups, too.

import re

def my_replace(match):
    match1 = match.group(1)
    match2 = match.group(2)
    match2 = match2.replace('@', '')
    return u"{0:0.{1}f}".format(float(match1), int(match2))

string = 'The first number is 14.2@1, and the second number is 50.6@4.'
result = re.sub(r'([0-9]+.[0-9]+)(@[0-9]+)', my_replace, string)

print(result)


>>> import re
>>> pat = r'@\w+'
>>> reduce(lambda s, m: s.replace(m, m + str(m.index('e'))), re.findall(pat, string), string)
'The quick @red2 fox jumps over the @lame4 brown dog.'





A solution without lambda

import re

def convert_func(matchobj):
    m =  matchobj.group(0)
    map = {'7': 'seven',
           '8': 'eight',
           '9': 'nine'}
    return map[m]

line = "7 ate 9"
new_line =  re.sub("[7-9]", convert_func, line)


import re

number_mapping = {'1': 'one',
                  '2': 'two',
                  '3': 'three'}
s = "1 testing 2 3"

print re.sub(r'\d', lambda x: number_mapping[x.group()], s)


text ="""
 DFFFFf                                                | XYYZZZ                    | AVRO   
 XXX__TEST                                                          | XXXX  | AVRO   
"""

import re
for x in re.findall(r'[|](.*)[|$]', text):
    print('--->', x)

```

```
