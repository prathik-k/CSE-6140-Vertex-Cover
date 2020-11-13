import networkx as nx

def createGraph(fname):

    with open(fname) as f:
        next(f)
        lines = f.read().splitlines()
    G = nx.parse_adjlist(lines,create_using = nx.MultiGraph(),nodetype=str)     
    return G


    


