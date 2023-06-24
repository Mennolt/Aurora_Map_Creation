import matplotlib.pyplot as plt
import pandas as pd

def draw_map(gal_map, jump_cons, gate_col_dict = None):
    #jump gate colours:
    if gate_col_dict == None:
        gate_col_dict = {0 : "orange",
                        406 : "blue",
                        417 : "green"}
    #now lets visualize the current situation:
    Xsize = (max(gal_map["Xcor"])-min(gal_map["Xcor"]))/200
    Ysize = (max(gal_map["Ycor"])-min(gal_map["Ycor"]))/200
    print(Xsize, Ysize)
    fig, ax = plt.subplots(figsize=(Xsize, Ysize))
    #edges
    #need to draw from x,y of sysID1 to x,y of sysID2
    for line in jump_cons.values:
        x1 = gal_map[gal_map["SystemID"] == line[2]]["Xcor"]#gal_map.loc["Xcor",line[2]]
        x2 = gal_map[gal_map["SystemID"] == line[3]]["Xcor"]
        y1 = gal_map[gal_map["SystemID"] == line[2]]["Ycor"]
        y2 = gal_map[gal_map["SystemID"] == line[3]]["Ycor"]

        colour = gate_col_dict[line[4]]
        plt.plot([x1,x2], [y1,y2], c=colour,lw=1, axes=ax, zorder=-1)
    #vertices
    gal_map.plot(kind="scatter", x="Xcor", y="Ycor", ax=ax)
    gal_map[gal_map["Name"] == "Sol"].plot(kind="scatter", x="Xcor", y="Ycor", ax=ax, c="black", s=50)
    plt.show()

def plot_diagnostics(diagnostics):
    fig, ax = plt.subplots(1)
    plt.plot(diagnostics["X"])
    plt.plot(diagnostics["Y"])
    plt.plot(diagnostics["force"])
    plt.legend([ "Xsizes", "Ysizes", "force"])
    plt.show()