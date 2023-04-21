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

In addition to character escapes and backreferences as described above, \g will use the substring matched by the group named name, as defined by the (?P...) syntax. \g uses the corresponding group number; \g<2> is therefore equivalent to \2, but isn’t ambiguous in a replacement such as \g<2>0. \20 would be interpreted as a reference to group 20, not a reference to group 2 followed by the literal character '0'. The backreference \g<0> substitutes in the entire substring matched by the RE.

```
