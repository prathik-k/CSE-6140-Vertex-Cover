
'''
This file implements the Simulate Annealing algoritthm to find the minimum vertex cover for an input graph.
TEAM 22, Aarohi
Language: Python 3
Executable: python main.py  -inst jazz.graph -alg ls2 -time 600 -seed 10
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


def main_ls2(graph_file,cutoff, randSeed):
    graph_file  = "DATA/"+graph_file
    randseed = int(randSeed)
    solution_file =  graph_file[0:-6] + "_LS2_" + str(cutoff) + "_" + str(randseed) + ".sol"
    trace_file = graph_file[0:-6] + "_LS2_" + str(cutoff) + "_" + str(randseed) + ".trace"
    output2 = open(trace_file, 'w')
    G, NumOfVer = read_graph(graph_file)
    G1 = G.copy()
    start_time = time.time()
    sol = initial_solution(G1,graph_file)

    output2.write('%.2f, %i\n' % (0, len(sol)))

    final_solution = sim_ann(G,output2,sol,cutoff,randseed,NumOfVer,start_time,graph_file)
    size = len(final_solution)
    total_time = round(time.time() - start_time)
    # # Write results to output file
    output1 = open(solution_file, 'w')
    output1.write(str(size) + '\n')
    for vid in range(size-1):
        output1.write(str(final_solution[vid]) + ',')
        output1.write(str(final_solution[vid+1]))

opt_cutoff = {'DATA/jazz.graph':158, 'DATA/karate.graph':14, 'DATA/football.graph':94, 'DATA/as-22july06.graph':3303, 'DATA/hep-th.graph':3926,'DATA/star.graph':6902, 'DATA/star2.graph':4542, 'DATA/netscience.graph':899, 'DATA/email.graph':594, 'DATA/delaunay_n10.graph':703, 'DATA/power.graph':2203}

# Read the graph file
def read_graph(filename):

    # Generate a graph to store input information
    G = nx.Graph()
    f = open(filename)
    line = f.readline()  # size of vertices; size of edges; 0
    values = line.split()
    values = [int(x) for x in values]
    NumOfVer, NumOfEdge = values[0], values[1]
    for i in range(NumOfVer):
        line = f.readline()    # read graph file line by line
        values = line.split()
        values = [int(x) for x in values]
        for j in range(len(values)):
            G.add_edge(i+1,values[j])
    return G,NumOfVer


def initial_solution(G, input_file):
    temp_G = G.nodes()
    return temp_G

# Local Search algorithm using Simulate Annealing
def sim_ann(G, output, sol, cutoff, randseed, NumOfVer,start_time, input_file):
    start_time1 = time.time()
    time_end = time.time() + int(cutoff)
    temp = 0.15     # set initial temperature based on Holger's stochastic local approach : 2004
    update_sol = sol.copy()
    random.seed(randseed)
    uncov_edges=[]
    while ((time.time() - start_time1) < cutoff and len(update_sol) > opt_cutoff[str(input_file)]):
        temp = 0.95 * temp       # update temperature
        count = 0
        while count < (NumOfVer - len(update_sol)-1) * (NumOfVer - len(update_sol) - 1) and len(update_sol) > opt_cutoff[str(input_file)]:
            count += 1
            if ((time.time() - start_time1) < cutoff)and len(update_sol) > opt_cutoff[str(input_file)]:
                while not uncov_edges:
                    update_sol = sol.copy()
                    output.write(str(time.time()-start_time) + "," + str(len(update_sol)) + "\n")
                    delete = random.choice(sol)
                    for x in G.neighbors(delete):
                        if x not in sol:
                            uncov_edges.append((x,delete))
                            uncov_edges.append((delete,x))
                    sol.remove(delete)    # decrement the size of vertex cover to find improved solution
                current = sol.copy()
                uncov_curr = uncov_edges.copy()
                delete = random.choice(sol)
                for x in G.neighbors(delete):
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

    return update_sol
