"""
A Coroutine is generator which is capable of constantly receiving input data, process input data and may or may not return any output.

Coroutines are majorly used to build better Data Processing Pipelines.

Similar to a generator, execution of a coroutine stops when it reaches yield statement.

A Coroutine uses send method to send any input value, which is captured by yield expression.

Coroutine - Example...
As seen in Example1 and Example2, passing input to coroutine is possible only after the first next function call.

Many programmers may forget to do so, which results in error.

Such a scenario can be avoided using a decorator as shown in Example 3.


"""
def stringParser():
    while True:
        name = yield
        (fname, lname) = name.split()
        f.send(fname)
        f.send(lname)

def stringLength():
    while True:
        string = yield
        print("Length of '{}' : {}".format(string, len(string)))


f = stringLength(); next(f)

s = stringParser()
next(s)
s.send('Jack Black')

############
def TokenIssuer():
    tokenId = 0
    while True:
        name = yield
        tokenId += 1
        print('Token number of', name, ':', tokenId)


t = TokenIssuer()
next(t)
t.send('George')
t.send('Rosy')
t.send('Smith')


def TokenIssuer(tokenId=0):
    try:
        while True:
            name = yield
            tokenId += 1
            print('Token number of', name, ':', tokenId)
    except GeneratorExit:
        print('Last issued Token is :', tokenId)


t = TokenIssuer(100)
next(t)
t.send('George')
t.send('Rosy')
t.send('Smith')
t.close()


# Example 3

def coroutine_decorator(func):
    def wrapper(*args, **kwdargs):
        c = func(*args, **kwdargs)
        next(c)
        return c

    return wrapper


@coroutine_decorator
def TokenIssuer(tokenId=0):
    try:
        while True:
            name = yield
            tokenId += 1
            print('Token number of', name, ':', tokenId)
    except GeneratorExit:
        print('Last issued Token is :', tokenId)


t = TokenIssuer(100)
t.send('George')
t.send('Rosy')
t.send('Smith')
t.close()

def nameFeeder():
    while True:
        fname = yield
        print('First Name:', fname)
        lname = yield
        print('Last Name:', lname)

n = nameFeeder()
next(n)
n.send('George')
n.send('Williams')
n.send('John')


def stringDisplay():
    while True:
        s = yield
        print(s*3)


c = stringDisplay()
next(c)
c.send('Hi!!')

def stringDisplay():
    while True:
        s = yield
        print(s*3)


c = stringDisplay()
c.send('Hi!!') # TypeError: can't send non-None value to a just-started

# !/bin/python3

import sys


# Define the function 'coroutine_decorator' below
def coroutine_decorator(coroutine_func):
    def wrapper(*args, **kwdargs):
        c = coroutine_func(*args, **kwdargs)
        next(c)
        return c

    return wrapper


# Define the coroutine function 'linear_equation' below
@coroutine_decorator
def linear_equation(a, b):
    while True:
        x = yield
        print("Expression, {}*x^2 + {}, with x being {} equals {}".format(a, b, x, a * x ** 2 + b))


# Define the coroutine function 'numberParser' below
@coroutine_decorator
def numberParser():
    while True:
        x = yield
        equation1 = linear_equation(3, 4)
        equation1.send(float(x))
        equation2 = linear_equation(2, -1)
        equation2.send(float(x))
    # code to send the input number to both the linear equations


def main(x):
    n = numberParser()
    n.send(float(x))


if __name__ == "__main__":
    x = float(input())

    res = main(x);


