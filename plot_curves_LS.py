import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

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
        xvals = [350,400,420,500,550,600]

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

def boxplot(method="LS1"):
    if method == "LS2":
        times_power = [155.69,162.48,46.4,224.78,90.85,144.36,72.55,332.59,107.27,98.15]
        times_star2 = [867.91,979.96,817.77,645.83,971.04,951.52,912.34,911.66,715.7,988.03]
        alt_name = "simulated annealing"
    
    elif method=="LS1":
        times_power = [11.58,11.63,11.53,11.47,11.52,11.48,11.6,11.42,11.5,11.36]
        times_star2 = [541.58,517.14,478.0,470.78,473.76,481.96,478.47,491.77,501.38,502.48]
        alt_name = "hill-climbing"

    all_time_data = [times_power,times_star2]
    fig,ax = plt.subplots()
    ax.set_title("Boxplot of running time for "+alt_name+" algorithm")
    ax.boxplot(all_time_data,showfliers=False)
    ax.set_ylabel("Runtime (s)")
    ax.set_xticklabels(['power.graph', 'star2.graph'])
    plt.savefig("plots/"+method+"_boxplot.png")
    plt.clf() 
    
if __name__=="__main__":
    boxplot("LS1")
    boxplot("LS2")
    plot_qrtd(inst="star2",maxtime=1000,method="LS1")
    plot_qrtd(inst="star2",maxtime=1000,method="LS2")
    plot_qrtd(inst="power",maxtime=1000,method="LS2")
    plot_qrtd(inst="power",maxtime=1000,method="LS1")

    plot_sqd(inst="power",maxtime=1000,method="LS1")
    plot_sqd(inst="power",maxtime=1000,method="LS2")
    plot_sqd(inst="star2",maxtime=1000,method="LS1")
    plot_sqd(inst="star2",maxtime=1000,method="LS2")


    


    