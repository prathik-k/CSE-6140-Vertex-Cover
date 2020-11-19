import networkx as nx
import time
import random
from random import shuffle
from utils import createGraph
from collections import deque

def isValidVC(VC,G):
    return all(u in VC or v in VC for u, v in G.edges())

def approx_mvc(filename,maxTime=600,seed=10):
    fname = "DATA/"+filename
    random.seed(a=seed)
    G = createGraph(fname)

    # initialize all vertices as not visited
    visited = [False]*G.nodes()

    # Consider all edges one by one
    for u in range(G.nodes()):

        # An edge is only picked when
		# both visited[u] and visited[v]
		# are false
        if not visited[u]:
            for v in G[u]:
                if not visited[v]:

                    # Add the vertices (u, v) to the
					# result set. We make the vertex
					# u and v visited so that all
					# edges from/to them would
					# be ignored
                    visited[v] = True
                    visited[u] = True

                    break

    return visited
