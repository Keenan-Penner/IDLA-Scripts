import random as rd
import matplotlib.pyplot as plt
from numba import jit 
import numpy as np
from tqdm import tqdm

## PRELIMINARY FUNCTIONS

@jit(nopython=True)
def movement2D(L,p): #from a given position, gives the new position (for 2D) (L of the form [[x,y],[...,...]])
    if p<0.25:##right##
        newposition = [sum(x) for x in zip(L[0], [1, 0])]
        L.append([1,0])
    elif p<0.5:##left##
        newposition = [sum(x) for x in zip(L[0], [-1, 0])]
        L.append([-1,0])
    elif p<0.75:##up##
        newposition = [sum(x) for x in zip(L[0], [0, 1])]
        L.append([0,1])
    else:##down##
        newposition = [sum(x) for x in zip(L[0], [0, -1])]
        L.append([0,-1])
    return L, newposition

@jit(nopython=True)
def prev2D(L,p): # For 2D
    if p<0.25: 
        previous= [sum(x) for x in zip(L, [-1, 0])]
    elif 0.25<=p<0.5:
        previous= [sum(x) for x in zip(L, [1, 0])]
    elif 0.5<=p<0.75:
        previous= [sum(x) for x in zip(L, [0, -1])]
    else:
        previous= [sum(x) for x in zip(L, [0, 1])]
    return previous

@jit(nopython=True)
def movement3D(L,p): #from a given position, gives the new position (for 3D)
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
def prev3D(L,p): #for 3D
    if p<1/6:
        previous= [sum(x) for x in zip(L, [-1, 0, 0])]
    elif p<1/3:
        previous= [sum(x) for x in zip(L, [1, 0, 0])]
    elif p<1/2:
        previous= [sum(x) for x in zip(L, [0, -1, 0])]
    elif p<2/3:
        previous= [sum(x) for x in zip(L, [0, 1, 0])]
    elif p<5/6:
        previous= [sum(x) for x in zip(L, [0, 0, -1])]
    else:
        previous= [sum(x) for x in zip(L, [0, 0, 1])]
    return previous

@jit(nopython=True)
def levelsplane(M):
    L = []
    for i in range(-M, M+1):
        for j in range(-M, M+1):
            L.append([i, j])
    return L  

@jit(nopython=True)
def levelsaxis(M):
    L=[0]
    for i in range(1,M+1):
        L.append(i)
        L.append(-i)
    return L

#IDLA functions in 2D and 3D


#classical  IDLA in 2D
@jit(nopython=True)
def idla(n): 
    L=[[0,0]]
    edges=[]
    count=1
    progress = 1
    print("Process started")
    while count<n:
        p=rd.random()
        move=movement2D([[0,0]],p)[1]
        while move in L:
            p=rd.random()
            move=movement2D([move],p)[1]    
        if move not in L:
            previous=prev2D(move,p)
            L.append(move)
            edges.append([previous,move])
            count+=1
        if count >= (n/10)*progress:
            print(f"Process at {progress*10}%")
            progress+=1
    return L, edges

#classical IDLA in 3D
@jit(nopython=True)
def idla3(n): 
    L=[[0,0,0]]
    edges=[]
    count=1
    progress = 1
    print("Process started")
    while count<n:
        p=rd.random()
        move=movement3D([[0,0,0]],p)[1]
        while move in L:
            p=rd.random()
            move=movement3D([move],p)[1]    
        if move not in L:
            prev=prev3D(move,p)
            L.append(move)
            edges.append([prev,move])
            count+=1
        if count >= (n/10)*progress:
            print(f"Process at {progress*10}%")
            progress+=1
    return L, edges


#IDLA with n particles emitted from a source, within a given aggregate in 2D
@jit(nopython=True)
def idla2d_general(n, level, agg): #IDLA avec n particules depuis un niveau, et avec un agrégat donné
    count=0
    while count<n:
        p=rd.random()
        move=[0,level]
        while move in agg:
            p=rd.random()
            move=movement2D([move],p)[1]    
        if move not in agg:
            agg.append(move)
            count+=1
    return agg

