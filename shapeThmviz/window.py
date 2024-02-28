import os
from ast import literal_eval
import matplotlib.pyplot as plt
import numpy as np

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

ax.scatter(X, Y, Z, depthshade=False)
max_range = np.array([max(X)-min(X), max(Y)-min(Y), max(Z)-min(Z)]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(max(X)+min(X))
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(max(Y)+min(Y))
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(max(Z)+min(Z))
for xb, yb, zb in zip(Xb, Yb, Zb):
    ax.plot([xb], [yb], [zb], 'w')
# plt.savefig(os.path.join(savepath, f"agg{PARTICLE_NUM}-{PARTICLE_NUM}-windowsize{WINDOW}.png"), dpi = 600)
plt.show()
plt.clf()