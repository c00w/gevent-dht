import gevent.monkey
gevent.monkey.patch_all()

import socket, gevent, json, node, uidlib
from protocol import Protocol, Connect
from finger import FingerTable
from set_store import SetHandler



class NetworkListener():
    def __init__(self, start_addr, port=8338, ip='127.0.0.1'):
        #Special node which talks about ourselves
        self.port = port
        self.ip = ip
        self.node = node.Node(uidlib.new_uid(), ip, port, None)
        
        #Handler Classes
        self.finger = FingerTable(self.node)
        self.set_handler = SetHandler(self.finger)
        
        #Set up the listening socket
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind(( self.ip, self.port))
        self._s.listen(5)
        
        gevent.spawn(self._accept)
        gevent.spawn(self._ask_help)
        
        if start_addr:
            Connect(self.finger, self.set_handler, start_addr)
        Connect(self.finger, self.set_handler, ip + ":" + str(port))
        
    def _accept(self):
        while True:
            conn, addr = self._s.accept()
            self._handle(conn, addr)
                
    def _handle(self, conn, addr):
        Protocol(conn, ":".join((addr[0], str(addr[1]))), self.finger, self.set_handler)
        
    def _ask_help(self):
        while True:
            needed = self.finger.get_levels()
            for level in needed:
                self.finger.level_send(level, 'REQ_LEVEL ' + str(level))
            gevent.sleep(60)
        
import unittest

class TestNetwork(unittest.TestCase):
    def testConnection(self):
        net = NetworkListener(None)
        net2 = NetworkListener(net.node.addr, port = 8337)
        with gevent.Timeout(1) as timeout:
            while len(net.finger.known) == 0:
                gevent.sleep()
        self.assertTrue(len(net.finger.known) != 0)
        
if __name__ == "__main__":
    unittest.main()  
                
