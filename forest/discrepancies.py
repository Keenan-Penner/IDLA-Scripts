import random as rd
from multiprocessing import Process
from numba import jit 
from argparse import ArgumentParser
import os
import numpy as np
import matplotlib.pyplot as plt


# useful tools
#@jit(nopython=True)
def levelsplane(M):
    L = []
    for i in range(-M, M+1):
        for j in range(-M, M+1):
            L.append([i, j])
    return L

#@jit(nopython=True)
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

def previous(L,p): #for 3D
    if p<1/6:
        previous= [sum(x) for x in zip(L[0], [-1, 0, 0])] 
    elif p<1/3:
        previous= [sum(x) for x in zip(L[0], [1, 0, 0])]
    elif p<1/2:
        previous= [sum(x) for x in zip(L[0], [0, -1, 0])]  
    elif p<2/3:
        previous= [sum(x) for x in zip(L[0], [0, 1, 0])]
    elif p<5/6:
        previous= [sum(x) for x in zip(L[0], [0, 0, -1])]
    else:
        previous= [sum(x) for x in zip(L[0], [0, 0, 1])]
    return previous

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

def discrepancy(n, M1, M2): 
    assert M1 <= M2
    times = [] #contains the emission times of the particles for each level
    level_list = levelsplane(M2)
    for elem in level_list:
        t1 = np.random.exponential(1)
        while t1 < n:
            small_level_list = levelsplane(M1)
            if elem in small_level_list:
                times.append([t1, elem, 1]) #we create times and their associated level, mark 1 for both aggregates
            else:
                times.append([t1, elem, 0])
            t1 += np.random.exponential(1)
    #need to sort times with the associated level 
    times.sort(key = lambda x: x[0]) 
    A1 = [] #small aggregate
    A2 = [] #big aggregate 
    arete1 = []
    arete2 = []
    discrep = []
    for elem in times:
        source = elem[1] 
        works_for_both = elem[2]
        #print(f"source: {source}, works for both: {works_for_both}")
        move = [0, source[0], source[1]]
        prev = move
        if works_for_both:
            while move in A1:
                p = rd.random()
                move = movement([move], p)[1]
                prev = previous([move], p)
            A1.append(move)
            arete1.append([prev, move])
            # at this point, move gives the new point for A1, but it is possible move is already in A2
            while move in A2:
                p = rd.random()
                move = movement([move], p)[1]
                prev = previous([move], p)
            A2.append(move)
            arete2.append([prev, move])
        else: #the particle only works for A2
            while move in A2:
                p = rd.random()
                move = movement([move], p)[1]
                prev = previous([move], p)
            discrep.append(move)
            A2.append(move)
            arete2.append([prev, move])
    #print(f"small aggregate: {A1}")
    #print(f"big aggregate: {A2}")
    #print(f"edges of small aggregate: {arete1}")
    #print(f"edges of big aggregate: {arete2}")
    return A1, A2, arete1, arete2, discrep


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--top_level", type=int, default=10)
    parser.add_argument("--bottom_level", type=int, default=1)
    parser.add_argument("--intensity", type=int, default=10)
    parser.add_argument("--do_plot", action="store_false") #defaults to true
    parser.add_argument("--save_path", type=str, default="C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Simulation\\")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    
    # check if save_path exists
    save_path = args.save_path
    if not os.path.exists(save_path):
        # create the directory
        print(f"Creating directory {save_path}")
        os.makedirs(save_path)
    
    n = args.intensity
    M1 = args.bottom_level
    M2 = args.top_level
    
    A1, A2, arete1, arete2, discrep = discrepancy(n, M1, M2)
    # need to find vertices reached by different particles
    vertex_diff = [] #gives vertices of big aggregate that aren't in the small aggregate
    potential_discrep = []
    for elem in A2:
        if elem not in A1:
            vertex_diff.append(elem)
    for elem in discrep:
        if elem not in A1:
            potential_discrep.append(elem)

    if args.do_plot:
        ax=plt.axes(projection="3d")
        ax.set_box_aspect([1,1,1])
        for i in range(len(arete1)):
            xline=[arete1[i][0][0],arete1[i][1][0]]
            yline=[arete1[i][0][1],arete1[i][1][1]]
            zline=[arete1[i][0][2],arete1[i][1][2]]
            ax.plot(xline, yline, zline, linewidth=2, color = "green")
        for elem in vertex_diff:
            xpoints = elem[0]
            ypoints = elem[1]
            zpoints = elem[2]
            ax.scatter(xpoints, ypoints, zpoints, color = "red", s= 1)
        for elem in potential_discrep:
            xpoints = elem[0]
            ypoints = elem[1]
            zpoints = elem[2]
            ax.scatter(xpoints, ypoints, zpoints, color = "blue", s= 1)
        plt.axis('off')
        plt.show()

