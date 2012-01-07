if __name__ == "__main__":
    import gevent.monkey
    gevent.monkey.patch_all()

import json, gevent.queue, gevent

class SetHandler():
    def __init__(self, finger):
        self.finger = finger
        self.dict = {}
        self.queue = {}
        gevent.spawn(self.check_updates)
        
    def check_updates(self):
        known = len(self.finger.known)
        while True:
            if len(self.finger.known) != known:
                known = len(self.finger.known)
                for k in self.dict:
                    self.update(k,self.dict[k])
            gevent.sleep(0.1)
        
    def get(self, key):
        self.queue[key] = gevent.queue.Queue(0)
        self.finger.send(hash(key) % int(32 * 'F', 16), 'GET ' + json.dumps(key))
        result = self.queue[key].get()
        del self.queue[key]
        return result
        
    def set(self, key, value):
        self.finger.send(hash(key) % int(32 * 'F', 16), 'SET ' + json.dumps([key, value]))
        
    def update(self, key, value):
        self.finger.send(hash(key) % int(32 * 'F', 16), 'UPD ' + json.dumps([key, value]))
        
    def add(self, key, value):
        self.finger.send(hash(key) % int(32 * 'F', 16), 'ADD ' + json.dumps([key, value]))
        
    def handle_msg(self, proto, msg):
        if msg[0:3] not in ['GET', 'SET', 'ADD', 'RES', 'UPD']:
            return
            
        if msg[0:3] in ['GET']:
            _, key = msg.split(' ', 1)
            key = json.loads(key)
            if key in self.dict:
                item = self.dict[key]
                proto.send('RES ' +  json.dumps([key,item]))
            proto.send('RES ' + json.dumps([key, None]))
            
        if msg[0:3] in ['SET']:
            _, item = msg.split(' ', 1)
            key, value = json.loads(item)
            self.dict[key] = value
            
        if msg[0:3] in ['ADD']:
            _, item = msg.split(' ', 1)
            key, value = json.loads(item)
            if key not in self.dict:
                self.dict[key] = []
            self.dict[key].append(value)
            
        if msg[0:3] in ['RES']:
            _, item = msg.split(' ', 1)
            key, value = json.loads(item)
            if key in self.queue:
                self.queue[key].put(value)
            
        if msg[0:3] in ['UPD']:
            _, item = msg.split(' ', 1)
            key, value = json.loads(item)
            if key not in self.dict:
                self.dict[key] = value
            
import unittest

class TestStore(unittest.TestCase):
    def testConnection(self):
        from network import NetworkListener
        net = NetworkListener(None, port = 8345)
        net2 = NetworkListener(net.node.addr, port = 8346)
        while len(net.finger.known) < 2:
            gevent.sleep()
        print net.finger.known
        net2.set_handler.set('hi','bar')
        net2.set_handler.set('lp_blah', ['hi'])
        net2.set_handler.add('lp_blah', 'bar')
        gevent.sleep(1)
        self.assertTrue(net.set_handler.get('hi') == 'bar')
        self.assertTrue(net.set_handler.get('lp_blah') == ['hi','bar'])

if __name__ == "__main__":
    unittest.main()  
