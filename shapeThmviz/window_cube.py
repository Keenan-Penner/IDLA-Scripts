import os
from ast import literal_eval
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

FOLDER_NAME = 'shapeThm-agg'
WINDOW = 10 # parameter for size of the window
PARTICLE_NUM = 30

savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\{FOLDER_NAME}"
os.chdir(savepath) #Change directory

A = open(f"agg{PARTICLE_NUM}-{PARTICLE_NUM}.txt",'r').read() #Assigns the contents of the file to B as string
A = literal_eval(A) #Makes this an array
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_aspect('equal')

## Small window

A_window = [elem for elem in A if -WINDOW <= elem[1] <= WINDOW and -WINDOW <= elem[2] <= WINDOW]
X = [elem[0] for elem in A_window]
Y = [elem[1] for elem in A_window]
Z = [elem[2] for elem in A_window]

ax.set_aspect('equal')

ax.scatter(X, Y, Z, s= 20, depthshade= False)
max_range = np.array([max(X)-min(X), max(Y)-min(Y), max(Z)-min(Z)]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(max(X)+min(X))
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(max(Y)+min(Y))
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(max(Z)+min(Z))
for xb, yb, zb in zip(Xb, Yb, Zb):
    ax.plot([xb], [yb], [zb], 'w')

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
    if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
    if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
    g = []
    for p,s,_ in zip(positions,sizes,colors):
        g.append( cuboid_data2(p, size=s) )
    return Poly3DCollection(np.concatenate(g),  
                            facecolors=np.repeat(colors,6), linewidths = 0.25, **kwargs)

positions=[]
for elem in A_window:
    new_elem = [elem[0]-.5, elem[1]-.5, elem[2]-.5]
    positions.append(new_elem)

pc = plotCubeAt2(positions,sizes=None,colors=None, edgecolor="k")
ax.add_collection3d(pc)
plt.show()
#plt.savefig(os.path.join(savepath, f"agg{PARTICLE_NUM}-{PARTICLE_NUM}-windowsize{WINDOW}-cubed.png"), dpi = 600)