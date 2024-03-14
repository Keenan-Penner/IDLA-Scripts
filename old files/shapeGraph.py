import os
from ast import literal_eval
import matplotlib.pyplot as plt
import numpy as np

FOLDER_NAME = 'shapeThm-agg'
WINDOW = 10
PARTICLE_NUM = 30
POSITIVE = True #only look at positive values of x for aggregate

savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\{FOLDER_NAME}"
os.chdir(savepath) #Change directory

A = open(f"agg{PARTICLE_NUM}-{PARTICLE_NUM}.txt",'r').read() #Assigns the contents of the file to B as string
A = literal_eval(A) #Makes this an array
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_aspect('equal')

## Total plot

X = [elem[0] for elem in A]
Y = [elem[1] for elem in A]
Z = [elem[2] for elem in A]
ax.scatter(X, Y, Z, depthshade=False)
max_range = np.array([max(X)-min(X), max(Y)-min(Y), max(Z)-min(Z)]).max()
Xb = 0.3*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(max(X)+min(X))
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(max(Y)+min(Y))
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(max(Z)+min(Z))
for xb, yb, zb in zip(Xb, Yb, Zb):
    ax.plot([xb], [yb], [zb], 'w')
#plt.savefig(os.path.join(savepath, f"agg{PARTICLE_NUM}-{PARTICLE_NUM}.png"), dpi = 600)
plt.clf()

## Small window
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_aspect('equal')

A_window = [elem for elem in A if -WINDOW <= elem[1] <= WINDOW and -WINDOW <= elem[2] <= WINDOW]
X = [elem[0] for elem in A_window]
Y = [elem[1] for elem in A_window]
Z = [elem[2] for elem in A_window]

ax.scatter(X, Y, Z, depthshade=False)
max_range = np.array([max(X)-min(X), max(Y)-min(Y), max(Z)-min(Z)]).max()
Xb = 0.3*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(max(X)+min(X))
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(max(Y)+min(Y))
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(max(Z)+min(Z))
for xb, yb, zb in zip(Xb, Yb, Zb):
    ax.plot([xb], [yb], [zb], 'w')
#plt.savefig(os.path.join(savepath, f"agg{PARTICLE_NUM}-{PARTICLE_NUM}-windowsize{WINDOW}.png"), dpi = 600)
plt.clf()

## Data visualization

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
    if point[0] > PARTICLE_NUM /2 or point[0] < -PARTICLE_NUM /2 : 
        exterior_border.append(point)
    elif point[0] == PARTICLE_NUM /2 or point[0] == -PARTICLE_NUM /2:
        perfect_border.append(point)
    else:
        interior_border.append(point)

X_interior = [elem[0] for elem in interior_border]
Y_interior = [elem[1] for elem in interior_border]
Z_interior = [elem[2] for elem in interior_border]

X_exterior = [elem[0] for elem in exterior_border]
Y_exterior = [elem[1] for elem in exterior_border]
Z_exterior = [elem[2] for elem in exterior_border]

X_perfect = [elem[0] for elem in perfect_border]
Y_perfect = [elem[1] for elem in perfect_border]
Z_perfect = [elem[2] for elem in perfect_border]

if POSITIVE:
    X = [elem[0] for elem in A_window if elem[0] >= 0]
    Y = [elem[1] for elem in A_window if elem[0] >= 0]
    Z = [elem[2] for elem in A_window if elem[0] >= 0]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_aspect('equal')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis') 
ax.scatter(X, Y, Z, depthshade=False)
ax.scatter(X_interior, Y_interior, Z_interior, depthshade=False, color = 'blue')
ax.scatter(X_exterior, Y_exterior, Z_exterior, depthshade=False, color = 'red')
ax.scatter(X_perfect, Y_perfect, Z_perfect, depthshade=False, color = 'magenta')
for xb, yb, zb in zip(Xb, Yb, Zb):
    ax.plot([xb], [yb], [zb], 'w')
#plt.savefig(os.path.join(savepath, f"agg{PARTICLE_NUM}-{PARTICLE_NUM}-windowsize{WINDOW}-Late-early(1).png"), dpi = 600)
plt.clf()

## Testing voxel

ax = plt.figure().add_subplot(projection='3d')

maxiX = max(max(X_interior), -min(X_interior))
maxiY = max(max(Y_interior), -min(Y_interior))
maxiZ = max(max(Z_interior), -min(Z_interior))

image = np.zeros((maxiX, maxiY, maxiZ))
print(image)

ax.set(xlabel = 'X axis', ylabel = 'Y axis', zlabel = 'Z axis')
ax.set_aspect('equal')
