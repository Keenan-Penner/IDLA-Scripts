"""
Visualisation of the point cloud using voxels
"""
import os
from ast import literal_eval
from tqdm import tqdm
import numpy as np
from matplotlib import animation
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--fill",
        action="store_true",
        help="Fill value for the useless points"
    )
    parser.add_argument(
        "--slice",
        action="store_true",
        help="Slice the voxel grid such that x >= 20"
    )
    parser.add_argument(
        "--animate",
        action="store_true",
        help="Animate the plot"
    )
    parser.add_argument(
        "--root",
        type=str,
        default="C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\",
    )
    parser.add_argument(
        "--folder",
        type=str,
        default="shapeThm-agg",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=10, 
    )
    parser.add_argument(
        "--particle_num",
        type=int,
        default=30, # this has to be divisible by 2
    )
    parser.add_argument(
        "--fullPlot",
        action="store_true",
        help="Plot the full plot"
    )
    parser.add_argument(
        "--file",
        type=str,
        default="agg30-30.txt",
    )
    args = parser.parse_args()
    root_file = os.path.join(args.root, args.folder)
    A = open(os.path.join(root_file, f"{args.file}.txt"), "r").read()
    A = literal_eval(A)  # make it an array
    A = np.array(A)

    if args.fullPlot: # if we want to plot the full aggregate
        
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
        plt.show()

    else: # if we want to plot the windowed aggregate

        # only keep points that are in the window (i.e. -WINDOW <= Y <= WINDOW and -WINDOW <= Z <= WINDOW)
        A = A[(A[:, 1] >= -args.window) & (A[:, 1] <= args.window) & (A[:, 2] >= -args.window) & (A[:, 2] <= args.window)]

        # get maximum x value
        global_maxi_x = np.max(A[:, 0])

        # get minimum x value
        global_mini_x = np.min(A[:, 0])

        # get max x-value along the y and z axis (for all y, z pairs)
        max_x = np.array([np.max(A[(A[:, 1] == i) & (A[:, 2] == j)][:, 0]) for i in range(-args.window, args.window + 1) for j in range(-args.window, args.window + 1)])
        # reshape the array to have first corrdinate the y and second the z
        max_x = max_x.reshape((args.window*2+1, args.window*2+1))
        # same for min x
        min_x = np.array([np.min(A[(A[:, 1] == i) & (A[:, 2] == j)][:, 0]) for i in range(-args.window, args.window + 1) for j in range(-args.window, args.window + 1)])
        min_x = min_x.reshape((args.window*2+1, args.window*2+1))

        # put green color for interior points (i.e. points on the x border with X < 15)
        # put red color for border points (i.e. points on the x border with X = 15)
        # put white color for other points
        voxel_grid = np.zeros((global_maxi_x - global_mini_x + 1, args.window*2+1, args.window*2+1))
        colors = np.empty(voxel_grid.shape, dtype=object)

        # loop over points in the array
        for point in tqdm(A):
            point_x = point[0]
            point_y = point[1]
            point_z = point[2]

            # get the max along the x axis for the current y and z
            current_max_x = max_x[point_y + args.window, point_z + args.window]
            current_min_x = min_x[point_y + args.window, point_z + args.window]
            """
            max_x = np.max(A[(A[:, 1] == point_y) & (A[:, 2] == point_z)][:, 0])
            min_x = np.min(A[(A[:, 1] == point_y) & (A[:, 2] == point_z)][:, 0])
            """
            voxel_x = point_x + abs(global_mini_x)
            voxel_y = point_y + args.window
            voxel_z = point_z + args.window
            if current_min_x < point_x < current_max_x:
                # voxel_grid[voxel_x, voxel_y, voxel_z] = 1
                colors[voxel_x, voxel_y, voxel_z] = "white"
                voxel_grid[voxel_x, voxel_y, voxel_z] = args.fill
            elif (point_x == current_max_x or point_x == current_min_x) and (0 < point_x < args.particle_num /2 or 0 > point_x > -args.particle_num /2):
                # voxel_grid[voxel_x, voxel_y, voxel_z] = 2
                colors[voxel_x, voxel_y, voxel_z] = "green"
                voxel_grid[voxel_x, voxel_y, voxel_z] = 1
            elif (point_x == current_max_x or point_x == current_min_x) and (point_x > args.particle_num /2 or point_x < -args.particle_num /2):
                # voxel_grid[voxel_x, voxel_y, voxel_z] = 2
                colors[voxel_x, voxel_y, voxel_z] = "red"
                voxel_grid[voxel_x, voxel_y, voxel_z] = 1
                #print(point_x, current_max_x, current_min_x, point_y, point_z, voxel_x, voxel_y, voxel_z)
            else:
                # voxel_grid[voxel_x, voxel_y, voxel_z] = 3
                colors[voxel_x, voxel_y, voxel_z] = "royalblue"
                voxel_grid[voxel_x, voxel_y, voxel_z] = 1


        #plot the voxel grid with matplotlib
        fig = plt.figure()
        # slice such that x >= 0
        if args.slice:
            voxel_grid = voxel_grid[- global_mini_x:, :, :]
            colors = colors[-global_mini_x:, :, :]
        ax = fig.add_subplot(111, projection='3d')

        x, y, z = np.indices((voxel_grid.shape[0] + 1, voxel_grid.shape[1] + 1, voxel_grid.shape[2] + 1))
        if not args.slice:
            x += global_mini_x
        y -= args.window
        z -= args.window

        suffix = "_sliced" if args.slice else ""

        # Plot or animate the voxel grid

        if not args.animate: # if we don't want to animate the plot
            ax.voxels(x, y, z, voxel_grid, facecolors=colors, edgecolor='k')
            if args.slice:
                plt.xticks(np.arange(0, global_maxi_x + 1, 5))
            else:
                #plt.xticks(np.arange(global_mini_x, global_maxi_x + 1, 5))
                plt.xticks(np.arange(-args.particle_num /2 - 5, args.particle_num /2 + 5, 5))
            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            ax.set_zlabel('Z axis') 
            ax.set_box_aspect([1, 1, 1])
            ax.set_aspect('equal')
            #plt.savefig(os.path.join(args.root, args.folder, f"voxels_window{suffix}"))
            plt.show()
        else: # if we want to animate the plot
            def init():
                ax.voxels(x, y, z, voxel_grid, facecolors=colors, edgecolor='k')
                if args.slice:
                    plt.xticks(np.arange(0, global_maxi_x + 1, 5))
                else:
                    #plt.xticks(np.arange(global_mini_x, global_maxi_x + 1, 5))
                    plt.xticks(np.arange(-args.particle_num /2 - 5, args.particle_num /2 + 5, 5))
                ax.set_xlabel('X axis')
                ax.set_ylabel('Y axis')
                ax.set_zlabel('Z axis') 
                ax.set_box_aspect([1, 1, 1])
                ax.set_aspect('equal')
                return fig,

            def animate(i):
                ax.view_init(elev=2., azim=i)
                return fig,

            # Animate
            anim = animation.FuncAnimation(fig, animate, init_func=init,
                                        frames=360, interval=20, blit=True)
            # Save
            anim.save(os.path.join(args.root, args.folder, f"voxels_window_anim{suffix}.mp4"), fps=30, extra_args=['-vcodec', 'libx264'])
