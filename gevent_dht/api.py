import gevent
import network
import socket
import uidlib

class distributedHashTable():
    def __init__(self, first_node, local_port=8339, local_ip=''):
        """
        First_node is the address of the first computer to connect to
        If it is none then you are bootstrapping the network and this
        is the first node.
        
        local_port is the local port to bind to.
        Default 8339.
        
        local_ip is the interface to bind to.
        Default is '' which should bind all addrresses
        """
        
        self.listener = network.NetworkListener(first_node, local_port, local_ip)
        
    def __get_node_from_key(self, key):
        #Get its hash mod the id limit
        key_hash = hash(key) % int('F'*32, 16)
        node = self.listener.finger.get_node(key_hash)
        
    def __getitem__(self, key):
        """
        Get an item from the distributed hash table
        """
        
        node = self.__get_node_from_key(key)
        return node.set_handler.get(key)
        
    def __setitem__(self, key, value):
        """
        Set an item in the distributed hash table
        """
        
        node = self.__get_node_from_key(key)
        return node.set_handler.set(key, value)
        
    def append(self, key, value):
        """
        Remove item
        """
        node = self.__get_node_from_key(key)
        return node.set_handler.add(key, value)
        
