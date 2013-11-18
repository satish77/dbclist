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

def parseFile(filepath):
    msgs    = {}
    nodes = {}
    id = 0
    msg2rx_nodes = {}
    count = 0
    prefixes = {}        
    with open(filepath) as f:
        while True:
            line = f.readline()
            if not line: break
            parseLine(line)
            #if count > 5000: break
            #print(prefixes)

