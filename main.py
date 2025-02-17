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
    trans = open_file(filename)
    for tr in trans:
        tr_info = tr.split(';')
        tm.add_edge(tr_info[0],tr_info[1],label=tr_info[2])
    return tm

TM = gen_tm('./transitions.txt')
for u, v, d in TM.edges(data=True):
    print(f"Transition: {u} -> {v}, {d['label']}")
