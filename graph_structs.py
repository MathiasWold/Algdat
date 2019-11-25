""" Vertex and Graph """

class Vertex:
    """ Class for generic vertex to be used in graph algorithms """
    
    def __init__(self, name=None, rank=None, comparator="rank"):
        """ 
            Name is optional, but is usually a number that represents the vertex.
            Rank is optional, but is usually the vertex's value
        """
        self.color = None
        self.d = None
        self.f = None
        self.p = None
        self.adj = []
        self.name = name
        self.rank = rank
        self.comparator = comparator
        
    
    def add_edge(self, vertex, weight=0):
        """ Add a directed edge from self to vertex and saves it in self.adj, tupled with weight """
        if not vertex in self.adj:
            self.adj.append((vertex, weight))

    def __lt__(self, other):
        """ Makes it possible to compare vertices by their ranks/value or d """
        if self.comparator == "d":
            return self.d < other.d
        else:
            return self.rank < other.rank

    def __repr__(self):
        """ Makes debugging easier :) """
        if self.name:
            return str(self.name)
            #return str(self.rank)
        else:
            return "Vertex"
    
class Graph:
    """ Class for graphs used in graph algorithms """
    
    def __init__(self, *vertices):
        """
            Initalizes with an optional number of vertices, and adds all vertex-edges as tuples to a list.
            These tuples contains the weight of the edge if present.
        """
        self.V = [v for v in vertices]
        self.E = []
        for u in self.V:
            for v in u.adj:
                if type(v) == tuple:
                    # tuple ==> edge is weighted
                    # edge format: (u, v, weight)
                    self.E.append((u, v[0], v[1]))
                else:
                    # edge not weighted
                    # edge format: (u, v)
                    self.E.append((u, v))

    def adj(self, vertex):
        """ Returns the adjacency list for a gived vertex in the graph """
        if vertex in self.V:
            return vertex.adj
        else:
            raise ValueError("Vertex not in graph")

    def print(self):
        """ Prints every vertex in the graph with its edges (and possible weights) in a readable format """
        print("Graph:")
        print("Edges: " + str(self.E))
        for v in self.V:
            print(f"{v} -> {v.adj}")
        print()



v1 = Vertex(1, 9)
v2 = Vertex(2, 3)

#print(v1 > v2)