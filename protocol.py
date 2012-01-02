import gevent
import gevent.queue

class Protocol():
    def __init__(self, conn, addr, finger):
        self.remote_addr = addr
        self.remote_conn = conn
        self.finger = finger
        self.conn = conn
        self.recv_gen = recv_generator(conn)
        self.send_queue = gevent.queue.Queue()
        self.host = ":".join(addr.split(':')[:-1])
        self.port = addr.split(':')[-1]
        gevent.spawn(self.local_handle)
        gevent.spawn(self.net_handle)
        gevent.spawn(self.check_alive)
        self.Node = None
        
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
            new_data = conn.recv(1024)
            msg += new_data
            if '|' in msg:
                item, msg = msg.split('|', 1)
                yield item
        
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
        self.remote_conn.send(item.replace('|', '') + '|')
            
    def net_msg_handle(self, msg):
        if msg[0:7] in ['UIDRESP']:
            _, uid = msg.split(' ', 1)
            if self.Node == None:
                self.Node = Node(uid, self.host, self.prot, self)
            self.finger.add(Node)
            
        if msg[0:6] in ['UIDREQ']:
            resp = 'UIDRESP ' + self.finger.self.uid
            self.send(resp)
            
        if msg[0:4] in ['PING']:
            self.send('PONG')
        
        if msg[0:4] in ['PONG']:
            pass
            
        if self.Node == None:
            self.send('UIDREQ')
        else:
            self.Node.seen()
            
    def __del__(self):
        self.send_queue.put(StopIteration)
        self.conn.shutdown()
        self.conn.close()
