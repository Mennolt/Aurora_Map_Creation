import sqlite3
import pandas as pd

def getMap(filename):
    """
    With filename a .db Aurora savefile,
    gets the galaxy map and jump points from that savefile
    """
    con = sqlite3.connect(filename)

    # the current map
    gal_map = pd.read_sql_query(
        "Select name, xcor, ycor, controlRaceID, systemID from fct_racesyssurvey where gameid=91 and raceid=406", con)
    # jump points between systems
    jump_cons = pd.read_sql_query("""select JP1.WarpPointID, JP2.WarpPointID, JP1.SystemID as SysID1, JP2.SystemID as SysID2, JP1.JumpGateRaceID
                                from FCT_JumpPoint as JP1, FCT_JumpPoint as JP2, FCT_racesyssurvey as survey1, FCT_racesyssurvey as survey2
                                where JP1.gameid = 91 and JP2.gameid=91 and
                                JP1.WPLink = JP2.WarpPointID and
                                JP1.SystemID = survey1.SystemID and JP2.systemid=survey2.systemID and
                                survey1.gameid = 91 and survey2.gameid = 91 and
                                survey1.raceid = 406 and survey2.raceid = 406""", con)
    jump_cons.sort_values(by=["SysID1", "SysID2"])
    con.close()
    return gal_map, jump_cons

def saveMap(filename, gal_map):
    #now lets add the data back into a DB
    con = sqlite3.connect(filename)
    cur = con.cursor()

    query = """UPDATE FCT_raceSysSurvey SET Xcor = ?, Ycor = ? WHERE SystemID = ?"""
    cur.executemany(query, tuple(zip(gal_map["Xcor"], gal_map["Ycor"], gal_map["SystemID"])))

    con.commit()
    print("Total", cur.rowcount, "Records updated successfully")
    cur.close()
    con.close()


# def create_dist_graph(gal_map, jumpPoints, dbfile):
#     from Graph import Graph
#     #find distance from each point to its neighbours
#     for system in gal_map["SystemID"]:
#         query = """SELECT """
#
#     # find the distances (pairwise) of each point
#     # construct a graph that has actual distances