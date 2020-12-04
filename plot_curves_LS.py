import numpy as np
import matplotlib.pyplot as plt 

'''
For the power.graph instance, the LS1 (hill climbing) algorithm yielded an average final result of 2279 for the VC size. Since the graph size is 4941, we have
5% solution: size=4808
8% solution: size=4728
10% solution: size=4675
20% solution: size=4409
We plot the QRTD plots for the above cases, with the time ranging from 0-17s.
'''

def plot_qrtd(inst='power',maxtime=600,seeds=[10,20,30,40,50,60,70,80,90,100],method="LS1",perc_sols = [6,8,15,20]):    
    if inst=='power':
        q = 2203
    elif inst=='star2':
        q = 4542
    all_cases,final_results = [],[]
    mt = 0
    for seed in seeds:
        fname = "output/"+inst+"_"+method+"_"+str(maxtime)+"_"+str(seed)+".trace"
        with open(fname,'r') as f:
            tracevals = f.readlines()
        tracevals = [x.strip().split(",") for x in tracevals]
        tracevals = {int(float(t)):int(vc_size) for (t,vc_size) in tracevals}
        all_cases.append(tracevals)
        final_results.append(list(tracevals.values())[-1])
        mt = max(mt,list(tracevals.keys())[-1])
        
    for case in all_cases:
        if mt not in case:
            finalkey,finalval = max(case, key=int),case[max(case, key=int)]
            for k in range(finalkey+1,mt):
                case[k]=finalval
    target_sizes = {}
    for perc in perc_sols:
        target_size = int(q*(100+perc)/100)
        target_sizes[perc] = target_size 


    if inst=="power" and method=="LS2":
        xvals = [0.1,0.5,2,5]    
    elif inst=="power" and method=="LS1":
        xvals = [0,2,4,6,8,10,12,20]
    elif inst=="star2" and method=="LS2":
        xvals = [50,80,100,200]
    elif inst=="star2" and method=="LS1":
        xvals = [450,470,500,550]

    for case in all_cases:
        for t in xvals:
            case[int(t)] = case.get(t, case[min(case.keys(), key=lambda k: abs(k-t))])    

    fig, ax = plt.subplots()
    markers = [("o",11),("^",9),("D",7),("H",5)]
    for i,perc in enumerate(perc_sols):     
        mk,size = markers[i]   
        P_vals = []
        for t in xvals:
            num_success,num_total = 0,len(seeds)
            for case in all_cases:
                if case[int(t)]<=target_sizes[perc]:
                    num_success+=1
            P_vals.append(num_success/num_total)
        ax.plot(xvals,P_vals,marker=mk,markersize=size,label=str(perc)+"%")
        ax.set_ylim([0,1.1])
    ax.set_ylabel("P(solve)")
    ax.set_xlabel("Time (s)")
    ax.legend()
    plt.savefig("plots/"+inst+"_"+method+"_qrtd.png")
    plt.clf()  

def plot_sqd(inst='power',maxtime=600,seeds=[10,20,30,40,50,60,70,80,90,100],method="LS1",perc_sols = np.linspace(0,15,21)):
    if inst=='power':
        q = 2203
    elif inst=='star2':
        q = 4542
    all_cases,final_results = [],[]
    mt = 0
    for seed in seeds:
        fname = "output/"+inst+"_"+method+"_"+str(maxtime)+"_"+str(seed)+".trace"
        with open(fname,'r') as f:
            tracevals = f.readlines()
        tracevals = [x.strip().split(",") for x in tracevals]
        tracevals = {int(float(t)):int(vc_size) for (t,vc_size) in tracevals}
        all_cases.append(tracevals)
        final_results.append(list(tracevals.values())[-1])
        mt = max(mt,list(tracevals.keys())[-1])
    target_sizes = {}
    for perc in perc_sols:
        target_size = int(q*(100+perc)/100)
        target_sizes[perc] = target_size     

    if inst=="power" and method=="LS2":
        times = [1,2,5,10]    
    elif inst=="power" and method=="LS1":
        times = [6,8,10,12]
    elif inst=="star2" and method=="LS2":
        times = [100,150,200,300]
    elif inst=="star2" and method=="LS1":
        times = [450,470,500,550]

    for case in all_cases:
        for t in times:
            case[t] = case.get(t, case[min(case.keys(), key=lambda k: abs(k-t))])

    for i in range(len(all_cases)):        
        case = {k:v for k,v in all_cases[i].items() if k in times}
        all_cases[i] = case
    
    fig, ax = plt.subplots()
    markers = [("o",11),("^",9),("D",7),("H",5)]
    for i,t in enumerate(times):
        mk,size = markers[i]  
        P_vals = []
        for perc in perc_sols:
            num_success,num_total = 0,len(seeds)
            for case in all_cases:
                if case[t]<=target_sizes[perc]:
                    num_success+=1
            P_vals.append(num_success/num_total)
        ax.plot(perc_sols,P_vals,marker=mk,markersize=size,label=str(t)+"s")
        ax.set_ylim([0,1.1])
    ax.set_ylabel("P(solve)")
    ax.set_xlabel("Solution quality (%)")
    ax.legend()
    plt.savefig("plots/"+inst+"_"+method+"_sqd.png")
    plt.clf()   


if __name__=="__main__":
    plot_qrtd(inst="star2",maxtime=1000,method="LS1")
    plot_qrtd(inst="star2",maxtime=1000,method="LS2")
    plot_qrtd(inst="power",maxtime=1000,method="LS2")
    plot_qrtd(inst="power",maxtime=1000,method="LS1")

    plot_sqd(inst="power",maxtime=1000,method="LS1")
    plot_sqd(inst="power",maxtime=1000,method="LS2")
    plot_sqd(inst="star2",maxtime=1000,method="LS1")
    plot_sqd(inst="star2",maxtime=1000,method="LS2")
    


    