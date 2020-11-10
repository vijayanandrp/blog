
# -*- coding: utf-8 -*-
import re

print('\n Split sentence by space ', '\n', '-'*35)
print(re.split(r'\s+', 'here are some words'))
print(re.split(r'[ ]+', 'here are some words'))

print(re.split(r's', 'here are some words'))
print(re.split(r'(s)', 'here are some words'))

print('\n Split sentence by with out numbers ', '\n', '-'*35)
print(re.split(r'\d+', 'k10Z18i13Q19u'))
print(re.split(r'[0-9]+', 'k10Z18i13Q19u'))


print('\n Conditional based Pattern split ', '\n', '-'*35)
print(re.split(r'[a-f]', 'asfw;adfgsltir;isprtafrrtradgksbcvijay;ADFUJFGAAVJY'))
print(re.split(r'[a-f][a-f]', 'asfw;adfgsltir;isprtafrrtradgksbcvijay'))
print(re.split(r'[a-fA-F]', 'asfw;adfgsltir;isprtafrrtradgksbcvijay;ADFUJFGAAVJY'), re.I|re.M)
print(re.split(r'[a-fA-F][a-fA-F]', 'asfw;adfgsltir;isprtafrrtradgksbcvijay;ADFUJFGAAVJYaAAnnd'), re.I|re.M)


print('\n Numbers ', '\n', '-'*35)
print(re.findall(r'\d+', 'k10Z18i13Q19u'))
print(re.findall(r'[0-9]+', 'k10Z18i13Q19u'))

# digits
# {5} = exact number of
# {1,60} range on number
# * = 0 or more
# + = 1 or more
# ? = 0 or 1 of

print(re.findall(r'\d{1}', 'k10Z18i13Q19u'))
print(re.findall(r'\d{1,5}', 'k10Z18i13Q19u'))


# \s - space
# \w word
# \d digits
# \D non-digits
# \S non-space
print(re.findall(r'\d{1,6}\s\w+\s\w+\s\d{1,7}', '6/403 karur india 639002'))


# encoding example
# url: https://docs.python.org/3/reference/lexical_analysis.html#encoding-declarations
# http://stackoverflow.com/questions/14682933/chinese-and-japanese-character-support-in-python

test1 = '# -*- coding: UTF-8 -*-'
test2 = '# -*- encoding: UTF-8 -*-'
test3 = '# -*- coding=UTF-8 -*-'
test4 = '# -*- encoding= UTF-8 -*-'
test5 = '# -*- encoding = UTF-8 -*-' # WRONG ONE

print(re.split(r'coding[=:]\s*([-\w.]+)', test1))
print(re.split(r'coding[=:]\s*([-\w.]+)', test2))
print(re.split(r'coding[=:]\s*([-\w.]+)', test3))
print(re.split(r'coding[=:]\s*([-\w.]+)', test4))
print(re.split(r'coding[=:]\s*([-\w.]+)', test5))
# print(re.split(r'coding[=:]\s*([-\w.]+)', test2))

#!/usr/bin/env python3.5
# encoding: utf-8
# -*- coding: utf-8 -*-
ru = u'\u30EB'
print(ru)
# encoding: utf-16

ru = u'ル'
print(ru)


path = u"E:\Test\は最高のプログラマ"
print(path)

ch='中国 (简体中文 )'
print(ch)

ch='香港特別行政區'
print(ch)

"""
https://docs.python.org/3/reference/lexical_analysis.html#encoding-declarations
-------------------------------------------------------------------------------------
2.1.4. Encoding declarations
If a comment in the first or second line of the Python script matches the regular expression coding[=:]\s*([-\w.]+),
this comment is processed as an encoding declaration;
the first group of this expression names the encoding of the source code file.
The encoding declaration must appear on a line of its own.
If it is the second line, the first line must also be a comment-only line.
The recommended forms of an encoding expression are

# -*- coding: <encoding-name> -*-
which is recognized also by GNU Emacs, and

# vim:fileencoding=<encoding-name>
which is recognized by Bram Moolenaar’s VIM.

If no encoding declaration is found, the default encoding is UTF-8.
In addition, if the first bytes of the file are the UTF-8 byte-order mark (b'\xef\xbb\xbf'),
the declared file encoding is UTF-8 (this is supported, among others, by Microsoft’s notepad).

If an encoding is declared, the encoding name must be recognized by Python.
The encoding is used for all lexical analysis, including string literals, comments and identifiers.
"""