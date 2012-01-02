import socket, gevent
from protocol import Protocol
from finger import FingerTable
class Network():
    def __init__(self, port=8338, ip='127.0.0.1'):
        self.finger = FingerTable()
        self.port = port
        self.ip = ip
        
        #Set up the listening socket
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind((self.port, self.ip))
        self._s.listen(5)
        
        gevent.spawn(self._accept)
        
    def _accept(self):
        while True:
            conn, addr = self._s.accept()
            self._handle(conn, addr)
                
    def _handle(self, conn, addr):
        Protocol(conn, addr, self.finger)
        
    def connect(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        a = Protocol(s, host + ":" + port, self.finger)
        a.send('UIDRESP ' + self.finger.self.id)
        a.send('UIDREQ')
        
    def get_more_nodes(self):
        pass
                
                
