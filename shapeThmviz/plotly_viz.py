"""
3d plotting with Plotly
"""
import os
from ast import literal_eval
from tqdm import tqdm
import pandas as pd
from plotly import express as px

FOLDER_NAME = 'shapeThm-agg'
WINDOW = 10
PARTICLE_NUM = 30
POSITIVE = True #only look at positive values of x for aggregate
PROJ = True

if __name__ == "__main__":
    root_file = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\{FOLDER_NAME}"
    A = open(os.path.join(root_file, f"agg{PARTICLE_NUM}-{PARTICLE_NUM}.txt"), "r").read()
    A = literal_eval(A)  # make it an array
    # convert to pandas dataframe
    import ipdb; ipdb.set_trace()
    df = pd.DataFrame(A, columns=["X", "Y", "Z"])

    #only keep points that are in the window (i.e. -WINDOW <= Y <= WINDOW and -WINDOW <= Z <= WINDOW)
    df = df[(df["Y"] >= -WINDOW) & (df["Y"] <= WINDOW) & (df["Z"] >= -WINDOW) & (df["Z"] <= WINDOW)]
    
    # put green color for interior points (i.e. points on the x border with X < 15)
    # put red color for border points (i.e. points on the x border with X = 15)
    # put blue color for other points
    colors = []
    # loop over points in the dataframe
    for i in tqdm(range(len(df))):
        point_x = df.iloc[i]["X"]
        point_y = df.iloc[i]["Y"]
        point_z = df.iloc[i]["Z"]

        # get the max along the x axis for the current y and z
        max_x = df[(df["Y"] == point_y) & (df["Z"] == point_z)]["X"].max()
        if point_x < max_x:
            colors.append("blue")
        elif point_x == max_x and (point_x < 15 or point_x > 15):
            colors.append("green")
        else:
            colors.append("red")
    df["colors"] = colors

    # plot the dataframe with plotly
    # only plots points with 10 < X < 20
    df["markers"] = [0 for i in range(len(df))]
    df = df[(df["X"] >= 10) & (df["X"] <= 20)]
    fig = px.scatter_3d(df, x="X", y="Y", z="Z", color="colors", symbol="markers", symbol_sequence=["square"])
    fig.update_traces(marker=dict(size=10))
    fig.show()