#IDLA with n particles emitted from a source, within a given aggregate in 3D
@jit(nopython=True) 
def idla3d_general(n, source, agg): 
    count = 0
    while count < n:
        p = rd.random()
        move = [0, source[0], source[1]]
        while move in agg:
            p = rd.random()
            move = movement3D([move], p)[1] 
        agg.append(move)
        count+=1
    return agg

# Multi-source IDLA in 2D (An[M])
@jit(nopython=True)
def A2(n,M): 
    level_list=levelsaxis(M)
    count=1
    total = 2*M +1
    progress = 1
    I=[[0,0]]
    print("Process started")
    while count< total:
        I=idla2d_general(n, level_list[count], I)
        count+=1
        if count >= (total/10)*progress:
            print(f"Process at {progress*10}%")
            progress+=1
    return I


# Multi-source IDLA in 3D (An[M])
@jit(nopython=True)
def A3(n, M): 
    level_list = levelsplane(M)
    count = 1
    I = [[0,0,0]]
    total = (2*M +1)**2
    progress = 1
    print("Process started")
    while count < total:
        I = idla3d_general(n, level_list[count], I)
        count+=1
        if count >= (total/10)*progress:
            print(f"Process at {progress*10}%")
            progress+=1
    return I

## 2D CLASSICAL IDLA PLOTTING

def reverse(edges):
    L=[]
    for i in range( len(edges) - 1, -1, -1) :
        L.append(edges[i])
    return L

def branch(edges,point): #gives all edges from center to point 
    B=[]
    rev=reverse(edges)
    for i in range(len(rev)):
        if rev[i][1]==point:
            B.append(rev[i])
            point=rev[i][0]
    return B

def treeplot2d(n, branch_arg, save_path):
    if save_path == "":
        return 0
    A=idla(n)
    points = A[0]
    edges=A[1]
    ##AGGREGATE
    xpoints=[points[i][0] for i in range(len(points))]
    ypoints=[points[i][1] for i in range(len(points))]

    max_x = max(abs(min(xpoints)), max(xpoints))
    max_y = max(abs(min(ypoints)), max(ypoints))

    plt.scatter(xpoints, ypoints, s=2, color = 'red')
    plt.axis('square')
    extremum = max(max_x, max_y)
    plt.xlim(-extremum - 1, extremum + 1)
    plt.ylim(-extremum - 1, extremum + 1)
    plt.title(f"2D IDLA with {n} particles")
    plt.savefig(f'{save_path}_agg.png', dpi=500)
    plt.clf()
    ##TREE
    point=A[0][-1]
    Branch=branch(edges,point)
    for i in range(len(edges)):
        plt.plot([edges[i][0][0],edges[i][1][0]],[edges[i][0][1],edges[i][1][1]],linewidth=0.5,color='blue')
    if branch_arg:
        for i in range(len(Branch)):
            plt.plot([Branch[i][0][0],Branch[i][1][0]],[Branch[i][0][1],Branch[i][1][1]],linewidth=0.5,color='red')
    plt.axis('square')
    plt.xlim(-extremum - 1, extremum + 1)
    plt.ylim(-extremum - 1, extremum + 1)
    plt.title(f"2D IDLA tree with {n} particles")
    plt.savefig(f'{save_path}_tree.png', dpi=500)
    plt.clf()

## 3D CLASSICAL IDLA PLOTTING

