'''
This file implements the Simulate Annealing algorithm to find the minimum vertex cover for an input graph.
TEAM 22, Aarohi, Prathik
Language: Python 3
Executable example: python main.py  -inst karate.graph -alg ls2 -time 600 -seed 10
The output is two files: *.sol and *.trace created
*.sol --- record the size of optimum vertex cover and the nodes in it.
*.trace --- record all the optimum solution found during the search and the time it was found
'''

import networkx as nx
from random import sample
import random
import time
import os
import math
from utils import *

def initial_solution(G, input_file):
    temp_G = G.nodes()
    return temp_G

# Local Search algorithm using Simulate Annealing
def sim_ann(G, sol, cutoff, randseed, NumOfVer,start_time, input_file,opt_cutoff):
    start_time1 = time.time()
    time_end = time.time() + int(cutoff)
    temp = 0.15     # set initial temperature based on Holger's stochastic local approach : 2004
    update_sol = sol.copy()
    random.seed(randseed)
    uncov_edges=[]
    solTrace = dict()
    while ((time.time() - start_time1) < cutoff and len(update_sol) > opt_cutoff[str(input_file)]):
        temp = 0.95 * temp       # update temperature
        count = 0
        while count < (NumOfVer - len(update_sol)-1) * (NumOfVer - len(update_sol) - 1) and len(update_sol) > opt_cutoff[str(input_file)]and (time.time() - start_time1) < cutoff:
            solTrace[round(time.time()-start_time,2)] = len(update_sol)
            count += 1
            if ((time.time() - start_time1) < cutoff)and len(update_sol) > opt_cutoff[str(input_file)]:
                while not uncov_edges:
                    update_sol = sol.copy()
                    solTrace[round(time.time()-start_time,2)] = len(update_sol)
                    delete = random.choice(sol)
                    for x in G.neighbors(delete):
                        solTrace[round(time.time()-start_time,2)] = len(update_sol)
                        if x not in sol:
                            uncov_edges.append((x,delete))
                            uncov_edges.append((delete,x))
                    sol.remove(delete)    # decrement the size of vertex cover to find improved solution
                current = sol.copy()
                uncov_curr = uncov_edges.copy()
                delete = random.choice(sol)
                for x in G.neighbors(delete):
                    solTrace[round(time.time()-start_time,2)] = len(update_sol)
                    if x not in sol:
                        uncov_edges.append((x,delete))
                        uncov_edges.append((delete,x))
                sol.remove(delete)    # randomly select an exiting vertex
                enter = random.choice(uncov_edges)
                if enter[0] in sol:
                    better_add = enter[1]
                else:
                    better_add = enter[0]
                sol.append(better_add)
                for x in G.neighbors(better_add):
                    solTrace[round(time.time()-start_time,2)] = len(update_sol)
                    if x not in sol:
                        uncov_edges.remove((better_add,x))
                        uncov_edges.remove((x,better_add))
                cost_curr = len(uncov_curr)/2
                cost_sol = len(uncov_edges)/2
                if cost_curr < cost_sol:    # if current solution is better
                    prob = math.exp(float(cost_curr - cost_sol)/float(temp))
                    num = round(random.uniform(0,1),10)
                    if num > prob:    # do not accept modified solution
                        sol = current.copy()
                        uncov_edges = uncov_curr.copy()
    return set(update_sol),list(solTrace.items())

def main_ls2(graph_file,cutoff, randSeed):
    opt_cutoff = {'DATA/jazz.graph':158, 'DATA/karate.graph':14, 'DATA/football.graph':94,
    'DATA/as-22july06.graph':3303, 'DATA/hep-th.graph':3926,'DATA/star.graph':6902, 'DATA/star2.graph':4542,
    'DATA/netscience.graph':899, 'DATA/email.graph':594, 'DATA/delaunay_n10.graph':703, 'DATA/power.graph':2203}
    
    graph_file  = "DATA/"+graph_file
    randseed = int(randSeed)
    G = createGraph(graph_file)
    NumOfVer = G.number_of_nodes()
    G1 = G.copy()
    start_time = time.time()
    sol = initial_solution(G1,graph_file)
    final_solution,solTrace = sim_ann(G,sol,cutoff,randseed,NumOfVer,start_time,graph_file,opt_cutoff)
    return final_solution,solTrace
