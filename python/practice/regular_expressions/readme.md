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

The method signature for re.sub is sub(pattern, repl, string, count=0, flags=0)

If you want it to do a single replacement you specify count=1:

In [2]: re.sub('t', 's', 'butter', count=1)
Out[2]: 'buster'
re.I is the flag for case insensitivity:

In [3]: re.sub('here', 'there', 'Here goes', flags=re.I)
Out[3]: 'there goes'
You can pass a function that takes a match object:

In [13]: re.sub('here', lambda m: m.group().upper(), 'Here goes', flags=re.I)
Out[13]: 'HERE goes'
