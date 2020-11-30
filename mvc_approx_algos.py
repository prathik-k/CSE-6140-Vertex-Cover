'''
This file implements the approximation algoritthm to find the minimum vertex cover for an input graph.
TEAM 22, Aarohi
Language: Python 3
Executable: python main.py  -inst jazz.graph -alg app -time 600 -seed 10
seed is not used though for approximation algorithm
The output is two files: *.sol and *.trace created
*.sol --- record the size of optimum vertex cover and the nodes in it.
*.trace --- record all the optimum solution found during the search and the time it was found
'''

import networkx as nx
import time
import random
from random import shuffle
from utils import createGraph
from collections import deque
import numpy as np

def approx_mvc(filename,maxTime=600,seed=10):
    fname = "DATA/"+filename
    random.seed(a=seed)
    G = createGraph(fname)

    # initialize all vertices as not visited
    visited = [False for i in range(len(G.nodes()))]
    startTime = time.time()
    endTime = startTime + maxTime
    solTrace = dict()

    vc_count = 0

    VC = np.zeros((1,len(G.nodes())))
    print((G.nodes()))

    while time.time()<endTime:
        # Consider all edges one by one
        for u in range(len(G.nodes())):
            # An edge is only picked when
		    # both visited[u] and visited[v]
		    # are false
            if not visited[u]:
                for v in G.neighbors(u+1):
                    if v == len(G.nodes()):
                        break
                    if not visited[v]:
                        # Add the vertices (u, v) to the
					    # result set. We make the vertex
					    # u and v visited so that all
					    # edges from/to them would
					    # be ignored
                        visited[v] = True
                        visited[u] = True
                        sol_check = 0
                        for check in range(len(G.nodes())):
                            if visited[check]:
                                sol_check += 1
                            solTrace[round(time.time()-startTime,2)] = sol_check
                        break
        for j in range(len(G.nodes())):
            if visited[j]:
                VC[0,vc_count] = j
                vc_count += 1
        VC_ret = VC[0,0:vc_count]
        break
    VC_ret = set([int(node) for node in VC_ret])
    return VC_ret, list(solTrace.items())
