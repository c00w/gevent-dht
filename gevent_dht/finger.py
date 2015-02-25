import uidlib, math, gevent

class FingerTable():
    def __init__(self, self_node, min_count=1):
        self.known = set([])
        self.self = self_node
        self.table = []
        self.min_count = min_count
        self.max_level = int(self._uid_2_level(32*'F', 32*'0'))+1
        for i in range(self.max_level):
            self.table.append(set([]))
        
    def _above_zero(self, item):
        if item < 0: 
            return 0
        return item
        
    def _uid_2_level(self, uid, other_uid=None):
        """
        Convert a uid to a log level in the finger table
        """
        if other_uid == None:
            other_uid = self.self.uid
        level = int(self._above_zero(
                        math.log(
                            uidlib.distance(uid, other_uid)+0.1)
                        )
                    )
        return level
        
    def _level_check(self, level):
        """
        Make sure the level is inside the table range.
        """
        if level > len(self.table) - 1:
            for i in range(len(self.table)-1, level):
                self.table.append(set([]))
                self.max_level += 1
                
    def add(self, Node):
        """
        Add a node to our finger table
        """
        self.known.add(Node)
        level = self._uid_2_level(Node.uid)
        self._level_check(level)
        self.table[level].add(Node)
        
    def remove(self, Node):
        """
        remove a node from our finger table
        """
        if Node not in self.known:
            return
        self.known.remove(Node)
        level = self._uid_2_level(Node.uid)
        self.table[level].remove(Node)
        
    def get_levels(self):
        """
        return what distances we would like to get uids for
        """
        for i in range(len(self.table)):
            if len(self.table[i]) < self.min_count:
                yield int(i)
                
    def get_nodes(self):
        """
        return a list of nodes in the finger table so far
        """
        nodes = []
        for i in range(len(self.table)):
            for node in self.table[i]:
                host = """%s:%d""" % (node.host, node.port)
                nodes.append(host)
        return nodes
        
    def get_node_from_level(self, level, uid):
        """
        Gets the node which is a certain level away from another uid
        """
        for i in xrange(
            int(level-self._uid_2_level(uid)), 
            int(level+self._uid_2_level(uid))
            ): #Triangle Inequality
            if i < len(self.table) and i >=0:
                for node in self.table[i]:
                    if self._uid_2_level(node.uid, uid) == level:
                        return node
        return None
            
                
    def level_send(self, level, msg):
        """
        Send message to the node closest to that level
        """
        self._level_check(level)
        closest_node = None
        closest_level = 0
        for node in self.known:
            node_level = self._uid_2_level(node.uid)
            if not closest_node or abs(node_level - level) < closest_level:
                closest_node = node
                closest_level = abs(node_level - level)
            #Do a cooperative yield since this could take a while
            #gevent.sleep()
        if closest_node:
            closest_node.prot.send(msg)
                          
    def get_node(self, uid):
        """
        get closest node
        """
        level = self._uid_2_level(uid)
        self._level_check(level)
        
        #Check if we have an entry
        if len(self.table[level]):
            search = self.table[level]
        #Else find the closest node
        else:
            search = self.known
            
        close_node = None
        for node in search:
            if not close_node or uidlib.distance(node.uid, uid) < uidlib.distance(close_node.uid, uid):
                close_node = node
            
        return close_node  
               
    def send(self, uid, msg):
        """
        Sends to the node closest to that uid
        """
        
        node = self.get_node(uid)
        if node and node.prot:  
            node.prot.send(msg)
        
import unittest, node
Node = node.Node
class fingertest(unittest.TestCase):
    def testadds(self):
    
        finger = FingerTable(Node(uidlib.new_uid(), '', '', ''))
        Nodes = set([])
        
        for i in range(100):
            a = uidlib.new_uid()
            b = Node(a, '', '', '')
            Nodes.add(b)
            finger.add(b)
            
        for y in finger.get_levels():
            pass
            
        for x in Nodes:
            finger.remove(x)
            
        self.assertTrue(len(finger.known) == 0)
        
    def test_levels_needed(self):
        finger = FingerTable(Node(uidlib.new_uid(), '', '', ''))
        self.assertTrue(len([x for x in finger.get_levels()]) == finger.max_level)
        finger.add(Node(uidlib.new_uid(), '', '', ''))
        self.assertTrue(len([x for x in finger.get_levels()]) == finger.max_level-1)
            
            
if __name__ == "__main__":
    unittest.main()


