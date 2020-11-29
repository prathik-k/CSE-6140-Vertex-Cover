import sys
from sys import argv
import argparse

from utils import write_to_file
from utils import write_to_file_app
#from LS1_hillclimb import hc
from mvc_approx_algos import approx_mvc

if __name__=="__main__":
    '''
    Sample command: python main.py --inst email.graph --alg ls1 --time 400 --seed 10
    Sample command approx: python main.py --inst email.graph --alg app --time 400 --seed 10
    The implemented algorithms are Branch & Bound (bnb), Approximation (approx), Hill Climbing (ls1) and ...

    '''


    parser = argparse.ArgumentParser(description='Different algorithms to compute the VC of a graph')
    parser.add_argument('--inst',action='store',type=str,required=True,help='Instance of graph')
    parser.add_argument('--alg',action='store',type=str,required=True,help='Type of algorithm - (BnB,Approx,LS1 (Hill climbing),...)')
    parser.add_argument('--time',action='store',default=600,type=int,required=True,help='Maximum runtime (s)')
    parser.add_argument('--seed',action='store',default=10,type=int,required=False,help='Random Seed')
    args=parser.parse_args()
    filename,alg,maxtime,seed = args.inst,args.alg,args.time,args.seed

    if alg.lower() == "ls1":
        VC,solTrace = hc(filename,maxtime,seed)
        print("VC generated")
        write_to_file(VC,filename,"LS1",maxtime,seed,solTrace)

    elif alg.lower() == "app":
        VC,solTrace = approx_mvc(filename,maxtime,seed)
        print("VC generated")
        write_to_file_app(VC,filename,"APP",maxtime,seed,solTrace)
