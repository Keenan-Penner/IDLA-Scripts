import os
from ast import literal_eval
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.pyplot as plt

## IMPORT FILE

FOLDER_NAME = 'shapeThm-agg'
WINDOW = 10
PARTICLE_NUM = 30
POSITIVE = True #only look at positive values of x for aggregate
PROJ = True

savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\{FOLDER_NAME}"
os.chdir(savepath) #Change directory

A = open(f"agg{PARTICLE_NUM}-{PARTICLE_NUM}.txt",'r').read() #Assigns the contents of the file to B as string
A = literal_eval(A) #Makes this an array

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_aspect('equal')
if PROJ:
    ax.view_init(elev=0, azim=-2)
plt.xticks([])
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis') 

#Create window

A_window = [elem for elem in A if -WINDOW <= elem[1] <= WINDOW and -WINDOW <= elem[2] <= WINDOW]

X = [elem[0] for elem in A_window]
Y = [elem[1] for elem in A_window]
Z = [elem[2] for elem in A_window]

## Fix axes so everything is centered correctly

max_range = np.array([max(X)-min(X), max(Y)-min(Y), max(Z)-min(Z)]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(max(X)+min(X))
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(max(Y)+min(Y))
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(max(Z)+min(Z))
for xb, yb, zb in zip(Xb, Yb, Zb):
    ax.plot([xb], [yb], [zb], 'w')

### Treat case of only looking at the right side 

if POSITIVE: 
    A_window = [elem for elem in A_window if elem[0] >= 0]

# CATEGORIZE POINTS ON THE BORDER

border = []
for i in range(-WINDOW, WINDOW +1):
    for j in range(-WINDOW, WINDOW +1):
        points = [elem[0] for elem in A_window if elem[1] == i and elem[2] == j] # gives all x points of line (., i, j)
        mini = min(points)
        maxi = max(points)
        border.append([maxi, i, j])
        if not POSITIVE:
            border.append([mini, i, j])

interior_border = []
exterior_border = []
perfect_border = []
for point in border:
    A_window.remove(point)
    if point[0] > PARTICLE_NUM /2 or point[0] < -PARTICLE_NUM /2 : #point is exterior
        exterior_border.append(point)
    elif point[0] == PARTICLE_NUM /2 or point[0] == -PARTICLE_NUM /2: #point is right on the border
        perfect_border.append(point)
    else:
        interior_border.append(point)

# Sort coordinates of various points

int_positions = []
for elem in interior_border:
    new_elem = [elem[0]-.5, elem[1]-.5, elem[2]-.5]
    int_positions.append(new_elem)

ext_positions = []
for elem in exterior_border:
    new_elem = [elem[0]-.5, elem[1]-.5, elem[2]-.5]
    ext_positions.append(new_elem)

perf_positions = []
for elem in perfect_border:
    new_elem = [elem[0]-.5, elem[1]-.5, elem[2]-.5]
    perf_positions.append(new_elem)

rem_positions = []
for elem in A_window:
    new_elem = [elem[0]-.5, elem[1]-.5, elem[2]-.5]
    rem_positions.append(new_elem)
## FUNCTIONS FOR CUBOID

def cuboid_data2(o, size=(1,1,1)):
    X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
         [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
         [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
         [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
         [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
    X = np.array(X).astype(float)
    for i in range(3):
        X[:,:,i] *= 1
    X += np.array(o)
    return X

def plotCubeAt2(positions,sizes=None,colors=None, **kwargs):
    fcolors=[colors]*len(positions)
    if not colors:
        fcolors=["C0"]*len(positions) # puts all colors to the first specified one
    #if not isinstance(colors,(list,np.ndarray)): fcolors=["C0"]*len(positions) # puts all colors to the first specified one
    if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
    g = []
    for p,s,c in zip(positions,sizes,fcolors):
        g.append( cuboid_data2(p, size= s) )
    return Poly3DCollection(np.concatenate(g),  
                            facecolors=np.repeat(fcolors,6), linewidths = 0.25, **kwargs)

# Plotting

## Plotting the 'uninteresting' points 

if A_window:
    pc = plotCubeAt2(rem_positions, sizes= None, colors= None, edgecolor= 'k')
    ax.add_collection3d(pc)

## Plotting interior points

if int_positions:
    pc = plotCubeAt2(int_positions, sizes= None, colors= 'green', edgecolor= 'k')
    ax.add_collection3d(pc)

## Plotting perfect positions

if perf_positions:
    pc = plotCubeAt2(perf_positions, sizes= None, colors= 'blue', edgecolor= 'k')
    ax.add_collection3d(pc)

## Plotting exterior points

if ext_positions: #False if list is empty (only runs for non-empty list)
    pc = plotCubeAt2(ext_positions, sizes=None, colors= 'red', edgecolor='k')
    ax.add_collection3d(pc)

# plt.savefig(os.path.join(savepath, f"agg{PARTICLE_NUM}-{PARTICLE_NUM}-windowsize{WINDOW}-colored{'-proj' if PROJ else ''}.png"), dpi = 600)
plt.show()