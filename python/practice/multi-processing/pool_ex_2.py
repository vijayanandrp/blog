from random import random
from math import sqrt, pi
from multiprocessing import Pool
import time


def compute_pi(n):
    i, inside = 0,0
    while i < n:
        x = random()
        y = random()
        if sqrt(x*x + y*y) <= 1:
            inside += 1
        i += 1
    ratio = 4.0 * inside / n
    return ratio

if __name__ == '__main__':
    start = time.time()
    
    with Pool(processes=4) as p:
        pis = p.map(compute_pi, [10000000] * 4)
        print(pis)
        mypi = sum(pis)/4
        print('My Pi: {0}, Error: {1}'.format(mypi, mypi - pi))
    delta = time.time() - start
    
    print("--- %s seconds ---" % delta)
   
 
# Sample Result
'''
[3.1417304, 3.141578, 3.1409976, 3.1404092]

My Pi: 3.1411788, Error: -0.0004138535897930673

--- 52.89663076400757 seconds ---
'''