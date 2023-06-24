from DatabaseFunctions import *
from Visualization import draw_map, plot_diagnostics

from Graph import Graph
from map_creator import map_updater

if __name__ == '__main__':

    checkpoint = 3
    scramble = False
    final = False
    N = 101
    dbfile = "AuroraDB.db"

    if not checkpoint:
        #get data from the database
        starMap, jumpPoints = getMap(dbfile)
        #draw_map(starMap, jumpPoints)
        checkpoint = 1
    else:
        #get data from intermediate results
        starMap = pd.read_csv(f"data/stars{checkpoint}.csv")
        jumpPoints = pd.read_csv(f"data/jumpPoints{checkpoint}.csv")
        checkpoint += 1


    if final:
        #save existing results into DB, then exit
        saveMap(dbfile, starMap)
    else:
        #update existing results:

        #create graphs of jump points and jump gates
        edges = [(line[2], line[3]) for line in jumpPoints.values]
        point_graph = Graph(starMap["SystemID"], edges)

        gatesdf = jumpPoints[jumpPoints["JumpGateRaceID"] != 0]
        gate_edges = [(line[2], line[3]) for line in gatesdf.values]
        gates_graph = Graph(starMap["SystemID"], gate_edges)

        #update the graph
        new_map, diagnostics = map_updater(starMap, point_graph, gates_graph, scramble, n = N)
        draw_map(new_map, jumpPoints)
        #plot_diagnostics(diagnostics)

        #save resulting dataframes as checkpoint csvs
        new_map.to_csv(f"data/stars{checkpoint}.csv", index=False)
        jumpPoints.to_csv(f"data/jumpPoints{checkpoint}.csv", index=False)
