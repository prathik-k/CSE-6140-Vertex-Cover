import sys
from sys import argv
import argparse

from LS_hillclimb import hc

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Different algorithms to compute the VC of a graph')
    parser.add_argument('-inst',action='store',type=str,required=True,help='Instance of graph')
    parser.add_argument('-alg',action='store',type=str,required=True,help='Type of algorithm - (B&B,Approx,HC,...)')
    parser.add_argument('-time',action='store',default=600,type=float,required=True,help='Maximum runtime (s)')
    parser.add_argument('-seed',action='store',default=10,type=int,required=False,help='Random Seed')
    args=parser.parse_args()
    
    filename,alg,maxtime,seed = ("DATA/"+args.inst),args.alg,args.time,args.seed
    
    if alg.lower() == "hc":
        hc(filename,maxtime,seed)