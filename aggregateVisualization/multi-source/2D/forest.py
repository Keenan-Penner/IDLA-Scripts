import os
from ast import literal_eval
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

def connected(edge1, edge2):
        point11 = edge1[0]
        point12 = edge1[1]
        point21 = edge2[0]
        point22 = edge2[1]
        
        return point11 == point21 or point11 == point22 or point12 == point21 or point12 == point22
    
def dfs(root, forest, visited):
    # Perform Depth-First Search (DFS) to find all edges connected to the root
    stack = [root]
    connected_edges = [root]
    visited.add(tuple(map(tuple, root)))  # Convert edge to tuple of tuples to make it hashable
    while stack:
        edge = stack.pop()
        for other_edge in forest:
            if tuple(map(tuple, other_edge)) not in visited and connected(edge, other_edge):
                visited.add(tuple(map(tuple, other_edge)))  # Convert edge to tuple of tuples
                connected_edges.append(other_edge)
                stack.append(other_edge)
    return connected_edges

def group_edges(forest):
    # This function identifies groups of connected edges (branches) for each root
    visited = set()
    groups = []
    for edge in forest:
        if tuple(map(tuple, edge)) not in visited:  # Convert edge to tuple of tuples to make it hashable
            # Use DFS to get all edges connected to this root (i.e., the entire branch)
            connected_edges = dfs(edge, forest, visited)
            groups.append(connected_edges)
    return groups

def darken_colormap(colormap, factor=0.7):
    """
    Darkens the colormap by adjusting the value (brightness) component of its colors.
    factor < 1 will darken the colors.
    """
    # Get the colormap colors
    colors = colormap(np.linspace(0, 1, colormap.N))
    
    # Convert each color from RGB to HSV, adjust brightness, then convert back
    darkened_colors = []
    for color in colors:
        hsv = rgb_to_hsv(color[:3])  # Ignore alpha
        hsv = (hsv[0], hsv[1], hsv[2] * factor)  # Darken the color by reducing the value component
        darkened_colors.append(hsv_to_rgb(hsv))  # Convert back to RGB
    
    # Create a new colormap from the darkened colors
    return cm.colors.ListedColormap(darkened_colors)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--root",
        type=str,
        default="C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\multi-source\\An-dagger\\2D\\",
    )
    parser.add_argument(
        "--sim_number",
        type=int,
        default="1",
    )
    parser.add_argument( # file containing edges of the aggregate
        "--forest", 
        type=str,
        default="bigforest", 
    )
    parser.add_argument(
        "--window",
        action="store_true",
    )
    parser.add_argument(
        "--draw",
        action="store_true",
        help="Draw a black box around a specific region",
    )
    parser.add_argument(
        "--color",
        action="store_true",
        help="draw each forest in a separate color",
    )
    args = parser.parse_args()
    
    root_file = os.path.join(args.root, f"sim{args.sim_number}")

    forest = open(os.path.join(root_file, f"{args.forest}.txt"), "r").read()
    forest = literal_eval(forest)  #make it an array

    fig, ax = plt.subplots()
    if args.window:
        #ax.set_xlim(0, 40)
        ax.set_ylim(-40, 40)
        # Remove ticks on x and y axes
        #plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        #plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

    ##FOREST
    for edge in forest:
            x1, y1 = edge[0]
            x2, y2 = edge[1]
            # If the two points are the same, plot a single point
            if x1 == x2 and y1 == y2:
                ax.scatter(x1, y1, color='blue', s=0.5)  # Plot root as a point
            else:
                ax.plot([x1, x2], [y1, y2], linewidth=0.5, color='blue')  # Plot edge
    if args.draw:
    #draw square of [30,70]x[-20,20]
        ax.plot([0, 40], [-20, -20], color='black')
        ax.plot([0, 40], [20, 20], color='black')
        ax.plot([0, 0], [-20, 20], color='black')
        ax.plot([40, 40], [-20, 20], color='black')
    ax.set_aspect('equal')
    plt.savefig(f'{root_file}\\forest_cap{args.sim_number}.png', dpi=500)
    plt.show()
    plt.close()

    if args.color:
        groups = group_edges(forest)
        num_forests = len(groups)
        print(groups)
        colormap = plt.cm.get_cmap('tab20', num_forests)
        colormap = darken_colormap(colormap, factor=0.7) #we darken the colors to make them more distinct
        for index, group in enumerate(groups):
            for edge in group:
                x1, y1 = edge[0]
                x2, y2 = edge[1]
                # If the two points are the same, plot a single point
                if x1 == x2 and y1 == y2: #the edge is actually a root
                    ax.scatter(x1, y1, color= colormap(index), s=0.5)  # Plot root as a point
                else:
                    ax.plot([x1, x2], [y1, y2], linewidth=1, color=colormap(index))  # Plot edge
        ax.set_aspect('equal')
        plt.savefig(f'{root_file}\\forest_colored{args.sim_number}.png', dpi=500)
        plt.show()
        plt.close()
    