"""
Hope you have understood from the previous course Functions and OOPs, what is a function? Now, let us understand what is a higher order function.

A Higher Order function is a function, which is capable of doing any one of the following things:

It can be functioned as a data and be assigned to a variable.

It can accept any other function as an argument.

It can return a function as its result.

The ability to build Higher order functions, allows a programmer to create Closures, which in turn are used to create Decorators.

********X***********

Decorators are evolved from the concept of closures.

A decorator function is a higher order function that takes a function as an argument and returns the inner function.

A decorator is capable of adding extra functionality to an existing function, without altering it.

"""
def outer(x, y):

    def inner1():
        return x+y

    def inner2():
        return x*y

    return (inner1, inner2)


(f1, f2) = outer(10, 25)

print(f1())
print(f2())

def outer(x, y):

    def inner1():
        return x+y

    def inner2(z):
        return inner1() + z

    return inner2


f = outer(10, 25)

print(f(15))


from functools import wraps

def decorator_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator_func
def square(x):
    return x**2

print(square.__name__)



def bind(func):
    func.data = 9
    return func


@bind
def add(x, y):
    return x + y


print(add(3, 10))
print(add.data)

exit()


def outer(func):
    def inner():
        print("Accessing: ", func.__name__)
        return func()

    inner.__name__ = func.__name__
    return inner


@outer
def greet():
    print("Hello!!")


print(greet.__name__)
exit()


def star(func):
    def wrapper(*args, **kwargs):
        print(3 * "*")
        func(*args, **kwargs)
        print(3 * "*")

    return wrapper


def hash1(func):
    def wrapper(*args, **kwargs):
        print(3 * "#")
        func(*args, **kwargs)
        print(3 * "#")

    return wrapper


@star
@hash1
def greet(msg):
    print(msg)


greet('hello')
exit()


def smart_divide(func):
    def wrapper(*args):
        a, b = args
        if b == 0:
            print('oops! cannot divide')
            return
        return func(*args)

    return wrapper


@smart_divide
def divide(a, b):
    return a / b


print(divide.__name__)
print(divide(4, 16))
print(divide(8, 0))
exit()


def outer(func):
    def inner():
        print("Accessing: ", func.__name__)
        return func()

    return inner


@outer
def greet():
    print("Hello!!")


# x = outer(greet)
# x()

# greet = outer(greet)
greet()
