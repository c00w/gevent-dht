import json, gevent.queue

def SetHandler():
    def __init__(self, finger):
        self.finger = finger
        self.dict = {}
        self.queues = {}
        
    def check_updates(self):
        known = len(self.finger.known)
        while True:
            if len(self.finger.known != known):
                known = len(self.finger.known)
                for k,v in self.dict:
                    self.update(k,v)
            gevent.sleep(0.1)
        
    def get(self, key):
        self.queue[key] = qevent.queue.Queue(0)
        self.finger.send(hash(key) % int(32 * 'F', 16), 'GET ' + json.dumps(key))
        result = self.queue[key].get()
        del self.queue[key]
        return result
        
    def set(self, key, value):
        self.finger.send(hash(key) % int(32 * 'F', 16), 'SET ' + json.dumps([key, value]))
        
    def update(self, key, value):
        self.finger.send(hash(key) % int(32 * 'F', 16), 'SET ' + json.dumps([key, value]))
        
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
                if type(item) is type(set()):
                    item = list(item)
                proto.send('RES ' +  json.dumps([key,self.dict[key]]))
            proto.send('RES ' + json.dumps([key, None]))
            
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
            
        if msg[0:3] in ['UPD']:
            _, item = msg.split(' ', 1)
            key, value = json.loads(item)
            if key not in self.dict:
                self.dict[key] = value
            
            
        
