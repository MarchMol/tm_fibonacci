import networkx as nx
# ---- Handling del input ---- #
def tokenize(input):
    tokens = input.split(',')
    return tokens

# ---- Gneración de la Máquina ---- #
# Abrir archivo y convertirlo a array
def open_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]  # Removes newlines

# Transformar array en grafo
def gen_tm(filename):
    tm = nx.MultiDiGraph()
    accept = []
    start = ""
    trans = open_file(filename)
    for tr in trans:
        tr_info = tr.split(';')
        if(len(tr_info)==2): # Si solo hay 2, es definición de estado
            if (tr_info[0]=="start"):
                start = tr_info[1]
            elif (tr_info[0]=="accept"):
                accept.append(tr_info[1])
        elif(len(tr_info)==3): # si hay 3, es transición
            tm.add_edge(tr_info[0],tr_info[1],label=tr_info[2])
    return (accept, start, tm)

def get_transitions(TM,st):
    return [(dest, data["label"]) for _, dest, _, data in TM.out_edges(st, keys=True, data=True)]

def move_head(mv, head):
    if (mv =='R'):
        head+=1
    if(mv=='L'):
        head-=1
    return head

def derivation(tape, head, st):
    rslt = ""
    for index,ch in enumerate(tape):
        if(index==head):
            rslt+=" ["+st+"]->"
        rslt+=ch
    print(rslt)
    
def choose_transition(st, ch, trans):
    if (len(trans)==1):
        return trans[0]
    else:
        for tr in trans:
            if (tr[1].split(',')[0] == ch):
                return tr
def sim(tm, tape, start, accept):
    current_state = start
    head = 0
    
    while(not(current_state in accept)):
        if(head>=len(tape)):
            tape.append('_')
        derivation(tape, head, current_state)
        current_symbol = tape[head]
        trans = choose_transition(current_state, current_symbol,get_transitions(tm,current_state))
        to_state = trans[0]
        rd, wr, mv = trans[1].split(',')
        if (rd == current_symbol):
            tape[head] = wr
            head = move_head(mv,head)
            current_state = to_state
    derivation(tape, head, current_state)
            
      
        
tape = tokenize("#,1,#,1")
accept,start,TM = gen_tm('./transitions.txt')

sim(TM,tape,start, accept)