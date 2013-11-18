import sys
import re

msgs    = {}
nodes = {}
id = 0
msg2rx_nodes = {}
count = 0
prefixes = {}        

def parseSignal(line):
    global count, id, msg2rx_nodes
    if id not in msgs:
        print id, "not in", msgs
        exit(-1)
    msgs[id]['signals'].append(line)
    name, colon, start_length, resolution, srange, percent, rest = re.split(r'\s+', line, 6)
    node_list = rest.split()[-1]
    rx_nodes = node_list.split(',')
    #if len(rx_nodes) > 1: print rx_nodes
    if id in msg2rx_nodes:
        msg2rx_nodes[id].append(rx_nodes)
    else:
        msg2rx_nodes[id] = [] + rx_nodes
    #count = count + 1
    #if count < 2: print line
    
def parseMessage(line):
    global count, id
    id_str, name_colon, dlc, node = re.split(r'\s+', line)
    id = int(id_str)
    #print hex(int(id)), msg_colon[:-1], dlc, ecu
    if id in msgs:
        print('Duplicate ID', id)
        exit(-1)
    msgs[id] = {}
    msgs[id]['name'] = name_colon[:-1]
    msgs[id]['signals'] = []
    msgs[id]['node'] = node
    msgs[id]['dlc'] = dlc
    if node in nodes:
        nodes[node] = nodes[node] + 1
    else:
        nodes[node] = 1
    #count = count + 1
    #if count < 2: print line

def parseLine(line):
    line = line.strip()
    if line == '': return
    fields = re.split(r'\s+', line, 1)
    if fields[0] == 'BO_':
        parseMessage(fields[1])
    elif fields[0] == 'SG_':
        parseSignal(fields[1])
    if fields[0] not in prefixes:
        prefixes[fields[0]] = 1
    else:
        prefixes[fields[0]] = prefixes[fields[0]] + 1

def print_tx_msgs(node):
    #print('Transmit messages of '+node+' :-')
    if node == '':
        node_msgs = msgs
    else:
        node_msgs = filter(lambda x: msgs[x]['node'] == node, msgs)
    for nm in node_msgs:
        print hex(nm), msgs[nm]['name']
    print

def print_rx_msgs(node):
    #print('Receive messages of '+node+' :-')
    for id in sorted(msg2rx_nodes):
        if(node in msg2rx_nodes[id]):
            print hex(id), msgs[id]['name']
    print

def print_nodes():
    for node in nodes: print node

def print_signal(line):
    name, colon, start_length, scale_offset, min_max, units, rx_nodes = re.split(r'\s+', line, 6)
    start, rest = start_length.split('|', 1)
    length, rest = rest.split('@', 1)
    scale, offset = scale_offset[1:-1].split(',')
    smin, smax    = min_max[1:-1].split('|',1)
    print ';'.join([name, start, length, rest[0], rest[1], scale, offset, smin, smax, units, rx_nodes])

def print_signals():
    print 'name;start-bit;length;endianess;sign;scale;offset;min;max;units;rx-nodes'
    for id in msgs:
        for s in msgs[id]['signals']:
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

dbc_path = sys.argv[1]
with open(dbc_path) as f:
    while True:
        line = f.readline()
        if not line: break
        parseLine(line)
        #if count > 5000: break
#print(prefixes)

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


