import matplotlib.pyplot as plt
import random as rd
from multiprocessing import Process
import numpy as np
from matplotlib import cm
from ast import literal_eval


# useful tools

FOLDER_NAME = "Simtest"

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
    print(f"Process{num} started")
    while count < total:
        I = idla(n, level_list[count], I)
        count+=1
        if count >= (total/10)*progress:
            print(f"Process{num} at {progress*10}%")
            progress+=1
    file = open(f"{FOLDER_NAME}/agg{num}.txt", 'w')
    file.write(str(I))
    file.close()
    return I

if __name__ == "__main__":
    from argparse import ArgumentParser
    import os
    parser = ArgumentParser()
    parser.add_argument("--particle_nb", type=int, default= 100)
    parser.add_argument("--levels", type=int, default=100) #variable levels corresponds to the max level M
    parser.add_argument("--nb_trials", type=int, default=1)
    args = parser.parse_args()

    if not os.path.exists(FOLDER_NAME):
            # create the directory
            print(f"Creating directory {FOLDER_NAME}")
            os.makedirs(FOLDER_NAME)

    procs = []
    
    for k in range(args.nb_trials):
        p = Process(target= A3, args=(args.particle_nb, args.levels,k,))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    
    '''
    savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\{FOLDER_NAME}"
    os.chdir(savepath) #Change directory
    for k in range(args.nb_trials):
        A = open(f"agg{k}.txt",'r').read() #Assigns the contents of the file to B as string
        A = literal_eval(A) #Makes this an array
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_aspect('equal')

        X = [elem[0] for elem in A]
        Y = [elem[1] for elem in A]
        Z = [elem[2] for elem in A]
        ax.scatter(X, Y, Z, depthshade=False)
        # Create cubic bounding box to simulate equal aspect ratio
        max_range = np.array([max(X)-min(X), max(Y)-min(Y), max(Z)-min(Z)]).max()
        Xb = 0.3*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(max(X)+min(X))
        Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(max(Y)+min(Y))
        Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(max(Z)+min(Z))
        # Comment or uncomment following both lines to test the fake bounding box:
        for xb, yb, zb in zip(Xb, Yb, Zb):
            ax.plot([xb], [yb], [zb], 'w')
        plt.savefig(os.path.join(savepath, f"agg{k}.png"))
        '''
