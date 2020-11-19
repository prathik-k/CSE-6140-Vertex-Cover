import networkx as nx
import time
import random
from random import shuffle
from utils import *
from collections import deque



def hc(filename,maxTime=600,seed=10):
    fname = "DATA/"+filename
    random.seed(a=seed)
    G = createGraph(fname)
    pqueue = deque(sorted(G.degree, key=lambda x: x[1]),maxlen = len(G))
    VC = set(G.nodes())
    startTime = time.time()
    endTime = startTime + maxTime
    solTrace = dict()

    while len(pqueue)>0 and time.time()<endTime:
        solTrace[round(time.time()-startTime,2)] = len(VC)
        currMinDeg = pqueue[0][1]
        currList = [pqueue.popleft()[0]]
        while len(pqueue)>0 and pqueue[0][1]==currMinDeg and time.time()<endTime:
            currList.append(pqueue.popleft()[0])
        shuffle(currList)
        while(len(currList)>0) and time.time()<endTime:
            node = currList.pop()
            VC.remove(node)
            if isValidVC(VC,G):
                continue
            else:
                VC.add(node)
    return VC,list(solTrace.items())





        

        
        

