import sys
from sys import argv
import argparse

from utils import write_to_file
from LS1_hillclimb import hc
from approx import approx_mvc
from LS2_sann import main_ls2
from Branch_and_Bound import bnb

seeds = [10,20,30,40,50,60,70,80,90,100]
filenames = ["power.graph","star2.graph"]
maxtime=1000
for filename in filenames:
    for seed in seeds:
        VC,solTrace = hc(filename,maxtime,seed)
        print("VC generated")
        write_to_file(VC,filename,"LS1",maxtime,seed,solTrace)

