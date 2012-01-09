import gevent, gevent.queue, socket, time
from node import Node

def addr_2_host_port(addr):
    host = ":".join(addr.split(':')[:-1])
    port = addr.split(':')[-1]
    return host, int(port)

def Connect(finger, set_handler, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr_2_host_port(addr)))
    return Protocol(s, addr, finger, set_handler)

class Protocol():
    def __init__(self, conn, addr, finger, set_handler):
        self.remote_addr = addr
        self.remote_conn = conn
        self.finger = finger
        self.Node = None
        self.set_handler = set_handler
        
        #Queues and generators for message handling
        self.recv_gen = self.recv_generator(conn)
        self.send_queue = gevent.queue.Queue()
        
        #Get address and port
        self.host, self.port = addr_2_host_port(addr)
        
        #Spawn handler threads.
        gevent.spawn(self.local_handle)
        gevent.spawn(self.net_handle)
        gevent.spawn(self.check_alive)
        
        self.send('UIDRESP ' + self.finger.self.uid)
        
    def check_alive(self):
        while True:
            gevent.sleep(60*1)
            if (time.time() - self.Node.last_seen) > 60:
                self.send('PING')
            if (time.time() - self.Node.last_seen) > 60*5:
                if self.Node:
                    self.finger.remove(self.Node)
                del self
                return
        
    def send(self, msg):
        self.send_queue.put(msg)
        
    def recv_generator(self, conn):
        msg = ''
        while True:
            new_data = conn.recv(32)
            msg += new_data
            if '|' in msg:
                length, remainder = msg.split('|', 1)
                length = int(length)
                if len(remainder) < length:
                    continue
                
                yield remainder[0:length]
                msg = remainder[length:len(remainder)]
        
    def net_handle(self):
        "Handle remote network messages"
        for msg in self.recv_gen:
            self.net_msg_handle(msg)
            
    def local_handle(self):
        "Handle requests for messages to be sent"
        for item in self.send_queue:
            self.net_msg_send(item)
            
    def net_msg_send(self, item):
        "Clean messages so they don't mess up the protocol"
        #print 'SENT: ' + item
        msg = str(len(item)) + '|' + item
        self.remote_conn.send(msg)
        
    def net_msg_handle(self, msg):
        if msg[0:7] in ['UIDRESP']:
            _, uid = msg.split(' ', 1)
            if self.Node == None:
                self.Node = Node(uid, self.host, self.port, self)
            self.finger.add(self.Node)
            
        if msg[0:6] in ['UIDREQ']:
            resp = 'UIDRESP ' + self.finger.self.uid
            self.send(resp)
            
        if msg[0:4] in ['PING']:
            self.send('PONG')
        
        if msg[0:4] in ['PONG']:
            pass
            
        if self.Node == None:
            self.send('UIDREQ')
            return
        else:
            self.Node.seen()
            
        if msg[0:9] in ['REQ_LEVEL']:
            _, level = msg.split(' ', 1)
            node = self.finger.get_node_from_level(int(level), self.Node.uid)
            if node:
                resp = 'RESP_LEVEL ' + str(node.uid) + " " + self.host + ":" + str(self.port)
                self.send(resp)
                
        if msg[0:10] in ['RESP_LEVEL']:
            _, uid, addr = msg.split(' ', 1)
            Connect(self.finger, self.set_handler, addr)
            
        self.set_handler.handle_msg(self, msg)
            
    def __del__(self):
        self.send_queue.put(StopIteration)
        self.remote_conn.shutdown()
        self.remote_conn.close()
        
        
class LoopBackProtocol(Protocol):
    """
    Protocol for talking to yourself
    """
    def __init__(self, addr, finger, set_handler):
        self.remote_addr = addr
        self.finger = finger
        self.Node = None
        self.set_handler = set_handler
        
        #Queues and generators for message handling
        self.recv_gen = gevent.queue.Queue()
        self.send_queue = gevent.queue.Queue()
        
        #Get address and port
        self.host, self.port = addr_2_host_port(addr)
        
        #Spawn handler threads.
        gevent.spawn(self.local_handle)
        gevent.spawn(self.net_handle)
        gevent.spawn(self.check_alive)
        
        self.send('UIDRESP ' + self.finger.self.uid)
        
    def net_msg_send(self, item):
        "Send messages locally so we can talk to ourselves"
        self.recv_gen.put(item)
        
import unittest

class TestProtocol(unittest.TestCase):
    def testaddr(self):
        self.assertTrue(addr_2_host_port("127.0.0.1:80") == ("127.0.0.1", 80))
        self.assertTrue(addr_2_host_port("fe80::1234:80") == ("fe80::1234", 80))
       
if __name__ == "__main__":
    unittest.main()
