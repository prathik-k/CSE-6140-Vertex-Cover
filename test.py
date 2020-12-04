import sys
from sys import argv
import argparse

from utils import write_to_file
from LS1_hillclimb import hc
from mvc_approx_algos import approx_mvc
from LS2_sann import main_ls2

seeds = [10,20,30,40,50,60,70,80,90,100]
filenames = ["star2.graph","power.graph"]
maxtime=600
for filename in filenames:
    for seed in seeds:
        VC,solTrace = main_ls2(filename,maxtime,seed)
        print("VC generated")
        write_to_file(VC,filename,"LS2",maxtime,seed,solTrace)