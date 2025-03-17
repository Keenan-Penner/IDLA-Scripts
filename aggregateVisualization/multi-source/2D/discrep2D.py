import os
from ast import literal_eval
from tqdm import tqdm
import numpy as np
from matplotlib import animation
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from argparse import ArgumentParser

def swap(e):
    return (e[1], e[0]) #swaps the vertices of an edge 

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--root",
        type=str,
        default="C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\multi-source\\An-dagger\\2D\\",
    )
    parser.add_argument(
        "--folder",
        type=str,
        default="sim2",
    )
    parser.add_argument( # file containing the points of the big aggregate
        "--aggfile",
        type=str,
        default="agg",
    )
    parser.add_argument( # file containing vertices common to both, but reached using different particles
        "--discfile",
        type=str,
        default="disc",
    )
    parser.add_argument( # file containing edges common to both forests
        "--edgefile",
        type=str,
        default="edges", 
    )
    parser.add_argument( # file containing edges common to both forests
        "--forest1file",
        type=str,
        default="smallforest", 
    )
    parser.add_argument( # file containing edges common to both forests
        "--forest2file",
        type=str,
        default="bigforest", 
    )
    parser.add_argument( 
        "--axis_off",
        action="store_true",
        help="Remove the axis from the plot",
    )
    args = parser.parse_args()
    root_file = os.path.join(args.root, args.folder)

    points = open(os.path.join(root_file, f"{args.aggfile}.txt"), "r").read()
    points = literal_eval(points)  # make it an array

    edges= open(os.path.join(root_file, f"{args.edgefile}.txt"), "r").read()
    edges = literal_eval(edges)  # make it an array

    disc = open(os.path.join(root_file, f"{args.discfile}.txt"), "r").read()
    disc = literal_eval(disc)  # make it an array

    fig, ax = plt.subplots()
    
    ##AGGREGATE
    xpoints=[points[i][0] for i in range(len(points))]
    ypoints=[points[i][1] for i in range(len(points))]

    max_x = max(abs(min(xpoints)), max(xpoints))
    max_y = max(abs(min(ypoints)), max(ypoints))

    print(max_x, max_y)

    ax.scatter(xpoints, ypoints, s=2, color = 'red')
    #plt.axis('square')
    extremum = max(max_x, max_y)
    ax.set_xlim(-40, 40)
    #ax.set_xlim(-max_x - 2, max_x + 2)
    #ax.set_ylim(-120, -40)
    ax.set_ylim(-40, 40)
    #ax.set_ylim(-max_y - 2, max_y + 2)
    ax.set_aspect('equal')
    
    ##FOREST
    for edge in edges:
            x1, y1 = edge[0]
            x2, y2 = edge[1]
            # If the two points are the same, plot a single point
            if x1 == x2 and y1 == y2:
                ax.scatter(x1, y1, color='green', s=2)  # Plot root as a point
            else:
                ax.plot([x1, x2], [y1, y2], linewidth=1, color='green')  # Plot edge
    #plt.axis('square')
    #plt.xlim(-extremum - 1, extremum + 1)
    #plt.ylim(-extremum - 1, extremum + 1)
    xdisc=[disc[i][0] for i in range(len(disc))]
    ydisc=[disc[i][1] for i in range(len(disc))]
    ax.scatter(xdisc, ydisc, s=2, color = 'blue')
    plt.savefig(f'{root_file}\\forest_zoomtest2.png', dpi=500)
    if args.axis_off:
        ax.set_axis_off()
        plt.savefig(f'{root_file}\\forest_zoomtest_axisoff.png', dpi=500)
    plt.show()
    plt.close()
'''
    f1_edges = open(os.path.join(root_file, f"{args.forest1file}.txt"), "r").read()
    f1_edges = literal_eval(f1_edges)  # make it an array
    
    f2_edges = open(os.path.join(root_file, f"{args.forest2file}.txt"), "r").read()
    f2_edges = literal_eval(f2_edges)  # make it an array
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    ax1.set_xlim(-max_x - 1, max_x + 1)
    ax1.set_ylim(-max_y - 1, max_y + 1)
    ax1.set_aspect('equal')

    ax2.set_xlim(-max_x - 1, max_x + 1)
    ax2.set_ylim(-max_y - 1, max_y + 1)
    ax2.set_aspect('equal')

    different_edges = []
    for e in f1_edges:
        if e not in f2_edges and swap(e) not in f2_edges:
            different_edges.append(e)
    ##FOREST
    # we plot the big forest
    for i in range(len(f2_edges)):
        ax1.plot([f2_edges[i][0][0],f2_edges[i][1][0]],[f2_edges[i][0][1],f2_edges[i][1][1]],linewidth=0.5,color='green')
    # we plot the small forest
    for i in range(len(f1_edges)):
        ax2.plot([f1_edges[i][0][0],f1_edges[i][1][0]],[f1_edges[i][0][1],f1_edges[i][1][1]],linewidth=0.5,color='green')
    for i in range(len(different_edges)):
        ax2.plot([different_edges[i][0][0],different_edges[i][1][0]],[different_edges[i][0][1],different_edges[i][1][1]],linewidth=0.5,color='red')
    #plt.savefig(f'{root_file}\\forest.png', dpi=500)
    plt.show()
    plt.clf()
    '''