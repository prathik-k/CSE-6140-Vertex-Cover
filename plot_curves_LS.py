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

def plot_qrtd(inst='power',maxtime=600,seeds=[10,20,30,40,50,60,70,80,90,100],method="LS1",perc_sols = [0.5,1,5,10,15,20,30,60,70,80,90]):    
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
    print(target_sizes)
    xvals = np.arange(mt)
    for perc in perc_sols:        
        P_vals = []
        for t in xvals:
            num_success,num_total = 0,len(seeds)
            for case in all_cases:
                if case[int(t)]<=target_sizes[perc]:
                    num_success+=1
            P_vals.append(100*num_success/num_total)
        plt.plot(P_vals,label=str(perc)+"%")
        plt.ylim([0,100])
    plt.ylabel("P(solve)")
    plt.xlabel("Time (s)")
    plt.legend()
    plt.show()

def plot_sqd(inst='power',maxtime=600,seeds=[10,20,30,40,50,60,70,80,90,100],method="LS1",perc_sols = np.linspace(0,100,21)):
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
    print(target_sizes)    
    times = np.round(np.linspace(0,mt,num=11),2)
    print(times)
    for case in all_cases:
        for t in times:
            case[t] = case.get(t, case[min(case.keys(), key=lambda k: abs(k-t))])

    for i in range(len(all_cases)):        
        case = {k:v for k,v in all_cases[i].items() if k in times}
        all_cases[i] = case

    
 

if __name__=="__main__":
    plot_sqd("star2")


    