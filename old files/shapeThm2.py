import matplotlib.pyplot as plt
import random as rd
from multiprocessing import Process
import numpy as np
from matplotlib import cm
from ast import literal_eval


# useful tools

FOLDER_NAME = "Simtest"
LOG_NAME = "log_files"
PERCENT_INCREMENT = 1 #Either 1 or 10

def levelsplane(M):
    L = []
    for i in range(-M, M+1):
        for j in range(-M, M+1):
            L.append([i, j])
    return L

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
def A3(n, M, num = 0): 
    level_list = levelsplane(M)
    count = 0
    I = []
    total = (2*M +1)**2
    progress = 1
    increment = 100 / PERCENT_INCREMENT
    file = open(f"{LOG_NAME}/init{num}.txt", 'w')
    file.write(f"Process{num} started")
    file.close()
    while count < total:
        I = idla(n, level_list[count], I)
        count+=1
        if count >= (total/increment)*progress:
            print(f"Process{num} at {progress*PERCENT_INCREMENT}%")
            file = open(f"{LOG_NAME}/init{progress*PERCENT_INCREMENT}.txt", 'w')
            file.write(f"Process{num} at {progress*PERCENT_INCREMENT}%")
            file.close()
            progress+=1
    file = open(f"{LOG_NAME}/init{progress*PERCENT_INCREMENT}.txt", 'w')
    file.write(f"Process{num} finished")
    file.close()
    file = open(f"{FOLDER_NAME}/agg{num}.txt", 'w')
    file.write(str(I))
    file.close()
    return I

if __name__ == "__main__":
    from argparse import ArgumentParser
    import os
    parser = ArgumentParser()
    parser.add_argument("--particle_nb", type=int, default= 1)
    parser.add_argument("--levels", type=int, default= 100) #variable levels corresponds to the max level M
    parser.add_argument("--nb_trials", type=int, default= 1)
    args = parser.parse_args()

    if not os.path.exists(FOLDER_NAME):
            # create the directory
            print(f"Creating directory {FOLDER_NAME}")
            os.makedirs(FOLDER_NAME)
    if not os.path.exists(LOG_NAME):
            # create the directory
            print(f"Creating directory {LOG_NAME}")
            os.makedirs(LOG_NAME)

    procs = []
    
    # FOR SIMPLE PROCESSING
    
    A3(args.particle_nb, args.levels, 0 )


    #FOR MULTI PROCESSING
    '''
    for k in range(args.nb_trials):
        p = Process(target= A3, args=(args.particle_nb, args.levels,k,))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    '''