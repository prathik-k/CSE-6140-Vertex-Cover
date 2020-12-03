import networkx as nx
import time
import random
from random import shuffle
from utils import *
from collections import deque

'''
This file implements the approximation algoritthm to find the minimum vertex cover for an input graph.
TEAM 22, Prathik
Language: Python 3
Executable: python main.py  -inst jazz.graph -alg ls1 -time 600 -seed 10
The output is two files: *.sol and *.trace created
*.sol --- record the size of optimum vertex cover and the nodes in it.
*.trace --- record all the optimum solution found during the search and the time it was found
'''
def hc(filename,maxTime=600,seed=10):
    fname = "DATA/"+filename
    random.seed(a=seed)
    G = createGraph(fname)
    '''
    Defining a priority queue that contains all nodes in the graph in increasing order of node degree.
     The first items to be popped are the nodes with least degree.
    '''
    degrees = dict(sorted(G.degree().items(), key=lambda item: item[1]))
    pqueue = deque(degrees.items())
    VC = set(G.nodes())
    startTime = time.time()
    endTime = startTime + maxTime
    solTrace = dict()
    '''
    This loop is terminated either when maxtime is reached, or 
    the priority queue is empty. Note that the timestamp is recorded within each nested
    loop also, since in some cases the nested loops take times longer than the recording interval (0.01s) to run.
    '''
    while len(pqueue)>0 and time.time()<endTime:
        solTrace[round(time.time()-startTime,2)] = len(VC)
        currMinDeg = pqueue[0][1]
        currList = [pqueue.popleft()[0]]
        while len(pqueue)>0 and pqueue[0][1]==currMinDeg and time.time()<endTime:
            solTrace[round(time.time()-startTime,2)] = len(VC)
            currList.append(pqueue.popleft()[0])
        '''
        Shuffling the contents of the current list, in which all nodes have the same degree.
        This procedure utilizes the specified random seed.
        '''
        shuffle(currList)
        while(len(currList)>0) and time.time()<endTime:
            solTrace[round(time.time()-startTime,2)] = len(VC)
            node = currList.pop()
            VC.remove(node)
            '''
            Checking whether the removal of the node from the graph still yields a valid VC?
            '''
            if isValidVC(VC,G):
                continue
            else:
                VC.add(node)
    print(VC,list(solTrace.items()))
    return VC,list(solTrace.items())





        

        
        

