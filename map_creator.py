import time
from SpringAlgorithm import *
import numpy as np

def map_updater(gal_map, point_graph, gate_graph, scrambler = False, n = 1001):

    start = time.time()
    Xsizes = []
    Ysizes = []
    forces_list = []


    # scrambler: optional module: changes all starting locations to be random
    if scrambler:
        gal_map["Xcor"] = np.random.normal(scale=1600, size=len(gal_map))
        gal_map["Ycor"] = np.random.normal(scale=900, size=len(gal_map))

    for i in range(n):
        new_x, new_y, forces = update_locations_connection_spring(gal_map, point_graph, gate_graph, 0.1)
        gal_map["Xcor"] = new_x
        gal_map["Ycor"] = new_y
        Xsize = (max(gal_map["Xcor"])-min(gal_map["Xcor"]))/200
        Ysize = (max(gal_map["Ycor"])-min(gal_map["Ycor"]))/200
        Xsizes.append(round(Xsize, 2))
        Ysizes.append(round(Ysize, 2))
        avg_force = sum(forces)/len(forces)
        forces_list.append(round(avg_force, 2))

        if i%100==0:
            print(i, int(time.time()-start))
    # print(Xsizes)
    # print(Ysizes)
    # #print(forces)
    # print(avg_distances)
    diagnostics = {
                    "X" : Xsizes,
                    "Y" : Ysizes,
                    "force" : forces

                   }
    return gal_map, diagnostics