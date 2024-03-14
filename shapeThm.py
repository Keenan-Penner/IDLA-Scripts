import random as rd
from multiprocessing import Process
from numba import jit 
from argparse import ArgumentParser
import os


# useful tools
@jit(nopython=True)
def levelsplane(M):
    L = []
    for i in range(-M, M+1):
        for j in range(-M, M+1):
            L.append([i, j])
    return L

@jit(nopython=True)
def movement(L,p): #from a given position, gives the new position 

    if p<1/6:
        
        newposition = [sum(x) for x in zip(L[0], [1, 0, 0])]
        L.append([1, 0, 0])
    
    elif p<1/3:
        
        newposition = [sum(x) for x in zip(L[0], [-1, 0, 0])]
        L.append([-1, 0, 0])
    
    elif p<1/2:
        
        newposition = [sum(x) for x in zip(L[0], [0, 1, 0])]
        L.append([0, 1, 0])
    
    elif p<2/3:
        
        newposition = [sum(x) for x in zip(L[0], [0, -1, 0])]
        L.append([0, -1, 0])
    
    elif p<5/6:

        newposition = [sum(x) for x in zip(L[0], [0, 0, 1])]
        L.append([0, 0, 1])
        
    else:
    
        newposition = [sum(x) for x in zip(L[0], [0, 0, -1])]
        L.append([0, 0, -1])
    return L, newposition

@jit(nopython=True) 
def idla(n, source, agg): #IDLA with n particles from a source, within a given aggregate 
    count = 0
    while count < n:
        p = rd.random()
        move = [0, source[0], source[1]]
        while move in agg:
            p = rd.random()
            move = movement([move], p)[1] 
        agg.append(move)
        count+=1
    return agg

# Cluster function of An[M] in 3D, returning coordinates of cluster points
@jit(nopython=True)
def A3(n, M, num = 0): 
    level_list = levelsplane(M)
    count = 0
    I = [[0,0,0]]
    total = (2*M +1)**2
    progress = 1
    print(f"Process{num} started")
    while count < total:
        I = idla(n, level_list[count], I)
        count+=1
        if count >= (total/10)*progress:
            print(f"Process{num} at {progress*10}%")
            progress+=1
    return I[1:]

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--particle_nb", 
        type=int, 
        default= 1
    )
    parser.add_argument(
        "--levels", 
        type=int, 
        default=50
    )
    parser.add_argument(
        "--nb_trials", 
        type=int, 
        default=1
    )
    parser.add_argument(
        "--multiprocessing",
        action="store_true",
        help="Use multiprocessing",
    )
    parser.add_argument(
        "--increment",
        type=int,
        default=10,
        help="Increment for the progress bar, either 1 or 10"
    )
    parser.add_argument(
        "--root",
        type=str,
        default="C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\",
    )
    parser.add_argument(
        "--folder",
        type=str,
        default="simulationsJit",
    )
    args = parser.parse_args()
    root_file = os.path.join(args.root, args.folder)
    if not os.path.exists(root_file): #if the directory does not exist
            # create the directory
            print(f"Creating directory {args.folder}")
            os.makedirs(args.folder)

    procs = []
    if args.multiprocessing: #if we wish to use multiprocessing, needs fixing
        for k in range(args.nb_trials):
            p = Process(target= A3, args=(args.particle_nb, args.levels,k,))
            p.start()
            procs.append(p)
        for p in procs:
            p.join()
        print(procs)
    else:
        file = open(f"{args.folder}/agg{args.nb_trials}.txt", 'w')
        file.write(str(A3(args.particle_nb, args.levels, 0 )))
        file.close()

