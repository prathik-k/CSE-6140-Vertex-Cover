import networkx as nx

def createGraph(fname,path="/DATA"):
    G = nx.read_adjlist(fname,create_using = nx.MultiGraph(),nodetype=int)
    with open(path+fname) as f:
        first_line = f.readline().split()
    G.remove_edges_from([(int(first_line[0]),int(first_line[1])),(int(first_line[0]),int(first_line[2]))])
    G = gt.read_graph_from_csv(fname+path,directed=False,skip_first=False)
    return G

    


