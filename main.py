import sys
from sys import argv
import argparse

from utils import write_to_file
from LS1_hillclimb import hc
from approx import approx_mvc
from LS2_sann import main_ls2
from Branch_and_Bound import bnb


if __name__=="__main__":
    '''
    Sample command for ls1: python main.py -inst star2.graph -alg ls1 -time 1000 -seed 10
    Sample command for ls2: python main.py -inst star2.graph -alg ls2 -time 1000 -seed 10
    Sample command approx: python main.py -inst as-22july06.graph -alg app -time 1000 -seed 10
    Sample command for b&b: python main.py -inst karate.graph -alg bnb -time 1000 -seed 10
    
    The implemented algorithms are Branch & Bound (bnb), Approximation (approx), Hill Climbing (ls1) and Simulated Annealing (ls2)

    ['jazz.graph', 'karate.graph', 'football.graph','as-22july06.graph',
    'hep-th.graph','star.graph', 'star2.graph',
    'netscience.graph', 'email.graph', 'delaunay_n10.graph', 'power.graph','dummy1.graph','dummy2.graph']
    '''
    parser = argparse.ArgumentParser(description='Different algorithms to compute the VC of a graph')
    parser.add_argument('-inst',action='store',type=str,required=True,help='Instance of graph')
    parser.add_argument('-alg',action='store',type=str,required=True,help='Type of algorithm - (BnB,Approx,LS1 (Hill climbing),LS2 (Simulated Annealing))')
    parser.add_argument('-time',action='store',default=1000,type=int,required=True,help='Maximum runtime (s)')
    parser.add_argument('-seed',action='store',default=10,type=int,required=False,help='Random Seed')
    args=parser.parse_args()
    filename,alg,maxtime,seed = args.inst,args.alg,args.time,args.seed

    if alg.lower() == "ls1":
        VC,solTrace = hc(filename,maxtime,seed)
        print("VC generated")
        write_to_file(VC,filename,"LS1",maxtime,seed,solTrace)

    elif alg.lower() == "app":
        VC,solTrace = approx_mvc(filename,maxtime,seed)
        print("VC generated")
        write_to_file(VC,filename,"APP",maxtime,seed,solTrace)
        
    elif alg.lower() == "ls2":
        VC,solTrace = main_ls2(filename,maxtime,seed)
        print("VC generated")
        write_to_file(VC,filename,"LS2",maxtime,seed,solTrace)
    
    elif alg.lower() == "bnb":
        VC,solTrace,solution = bnb(filename,maxtime,seed)
        print("VC generated")
        write_to_file(VC,filename,"BNB",maxtime,seed,solTrace)
