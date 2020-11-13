import networkx as nx
import time
import random
from random import shuffle
from utils import createGraph

def isValidVC(VC,G):
    return all(u in VC or v in VC for u, v in G.edges())

def hc(filename,maxtime=600,seed=10):
    random.seed(a=seed)
    G = createGraph(filename)
    pqueue = deque(sorted(G.degree, key=lambda x: x[1]),maxlen = len(G))
    VC = set(G.nodes())
    term_time = time.time() + maxtime
    while len(pqueue)>0 and time.time()<term_time:
        currMinDeg = pqueue[0][1]
        currList = [pqueue.popleft()[0]]
        while len(pqueue)>0 and pqueue[0][1]==currMinDeg:
            currList.append(pqueue.popleft()[0])
        shuffle(currList)
        while(len(currList)>0):
            node = currList.pop()
            VC.remove(node)
            if isValidVC(VC,G):
                continue
            else:
                VC.add(node) 

    return VC





        

        
        

