"""
Descriptors
===========
Python descriptors allow a programmer to create managed attributes.

In other object-oriented languages, you will find getter and setter methods to manage attributes.

However, Python allows a programmer to manage the attributes simply with the attribute name, without losing their protection.

This is achieved by defining a descriptor class, that implements any of __get__, __set__, __delete__ methods.

Properties
===========
Descriptors can also be created using property() type.

It is easy to create a descriptor for any attribute using property().

Syntax of defining a Property

property(fget=None, fset=None, fdel=None, doc=None)

where,

fget : attribute get method

fset : attribute set method

fdel – attribute delete method

doc – docstring

Property Decorators
===================
Descriptors can also be created with property decorators.

While using property decorators, an attribute's get method will be same as its name and will be decorated with property.

In a case of defining any set or delete methods, they will be decorated with respective setter and deleter methods.
"""


class A:

    def __init__(self, val):
        self.x = val

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        self.__x = val

    @x.deleter
    def x(self):
        del self.__x


a = A(7)
del a.x
print(a.x)

# !/bin/python3

import sys
import os


# Add Celsius class implementation below.
class Celsius:
    def __get__(self, obj, owner):
        return 5 * (obj.fahrenheit - 32) / 9

    def __set__(self, obj, value):
        obj.fahrenheit = 32 + 9 * value / 5


class Temperature:
    celsius = Celsius()

    def __init__(self, fahrenheit):
        self.fahrenheit = fahrenheit


# Add temperature class implementation below.


'''Check the Tail section for input/output'''

if __name__ == "__main__":
    with open(os.environ['OUTPUT_PATH'], 'w') as fout:
        res_lst = list()
        t1 = Temperature(int(input()))
        res_lst.append((t1.fahrenheit, t1.celsius))
        t1.celsius = int(input())
        res_lst.append((t1.fahrenheit, t1.celsius))
        fout.write("{}\n{}".format(*res_lst))

class EmpNameDescriptor:
    def __get__(self, obj, owner):
        return self.__empname

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError("'empname' must be a string.")
        self.__empname = value


class EmpIdDescriptor:
    def __get__(self, obj, owner):
        return self.__empid

    def __set__(self, obj, value):
        if hasattr(obj, 'empid'):
            raise ValueError("'empid' is read only attribute")
        if not isinstance(value, int):
            raise TypeError("'empid' must be an integer.")
        self.__empid = value


class Employee:
    empid = EmpIdDescriptor()
    empname = EmpNameDescriptor()

    def __init__(self, emp_id, emp_name):
        self.empid = emp_id
        self.empname = emp_name


e1 = Employee(123456, 'John')
print(e1.empid, '-', e1.empname)
e1.empname = 'Williams'
print(e1.empid, '-', e1.empname)
e1.empid = 76347322  # Raises  Read only error


class Employee:
    def __init__(self, emp_id, emp_name):
        self.empid = emp_id
        self.empname = emp_name

    def getEmpID(self):
        return self.__empid

    def setEmpID(self, value):
        if not isinstance(value, int):
            raise TypeError("'empid' must be an integer.")
        self.__empid = value

    empid = property(getEmpID, setEmpID)

    def getEmpName(self):
        return self.__empname

    def setEmpName(self, value):
        if not isinstance(value, str):
            raise TypeError("empname' must be a string.")

        self.__empname = value

    def delEmpName(self):
        del self.__empname

    empname = property(getEmpName, setEmpName, delEmpName)


e1 = Employee(123456, 'John')

print(e1.empid, '-', e1.empname)  # -> '123456 - John'

del e1.empname  # Deletes 'empname'

print(e1.empname)  # Raises 'AttributeError'


class A:

    def __init__(self, x):
        self.__x = x

    @property
    def x(self):
        return self.__x


a = A(7)
a.x = 10
print(a.x)


class Employee:
    def __init__(self, emp_id, emp_name):
        self.empid = emp_id
        self.empname = emp_name

    @property
    def empid(self):
        return self.__empid

    @empid.setter
    def empid(self, value):
        if not isinstance(value, int):
            raise TypeError("'empid' must be an integer.")
        self.__empid = value

    @property
    def empname(self):
        return self.__empname

    @empname.setter
    def empname(self, value):
        if not isinstance(value, str):
            raise TypeError("'empname' must be a string.")
        self.__empname = value

    @empname.deleter
    def empname(self):
        del self.__empname


e1 = Employee(123456, 'John')
print(e1.empid, '-', e1.empname)  # -> '123456 - John'
del e1.empname  # Deletes 'empname'
print(e1.empname)  # Raises 'AttributeError'


class A:

    def __init__(self, val):
        self.x = val

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        self.__x = val

    @x.deleter
    def x(self):
        del self.__x


a = A(7)
del a.x
print(a.x)