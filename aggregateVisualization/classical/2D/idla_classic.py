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
        "--root",
        type=str,
        default="C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\",
    )
    parser.add_argument(
        "--folder",
        type=str,
        default="classical_IDLA",
    )
    parser.add_argument(
        "--sim_number",
        type=int,
        default="1",
    )
    parser.add_argument( # file containing the points of the aggregate
        "--aggfile",
        type=str,
        default="agg",
    )
    parser.add_argument( # file containing edges of the aggregate
        "--edgefile",
        type=str,
        default="edges", 
    )
    parser.add_argument(
        "--window",
        action="store_true",
    )
    parser.add_argument(
        "--draw",
        action="store_true",
    )
    args = parser.parse_args()
    root_file = os.path.join(args.root, args.folder)
    root_file = os.path.join(root_file, f"sim{args.sim_number}")

    points = open(os.path.join(root_file, f"{args.aggfile}.txt"), "r").read()
    points = literal_eval(points)  # make it an array

    edges= open(os.path.join(root_file, f"{args.edgefile}.txt"), "r").read()
    edges = literal_eval(edges)  # make it an array

    fig, ax = plt.subplots()
    if args.window:
        ax.set_xlim(30, 70)
        ax.set_ylim(-20, 20)
        # Remove ticks on x and y axes
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    ##FOREST
    for edge in edges:
            x1, y1 = edge[0]
            x2, y2 = edge[1]
            
            ax.plot([x1, x2], [y1, y2], linewidth=0.5, color='blue')  # Plot edge
    if args.draw:
    #draw square of [30,70]x[-20,20]
        ax.plot([30, 70], [-20, -20], color='black')
        ax.plot([30, 70], [20, 20], color='black')
        ax.plot([30, 30], [-20, 20], color='black')
        ax.plot([70, 70], [-20, 20], color='black')
    ax.set_aspect('equal')
    plt.savefig(f'{root_file}\\tree_square{args.sim_number}.png', dpi=500)
    plt.show()
    plt.close()
    