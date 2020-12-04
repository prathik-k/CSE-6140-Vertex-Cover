import sys
from sys import argv
import argparse

from utils import write_to_file
from LS1_hillclimb import hc
from approx import approx_mvc
from LS2_sann import main_ls2
from Branch_and_Bound import bnb

seed = 10
filenames = ['jazz.graph', 'karate.graph', 'football.graph','as-22july06.graph',
    'hep-th.graph','star.graph', 'star2.graph',
    'netscience.graph', 'email.graph', 'delaunay_n10.graph', 'power.graph','dummy1.graph','dummy2.graph']
maxtime=1000
for filename in filenames:
    VC,solTrace = hc(filename,maxtime,seed)
    print("VC generated for ",filename)
    write_to_file(VC,filename,"LS1",maxtime,seed,solTrace)

'''
seeds = [10,20,30,40,50,60,70,80,90,100]
filenames = ["star2.graph","power.graph"]
maxtime=600
for filename in filenames:
    for seed in seeds:
        VC,solTrace = main_ls2(filename,maxtime,seed)
        print("VC generated")
        write_to_file(VC,filename,"LS2",maxtime,seed,solTrace)
'''
