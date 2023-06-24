from SpringUtilities import *

# now for an algorithm to improve this:
# general idea: all points repel each other (slightly), but are attracted to 0,0 and to points they are connected to
# maybe stuff with the same control race extra attracts each other? Might need to manually change the control race for my actual colonized area

# iterate the algorithm until a nice picture emerges
def update_locations_connection_spring(gal_map, point_graph, gates_graph, global_force_mult=1):
    new_x = []
    new_y = []
    forces = []
    for x, y, SysID in zip(gal_map["Xcor"], gal_map["Ycor"], gal_map["SystemID"]):
        x_force = 0
        y_force = 0
        # force by other points
        for x2, y2, SysID2 in zip(gal_map["Xcor"], gal_map["Ycor"], gal_map["SystemID"]):
            if SysID2 == SysID:
                continue
            connected = point_graph.exists(SysID, SysID2)  # False if non connected, True otherwise
            gate = gates_graph.exists(SysID, SysID2)

            x_part, y_part = interaction_forces_default(x,y,x2,y2,connected, gate, global_force_mult)
            x_force += x_part
            y_force += y_part


        # force by attraction to the center:
        distance = dist(x, y, 0, 0)
        if distance > 1:
            compensated_distance = (((x ** 2) * 81 + (y ** 2) * 256) ** 0.5) / (
                        9 * 16)  # distance such that shape of monitor is preferred
            force_strength = -global_force_mult * (compensated_distance ** 1.2) / 200  # higher if further from center
            x_part, y_part = force_distribution(x, y, 0, 0)
            x_force += x_part * (9 / 16) * force_strength
            y_force += y_part * (16 / 9) * force_strength

        # updating the output
        new_x.append(x + x_force)
        new_y.append(y + y_force)
        forces.append((x_force ** 2 + y_force ** 2) ** 0.5)
    return new_x, new_y, forces

def update_locs_towards_real_dist(gal_map, jumpPoints, dist_graph, global_force_mult=1):
    """
    Graph updating algorithm that tries to approximate the distances that exist in reality
    :param gal_map: FCT_RaceSysSurvey table
    :param jumpPoints: FCT_JumpPoints table
    :param global_force_mult: float, used to finetune force strength
    :return: x_new, y_new: updated locations for all points in gal_map
    """
    #find the distances (pairwise) of each point
    #construct a graph that has actual distances


