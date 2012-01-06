"""
Class to store node information.
The actual class which sends stuff is the protocol class
"""

import uidlib, time

class Node():
    """ Contains contact info """
    def __init__(self, uid, host, port, prot):
        self.uid = uid
        self.num = uidlib.uid_2_num(uid)
        self.host = host
        self.port = port
        self.prot = prot
        self.last_seen = -1
        
    def send(self, msg):
        self.prot.send(msg)
        
    def seen(self):
        self.last_seen = time.time()
        
    def __repr__(self):
        return '<Node ' + str((self.uid, self.host, self.port)) + ' >'
        
    def __lt__(self, a):
        if isinstance(a, Node):
            a = a.num
        return self.num < a
        
    def __le__(self, a):
        if isinstance(a, Node):
            a = a.num
        return self.num <= a
        
    def __gt__(self, a):
        if isinstance(a, Node):
            a = a.num
        return self.num > a
    
    def __ge__(self, a):
        if isinstance(a, Node):
            a = a.num
        return self.num >= a
        
    def __eq__(self, a):
        if isinstance(a, Node):
            a = a.num
        return self.num == a
        
    def __ne__(self, a):
        if isinstance(a, Node):
            a = a.num
        return self.num != a
        
    def __hash__(self):
        return hash(self.uid) ^ hash(self.host) ^ hash(self.port)
        
        
import unittest

class TestNode(unittest.TestCase):
    def testCreation(self):
        a = Node(uidlib.new_uid(), 'localhost', '8338', None)
        self.assertTrue(isinstance(a, Node))
        
    def testHashability(self):
        a = Node(uidlib.new_uid(), 'localhost', '8338', None)
        b = set([])
        b.add(a)
        
if __name__ == "__main__":
    unittest.main()
