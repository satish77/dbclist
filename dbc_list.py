import sys
import dbc
import re

def print_tx_msgs(node):
    #print('Transmit messages of '+node+' :-')
    if node == '':
        node_msgs =dbc. msgs
    else:
        node_msgs = filter(lambda x: dbc.msgs[x]['node'] == node,dbc. msgs)
    for nm in node_msgs:
        print hex(nm), dbc.msgs[nm]['name']
    print

def print_rx_msgs(node):
    #print('Receive messages of '+node+' :-')
    for id in sorted(dbc.msg2rx_nodes):
        if(node in dbc.msg2rx_nodes[id]):
            print hex(id),dbc. msgs[id]['name']
    print

def print_nodes():
    for node in dbc.nodes: print node

def print_signal(line):
    name, colon, start_length, scale_offset, min_max, units, rx_nodes = re.split(r'\s+', line, 6)
    start, rest = start_length.split('|', 1)
    length, rest = rest.split('@', 1)
    scale, offset = scale_offset[1:-1].split(',')
    smin, smax    = min_max[1:-1].split('|',1)
    print ';'.join([name, start, length, rest[0], rest[1], scale, offset, smin, smax, units, rx_nodes])

def print_signals():
    print 'name;start-bit;length;endianess;sign;scale;offset;min;max;units;rx-nodes'
    for id in dbc.msgs:
        for s in dbc.msgs[id]['signals']:
            print hex(id), ';',
            print_signal(s)
        
def show_help():
    print('Usage: '+sys.argv[0]+' <dbc path> command')
    print('''commands:
       nodes
       txmessages [node]
       rxmessages <node>
       signals
''')

if len(sys.argv) == 1:
    command = ""
else:
    command = sys.argv[2]

dbc.parseFile(sys.argv[1])

if command == 'nodes':
    print_nodes()
elif command == 'txmessages':
    if len(sys.argv) > 3:
        print_tx_msgs(sys.argv[3])
    else:
        print_tx_msgs('')
elif len(sys.argv) > 3 and command == 'rxmessages':
    print_rx_msgs(sys.argv[3])
elif command == 'signals':
    print_signals()
else:
    show_help()

'''
TODO: 
pretty print signals
change start bit to motorola format
support csv output for subsequent parsing
document output headers in help
'''


