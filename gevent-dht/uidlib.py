"""
Handles uid creation and conversion to integer types
"""

from hashlib import md5
from os import urandom

def new_uid():
    a = md5()
    a.update(urandom(16))
    return a.hexdigest()
    
def uid_2_num(uid):
    return long(uid, 16)
    
def num_2_uid(num):
    item = hex(num)[2:-1]
    return (32 - len(item)) * '0' + item
    
def distance(a, b):
    if isinstance(a, str):
        a = uid_2_num(a)
    if isinstance(b, str):
        b = uid_2_num(b)
    return a^b
    
import unittest

class uidtest(unittest.TestCase):
    def testTransforms(self):
        for i in range(100):
            a = new_uid()
            self.assertEqual(a, num_2_uid(uid_2_num(a)))
            
if __name__ == "__main__":
    unittest.main()

