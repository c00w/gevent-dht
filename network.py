import socket, gevent, json, node, uidlib
from protocol import Protocol
from finger import FingerTable

class NetworkListener():
    def __init__(self, initial_node, port=8338, ip='127.0.0.1'):
        #Special node which talks about ourselves
        self.node = node.Node(uidlib.new_uid(), ip, port, None)
        self.finger = FingerTable(self.node)
        self.port = port
        self.ip = ip
        
        #Set up the listening socket
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind((self.port, self.ip))
        self._s.listen(5)
        
        gevent.spawn(self._accept)
        gevent.spawn(self._ask_help)
        
    def _accept(self):
        while True:
            conn, addr = self._s.accept()
            self._handle(conn, addr)
                
    def _handle(self, conn, addr):
        Protocol(conn, addr, self.finger)
        
    def _ask_help(self):
        while True:
            needed = self.finger.get_levels()
            for level in needed:
                self.finger.level_send(level, 'REQ_LEVEL ' + str(level))
            gevent.sleep(60)
        
                
                
