

values = {'aijqy': 1, 'bkr': 2, 'cgls': 3, 'dtm': 4, 'ehnx': 5, 'uvw': 6, 'oz': 7, 'fp': 8}

values  =  dict((char, values[key]) for key in values.keys() for char in key)

print(values, len(values))

while 1:
    name =  str(input(">> Please enter your name: "))
    _numbers = [ values[char] for char in name.lower().strip() if char in values.keys()]
    print(name, ' = ', sum(_numbers))