def treeplot3d(n, branch_arg, savepath):
    A=idla3(n)
    ax=plt.axes(projection="3d")
    ax.set_box_aspect([1,1,1])
    ##AGGREGATE
    points = A[0]
    xpoints = [points[i][0] for i in range(len(points))]
    ypoints = [points[i][1] for i in range(len(points))]
    zpoints = [points[i][2] for i in range(len(points))]
    ax.scatter(xpoints,ypoints,zpoints, s=2, color = 'C0')
    plt.title(f"3D IDLA with {n} particles")
    plt.axis('off')
    plt.savefig(f'{savepath}_agg.png', dpi=500)
    plt.clf()
    ##TREE 
    ax=plt.axes(projection="3d")
    ax.set_box_aspect([1,1,1])
    edges= A[1]
    point= A[0][-1]
    Branch=branch(edges,point)
    for i in range(len(edges)):
        xline=[edges[i][0][0], edges[i][1][0]]
        yline=[edges[i][0][1], edges[i][1][1]]
        zline=[edges[i][0][2], edges[i][1][2]]
        ax.plot(xline,yline,zline,linewidth=2, color = 'C0')
    if branch_arg:
        for i in range(len(Branch)):
            xline=[Branch[i][0][0],Branch[i][1][0]]
            yline=[Branch[i][0][1],Branch[i][1][1]]
            zline=[Branch[i][0][2],Branch[i][1][2]]
            ax.plot(xline,yline,zline,linewidth=2, color = 'red')
    plt.title(f"3D IDLA tree with {n} particles")
    plt.axis('off')
    plt.savefig(f'{savepath}_tree.png', dpi=500)
    plt.clf()

## 2D MULTI SOURCE IDLA PLOTTING

def multisource2d(n, M, savepath):
    A = A2(n,M)
    xpoints = [A[i][0] for i in range(len(A))]
    ypoints = [A[i][1] for i in range(len(A))]

    max_x = max(abs(min(xpoints)), max(xpoints))
    max_y = max(abs(min(ypoints)), max(ypoints))
    print(max_x)
    plt.scatter(xpoints, ypoints, s=2, color = 'C0')
    plt.axis('square')
    plt.title(f"2D Multi-source IDLA : A_{n}[{M}]")
    extremum = max(max_x, max_y)
    plt.xlim(-extremum - 1, extremum + 1)
    plt.ylim(-extremum - 1, extremum + 1)
    plt.savefig(f'{savepath}_agg.png', dpi=500)
    plt.clf()

def multisource3d(n, M, savepath):
    A=A3(n,M)
    A = np.array(A)
    #get maximum and minimum x value
    global_maxi_x = np.max(A[:, 0])
    global_mini_x = np.min(A[:, 0])

    #get maximum and minimum y value
    global_maxi_y = np.max(A[:, 1])
    global_mini_y = np.min(A[:, 1])

    #get maximum and minimum z value
    global_maxi_z = np.max(A[:, 2])
    global_mini_z = np.min(A[:, 2])

    #create a voxel grid containing the aggregate
    voxel_grid = np.zeros((global_maxi_x - global_mini_x +1, 
                            global_maxi_y - global_mini_y +1, 
                            global_maxi_z - global_mini_z +1))
    
    #loop over points in the array

    for point in tqdm(A):
        point_x = point[0]
        point_y = point[1]
        point_z = point[2]
    #translation of all the coordinates by value of their global minimum
        voxel_x = point_x + abs(global_mini_x)
        voxel_y = point_y + abs(global_mini_y)
        voxel_z = point_z + abs(global_mini_z)

        voxel_grid[voxel_x, voxel_y, voxel_z] = 1
    
    #plot 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x, y, z = np.indices((voxel_grid.shape[0] + 1, voxel_grid.shape[1] + 1, voxel_grid.shape[2] + 1))

    x+= global_mini_x
    y+= global_mini_y
    z+= global_mini_z 

    ax.voxels(x, y, z, voxel_grid, edgecolor='k', shade = False)

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis') 
    ax.set_box_aspect([1, 1, 1])
    ax.set_aspect('equal')
    plt.title(f"3D Multi-source IDLA : A_{n}[{M}]")
    plt.savefig(f'{savepath}_agg.png', dpi=500)
    plt.clf()
