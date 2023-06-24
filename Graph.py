# creating a more efficient adjacency structure: dict containing Adjacency lists

class Graph():
    def __init__(self, vertices, edges, weights = None):
        """Given a list of vertices, and a list of directed edges (2-tuple (from,to)),
        creates a datastructure to quickly find the existence of an edge"""
        self.con_dict = {i: [] for i in vertices}
        for i, j in edges:
            self.con_dict[i].append(j)
        if weights:
            self.weight_dict = {}
            for i,j,weight in weights:
                self.weight_dict[(i,j)] = weight

    def exists(self, i, j):
        """Returns True is i->j exists, False otherwise"""
        return j in self.con_dict[i]

    def degree(self, i):
        return len(self.con_dict[i])