"""
A Context Manager allows a programmer to perform required activities, automatically, while entering or exiting a Context.

For example, opening a file, doing few file operations, and closing the file is manged using Context Manager as shown below.


with open('sample.txt', 'w') as fp:

    content = fp.read()

The keyword with is used in Python to enable a context manager. It automatically takes care of closing the file.

Context Manager...
Consider the following example, which tries to establish a connection to a database, perform few db operations and finally close the connection.
Example 1

import sqlite3
try:
    dbConnection = sqlite3.connect('TEST.db')
    cursor = dbConnection.cursor()
    '''
    Few db operations
    ...
    '''
except Exception:
    print('No Connection.')
finally:
    dbConnection.close()

Context Manager...
Example 2

import sqlite3
class DbConnect(object):
    def __init__(self, dbname):
        self.dbname = dbname
    def __enter__(self):
        self.dbConnection = sqlite3.connect(self.dbname)
        return self.dbConnection
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dbConnection.close()
with DbConnect('TEST.db') as db:
    cursor = db.cursor()
    '''
   Few db operations
   ...
    '''

"""

from contextlib import contextmanager


@contextmanager
def context():
    print('Entering Context')
    yield
    print("Exiting Context")


with context():
    print('In Context')

import zipfile


# Define 'writeTo' function below, such that
# it writes input_text string to filename.

def writeTo(filename, input_text):
    with open(filename, 'w') as fp:
        fp.write(input_text)


# Define the function 'archive' below, such that
# it archives 'filename' into the 'zipfile'
def archive(zfile, filename):
    with zipfile.ZipFile(zfile, 'w') as zp:
        zp.write(filename)


import subprocess


def run_process(cmd_args):
    with subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        out, err = p.communicate()
    return out
