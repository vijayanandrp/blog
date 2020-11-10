from random import random
from math import sqrt, pi


def compute_pi(n):
    i, inside = 0, 0
    while i < n:
        x, y = random(), random()
        if sqrt(x**2 + y**2) <= 1:
            inside += 1
        i += 1
    
    ratio = 4.0 * inside/ n
    return ratio

if __name__ == '__main__':
    my_pi = compute_pi(10000000)
    print('My Pi: {0}, Error: {1}'.format(my_pi, my_pi - pi))

