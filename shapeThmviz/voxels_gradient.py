"""
Visualisation of the point cloud using voxels
"""
import os
from ast import literal_eval
from tqdm import tqdm
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

FOLDER_NAME = 'shapeThm-agg'
WINDOW = 10
PARTICLE_NUM = 30
POSITIVE = True #only look at positive values of x for aggregate
PROJ = True

if __name__ == "__main__":
    root_file = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\{FOLDER_NAME}"
    A = open(os.path.join(root_file, f"agg{PARTICLE_NUM}-{PARTICLE_NUM}.txt"), "r").read()
    A = literal_eval(A)  # make it an array
    A = np.array(A)
    # convert to pandas dataframe

    # only keep points that are in the window (i.e. -WINDOW <= Y <= WINDOW and -WINDOW <= Z <= WINDOW)
    A = A[(A[:, 1] >= -WINDOW) & (A[:, 1] <= WINDOW) & (A[:, 2] >= -WINDOW) & (A[:, 2] <= WINDOW)]

    # put green color for interior points (i.e. points on the x border with X < 15)
    # put red color for border points (i.e. points on the x border with X = 15)
    # put blue color for other points
    voxel_grid = np.zeros((31, WINDOW*2+1, WINDOW*2+1))
    colors = np.empty(voxel_grid.shape, dtype=object)

    # loop over points in the array
    for point in tqdm(A):
        point_x = point[0]
        point_y = point[1]
        point_z = point[2]

        # get the max along the x axis for the current y and z
        max_x = np.max(A[(A[:, 1] == point_y) & (A[:, 2] == point_z)][:, 0])
        voxel_x = point_x + 15  #this is to be confirmed with other point clouds
        voxel_y = point_y + WINDOW
        voxel_z = point_z + WINDOW

        dist_to_max = abs(max_x - point_x)

        # put a color depending on the distance to the max (continuous color scale from red to blue)
        colors[voxel_x, voxel_y, voxel_z] = [1 - dist_to_max / 15, 0, dist_to_max / 15, 1]
        voxel_grid[voxel_x, voxel_y, voxel_z] = 1
        
        """
        if point_x == max_x :
            # voxel_grid[voxel_x, voxel_y, voxel_z] = 2
            colors[voxel_x, voxel_y, voxel_z] = "red"
            voxel_grid[voxel_x, voxel_y, voxel_z] = 1
        elif point_x == max_x - 1 :
            # voxel_grid[voxel_x, voxel_y, voxel_z] = 2
            colors[voxel_x, voxel_y, voxel_z] = "green"
            voxel_grid[voxel_x, voxel_y, voxel_z] = 1
        elif point_x == max_x - 2:
            # voxel_grid[voxel_x, voxel_y, voxel_z] = 2
            colors[voxel_x, voxel_y, voxel_z] = "dodgerblue"
            voxel_grid[voxel_x, voxel_y, voxel_z] = 1
        else:
            # voxel_grid[voxel_x, voxel_y, voxel_z] = 3
            colors[voxel_x, voxel_y, voxel_z] = "lightblue"
            voxel_grid[voxel_x, voxel_y, voxel_z] = 1
        """

    #plot the voxel grid with matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # equal aspect ratio
    # only keep the slice such that x > 25
    voxel_grid = voxel_grid[25:, :, :]
    colors = colors[25:, :, :]
    ax.voxels(voxel_grid, facecolors=colors, edgecolor='k')
    ax.set_box_aspect([1,1,1])
    ax.set_aspect('equal')
    plt.show()