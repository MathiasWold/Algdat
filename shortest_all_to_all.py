""" All-Pairs Shortest Paths solutions using Floyd-Warshall and Johnson """

import sys
from graph_structs import Graph, Vertex
from shortest_one_to_all import bellman_ford, dijkstra


def weight_matrix(G):
    """ Converts and returns G in matrix format, where D[u.rank][v.rank] is equal to weight of edge from u to v """

    n = len(G.V)
    D = [[sys.maxsize for i in range(n)] for i in range(n)]
    for i in range(n):
        D[i][i] = 0

    for u in G.V:
        for v, weight in G.adj(u):
            D[u.rank][v.rank] = weight

    return D


def predecessor_matrix(G):
    """ Returns the predecessor-matrix for G, where P[u.rank][v.rank] is equal to u for edges u -> v """

    n = len(G.V)
    P = [[None for i in range(n)] for i in range(n)]

    for u in G.V:
        for v, weight in G.adj(u):
            P[u.rank][v.rank] = u

    return P


def floyd_warshall(G):
    """ 
    Takes a graph G in matrix-representation as input.\n
    Returns all-pair shortest paths as a matrix D, and the vertex predecessors for the shortest paths as a matrix P 
    """

    n = len(G.V)
    D = weight_matrix(G)
    P = predecessor_matrix(G)

    # prints inital D and P (when k = 0)
    print("D for k = 0")
    for row in D:
        print(row)
    print("P for k = 0")
    print()
    for row in P:
        print(row)
    print()

    for k in range(n):
        for i in range(n):
            for j in range(n):
                # if path i -> k -> j is shorter than i -> j
                if D[i][j] > D[i][k] + D[k][j]:
                    D[i][j] = D[i][k] + D[k][j]
                    P[i][j] = P[k][j]

        # prints D and P for each k
        print(f"D for k = {k + 1}")
        for row in D:
            print(row)
        print()
        print(f"P for k = {k + 1}")
        for row in P:
            print(row)
        print()

    # returns D and P when k = (n-1), resulting in a matrix containing shortest paths between all pairs of nodes in D
    return D, P


def johnson(G):
    """ 
    Finds all-pair shortest paths in sparse graphs using bellman-ford and dijkstra as subroutines. \n
    Returns matrix D with computed shortest paths from u to v in D[u][v]
    """

    # add a new vertex s to a copy of G, called G_s, where there is an edge (s, v, 0) for all v in G.V
    s = Vertex("s", -1)
    for v in G.V:
        s.add_edge(v, 0)
    G_s = Graph(*G.V, s)

    # run bellman-ford to compute v.d from s for all v in G_s.V
    if not bellman_ford(G_s, s):
        raise ValueError("Input graph contains a negative-weight cycle")

    # h is an array satisfying h[v.rank] = v.d, computed from bellman-ford above
    # here v.rank is used as an index
    h = [0 for i in range(len(G_s.V))]
    for v in G_s.V:
        h[v.rank] = v.d

    # make every edge non-negative
    for u in G_s.V:
        for edge in G_s.adj(u):
            # edge format: (v, weight)
            edge[1] = edge[1] + h[u.rank] - h[edge[0].rank]

    # n x n-array for storing computed all-pair shortest paths
    n = len(G.V)
    D = [[None for i in range(n)] for i in range(n)]

    # runs dijkstra for each vertex u in G.V to compute shortest paths from u to all other vertices v
    for u in G.V:
        dijkstra(G, u)
        for v in G.V:
            # redo the re-weighting, and store the shortest paths in D
            D[u.rank][v.rank] = v.d + h[v.rank] - h[u.rank]

    return D


def test1():
    """ Test for floyd-warshall """
    # rank = row/col-index in matrix-representation
    v1 = Vertex("1", 0)
    v2 = Vertex("2", 1)
    v3 = Vertex("3", 2)
    v4 = Vertex("4", 3)
    v5 = Vertex("5", 4)

    v1.add_edge(v2, 3)
    v1.add_edge(v3, 8)
    v1.add_edge(v5, -4)
    v2.add_edge(v4, 1)
    v2.add_edge(v5, 7)
    v3.add_edge(v2, 4)
    v4.add_edge(v1, 2)
    v4.add_edge(v3, -5)
    v5.add_edge(v4, 6)

    g = Graph(v1, v2, v3, v4, v5)
    D, P = floyd_warshall(g)

# test1()


def test2():
    """ Test for johnson """

    # comparator = "d" to make dijksta's min-pri-queue work
    # rank = vertex index to be used in johnsons computation of h(v) = v.d
    v1 = Vertex("1", 0, comparator="d")
    v2 = Vertex("2", 1, comparator="d")
    v3 = Vertex("3", 2, comparator="d")
    v4 = Vertex("4", 3, comparator="d")
    v5 = Vertex("5", 4, comparator="d")

    v1.add_edge(v2, 3)
    v1.add_edge(v3, 8)
    v1.add_edge(v5, -4)
    v2.add_edge(v5, 7)
    v2.add_edge(v4, 1)
    v3.add_edge(v2, 4)
    v4.add_edge(v3, -5)
    v4.add_edge(v1, 2)
    # v1.add_edge(v4, -3)   # remove comment to create a negative cycle
    v5.add_edge(v4, 6)

    g = Graph(v1, v2, v3, v4, v5)
    D = johnson(g)

    for vertex, row in enumerate(D):
        print(f"Shortest paths from {vertex+1} to all:", row)

# test2()


def test3():
    """ Comparing outputs of floyd-warshall and johnson """

    def _init():
        v1 = Vertex("1", 0, comparator="d")
        v2 = Vertex("2", 1, comparator="d")
        v3 = Vertex("3", 2, comparator="d")
        v4 = Vertex("4", 3, comparator="d")
        v5 = Vertex("5", 4, comparator="d")

        v1.add_edge(v2, 3)
        v1.add_edge(v3, 8)
        v1.add_edge(v5, -4)
        v2.add_edge(v5, 7)
        v2.add_edge(v4, 1)
        v3.add_edge(v2, 4)
        v4.add_edge(v3, -5)
        v4.add_edge(v1, 2)
        v5.add_edge(v4, 6)

        g = Graph(v1, v2, v3, v4, v5)

        return g

    g = _init()
    d1 = floyd_warshall(g)[0]
    g = _init()
    d2 = johnson(g)

    print(d1 == d2)

# test3()
