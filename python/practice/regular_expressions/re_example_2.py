#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import re
from urllib import request

sites = 'google yahoo bbc msn'.split()

for site in sites:
    print('Searching ' + site.upper())
    try:
        u = request.urlopen('https://www.' + site + '.com')
    except Exception as err:
        print('Error while opening {}.com - {}'.format(site, str(err)))
        continue
    text = u.read()
    title = re.findall(r'<title>+.*</title>+',
                       str(text),
                       re.I|re.M)
    
    print(title, '\n\n')
