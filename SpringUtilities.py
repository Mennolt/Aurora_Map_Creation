from Utilities import *

def connected_pull(x1,y1,x2,y2, min_force,stable_dist = 150,  force_mult=1):
    """Calculates the pull for 2 connected nodes"""
    force_strength = force_mult * max((-dist(x1, y1, x2, y2) + stable_dist) / 50, min_force)
    x_part, y_part = force_distribution(x1, y1, x2, y2)
    x_force = x_part * force_strength
    y_force = y_part * force_strength
    return x_force, y_force

def interaction_forces_default(x1,y1,x2,y2, connection, gate, global_force_mult):
    """
    Calculates interaction forces for 2 points which may or may not be connected
    x1,y1,x2,y2: coordinates for the vertices
    connection: whether there is any connection between the vertices (jump points)
    gate: whether there is a jump gate between the vertices
    """

    x_force = 0
    y_force = 0
    # if connected: add a force pulling it towards a distance of 200
    if connection:
        # idea: add a modifier that increases ideal distance for high degree nodes
        # (does need to be tuned to keep degree 2/3 the same)

        if gate:  # this line time bottleneck, streamline with graph of gates?
            # stronger force if jump gate
            x_part, y_part = connected_pull(x1, y1, x2, y2, -100, 100, 200 * global_force_mult)
        else:
            x_part, y_part = connected_pull(x1, y1, x2, y2, -50, 150, 50 * global_force_mult)

        x_force += x_part
        y_force += y_part

    else:
        # non-connected vertices repel each other
        force_strength = 7500 * global_force_mult / (dist(x1, y1, x2, y2) ** 2)  # higher if closer
        x_part, y_part = force_distribution(x1, y1, x2, y2)
        x_force += x_part * force_strength
        y_force += y_part * force_strength
    return x_force, y_force