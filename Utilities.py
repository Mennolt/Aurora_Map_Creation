def dist(x,y,x2,y2):
    return ((x-x2)**2+(y-y2)**2)**0.5
def force_distribution(x,y,x2,y2):
    """Calculates how to distribute force to x and y forces to the total force is parallel to the x1,y1 -> x2,y2 line,
       repelling"""
    x_dist = x-x2
    y_dist = y-y2
    tot_dist = dist(x,y,x2,y2)
    return x_dist/tot_dist, y_dist/tot_dist