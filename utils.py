import networkx as nx

def createGraph(fname):
    with open(fname) as f:
        next(f)
        lines = f.read().splitlines()
    
    G = nx.Graph()
    for i in range(len(lines)):
        nodes = map(int,lines[i].split())
        edges = [(i+1,v) for v in nodes]
        G.add_edges_from(edges)    
    return G

def isValidVC(VC,G):
    return all(u in VC or v in VC for u, v in G.edges())

def write_to_file(VC,filename,alg,maxtime,seed,solTrace):
    fname = "results/"+filename+"_"+alg+"_"+str(maxtime)+"_"+str(seed)+".sol"
    VC = list(map(str,VC))
    with open(fname, "w") as f:
        f.write(str(len(VC)) + "\n")
        f.write(str(",".join(list(VC))))
    
    traceFile = "results/"+filename+"_"+alg+"_"+str(maxtime)+"_"+str(seed)+".trace"
    with open(traceFile, "w") as f:
        for trace in solTrace:
            line = str(trace[0])+","+str(trace[1])+"\n"
            f.write(line)
    


    


