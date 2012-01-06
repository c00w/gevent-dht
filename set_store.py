import json, gevent.queue

def SetHandler():
    def __init__(self, proto):
        self.proto = proto
        self.dict = {}
        self.queues = {}
        
    def get(self, key):
        self.queue[key] = qevent.queue.Queue(0)
        self.finger.send(hash(key) % int(32 * 'F', 16), 'GET ' + json.dumps(key))
        result = self.queue[key].get()
        del self.queue[key]
        return result
        
    def set(self, key, value):
        self.finger.send(hash(key) % int(32 * 'F', 16), 'SET ' + json.dumps([key, value]))
        
    def add(self, key, value):
        self.finger.send(hash(key) % int(32 * 'F', 16), 'ADD ' + json.dumps([key, value]))
        
    def handle_msg(self, msg):
        if msg[0:3] not in ['GET', 'SET', 'ADD', 'RES']:
            return
            
        if msg[0:3] in ['GET']:
            _, key = msg.split(' ', 1)
            key = json.loads(key)
            if key in self.dict:
                item = self.dict[key]
                if type(item) is type(set())
                    item = list(item)
                self.proto.send('RES ' +  json.dumps([key,self.dict[key]))
            self.proto.send('RES ' + json.dumps([key, None]))
            
        if msg[0:3] in ['SET']:
            _, item = msg.split(' ', 1)
            key, value = json.loads(item)
            self.dict[key] = value
            
        if msg[0:3] in ['ADD']:
            _, item = msg.split(' ', 1)
            key, value = json.loads(item)
            if key not in self.dict:
                self.dict[key] = set()
            self.dict[key].add(value)
            
        if msg[0:3] in ['RES']:
            _, item = msg.split(' ', 1)
            key, value = json.loads(item)
            self.queue[key].put(value)
            
            
        
