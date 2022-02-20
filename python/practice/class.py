"""
You have read about function, higher order function, closures etc.
Now, it is time to learn about their scope.
Based on the scope, functions/methods are of two types.

They are:
1. Class methods
2. Static methods


An Abstract Base Class or ABC mandates the derived classes to implement specific methods from the base class.
It is not possible to create an object from a defined ABC class.
Creating objects of derived classes is possible only
when derived classes override existing functionality of all abstract methods defined in an ABC class.

"""


class Circle(object):
    no_of_circles = 0

    def __init__(self, radius):
        self.__radius = radius
        Circle.no_of_circles += 1

    @classmethod
    def getCirclesCount(cls):
        return cls.no_of_circles

    @staticmethod
    def square(x):
        return x ** 2

    def area(self):
        return 3.14 * self.square(self.__radius)


c1 = Circle(3.9)
print(c1.area())  # 47.7594

# Calling Static method
print(Circle.square(10))  # 100
print(c1.square(10))  # 100

c2 = Circle(5.2)
c3 = Circle(4.8)

print(c1.getCirclesCount())  # 3
print(c2.getCirclesCount())  # 3
print(c3.getCirclesCount())  # 3

# calling Class method
print(Circle.getCirclesCount())  # 3

# class A:
#
#     @staticmethod
#     def m1(self):
#         print('Static Method')
#
#     @classmethod
#     def m1(self):
#         print('Class Method')
#
#
# A.m1()  # Class Method


# from abc import ABC, abstractmethod
#
#
# class Shape(ABC):
#     @abstractmethod
#     def area(self):
#         pass
#
#     @abstractmethod
#     def perimeter(self):
#         pass
#
#
# # s1 = Shape() # Error
#
# class Circle(Shape):
#     def __init__(self, radius):
#         self.__radius = radius
#
#     @staticmethod
#     def square(x):
#         return x ** 2
#
#     def area(self):
#         return 3.14 * self.square(self.__radius)
#
#     def perimeter(self):
#         return 2 * 3.14 * self.__radius
#
#
# c1 = Circle(3.9)
# print(c1.area())
# print(c1.perimeter())
#
from abc import ABC, abstractmethod
#
#
# class A(ABC):
#
#     @abstractmethod
#     @classmethod
#     def m1(self):
#         print('In class A, Method m1.')
#
#
# class B(A):
#
#     @classmethod
#     def m1(self):
#         print('In class B, Method m1.')
#
#
# b = B()
# b.m1()
# B.m1()
# A.m1()

# from abc import ABC, abstractmethod
#
# class A(ABC):
#
#     @abstractmethod
#     def m1(self):
#         print('In class A, Method m1.')
#
#
# class B(A):
#
#     def m1(self):
#         print('In class B, Method m1.')
#
#
# class C(B):
#
#     def m2(self):
#         print('In class C, Method m2.')
#
#
# c = C()
# c.m1()
# c.m2()
from abc import ABC, abstractmethod


class A(ABC):

    @classmethod
    @abstractmethod
    def m1(self):
        print('In class A, Method m1.')


class B(A):

    @classmethod
    def m1(self):
        print('In class B, Method m1.')


b = B()
b.m1()
B.m1()
A.m1()


def s1(x, y):
    return x * y


class A:

    @staticmethod
    def s1(x, y):
        return x + y

    def s2(self, x, y):
        return s1(x, y)


a = A()
print(a.s2(3, 7))

from abc import ABC, abstractmethod


class A(ABC):

    @abstractmethod
    def m1(self):
        print('In class A, Method m1.')


class B(A):

    @staticmethod
    def m1(self):
        print('In class B, Method m1.')


b = B()
B.m1(b)

import inspect

from abc import ABC, abstractmethod


# Define the abstract class 'Animal' below
# with abstract method 'say'
class Animal(ABC):
    @abstractmethod
    def say(self):
        pass

# # Define class Dog derived from Animal
# # Also define 'say' method inside 'Dog' class
# class Dog(Animal):
#     def say(self):
#         return "I speak Booooo"
#
#
# if __name__ == '__main__':
#
#     if issubclass(Animal, ABC):
#         print("'Animal' is an abstract class")
#
#     if '@abstractmethod' in inspect.getsource(Animal.say):
#         print("'say' is an abstract method")
#
#     if issubclass(Dog, Animal):
#         print("'Dog' is dervied from 'Animal' class")
#
#     d1 = Dog()
#     print("Dog,'d1', says :", d1.say())
