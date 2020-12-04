# CSE-6140-Vertex-Cover

## Running main.py
In order to implement the algorithms within this repository (with the main.py file), please use the following syntax:

```
python main.py -inst $INST-NAME$ -alg $ALGORITHM$ -time $MAXTIME$ -seed $RANDOMSEED$
```
where the acceptable entries for $INST-NAME$ are LS1, LS2, APP or BNB (which correspond to a hill-climbing algorithm, simulated annealing, approximation with constructive heuristic or branch & bound).

Note that the above command requires an entry for $INST-NAME$ and $ALGORITHM$ arguments, but has default values for $MAXTIME$ and $RANDOMSEED$ as 1000 and 10, respectively.
The results of each run will be stored in the form of .sol and .trace files corresponding to the instance and algorithm (containing the optimal VC size as computed by the algorithm within the stipulated runtime, and the solution trace).