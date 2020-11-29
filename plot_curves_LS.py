import numpy as np
import matplotlib.pyplot as plt 

def plot_qrtd(inst='power',maxtime=600,seeds=[10,20,30,40,50,60,70,80,90,100],methods=["LS1","LS2"]):

    for method in methods:
        for seed in seeds:
            fname = "output/"+inst+"_"+method+"_"+str(maxtime)+"_"+str(seed)+".trace"
            with open(fname,'rb') as f:
                tracevals = f.read().splitlines()
    
    print(tracevals)

if __name__=="__main__":
    plot_qrtd()


    