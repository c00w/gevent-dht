This is a basic implementation of a dht using gevent.

There are two things you have to concern yourself with.
1.) Bootstrapping the network.
The following example creates a network of one node

-------------------------------------------------------------------
import gevent_dht
table = gevent_dht.distributedHashTable(None) #This tell the network it 
        # is the first node by default it listens on port 8339
        #
        
table['key_1'] = [1,2,3] #This sets a value in our hash table
for i in table['key_1']:
    print i #Prints 123
    
table.append('key_1', 4) #Adds an item to a list in a hash table
                         #Note if the key is not in the hash table
                         #It will put a list in place and then append 
                         #to it.
                         
#Now we are adding another node
    
other_clients_table = gevent_dht.distributedHashTable(
                    '127.0.0.1:8339', local_port = 8449)
    #Another client has connected. It supplied the address of 
    # a node in the network to connect with the preexisting network
    
for i in other_clients_table['key_1']:
    print i #Prints 1234

-------------------------------------------------------------------

So in order to connect to an existing network you must have a way to get an 
address of another member. It doesn't have to be the first node but needs 
to be a node in the network.

2.) Latency/ This may fail.

Keys are not guarenteed to persist forever, nodes may crash, the network 
may eat messages etc... While we are working in tcp/ip mode there may still 
be bizarre glitches. Always check for a return value of None.

Additionally due to the time it takes for messages to travel the network 
sometimes a key will not be immedietly available after you set it or
when you get the result back it may not be completely current.
