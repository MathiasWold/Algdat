""" Single-Source Shortest Path solutions using Bellman-Ford, DAG-shortest-paths and Dijkstra """

import sys
from graph_structs import Graph, Vertex
from graph_traversal import topological_sort
from heaps import MinHeap

def initialize_single_source(G, s):
    """ Initalization for single source shortest path algorithms """
    for v in G.V:
        v.d = sys.maxsize
        v.p = None
    s.d = 0

def relax(v1, v2):
    """ Relax is used to decrease distance estimate v.d for s to v if possible """
    for v, weight in v1.adj:
        if v == v2:
            if v2.d > v1.d + weight:
                v2.d = v1.d + weight
                v2.p = v1
        # else:
        #     raise ValueError("v1 and v2 does not share an edge")

def bellman_ford(G, s):
    """
        Find shortest paths from s to all other vertices, works with negative edges.\n
        Returns True if there are no negative cycles, otherwise return False
     """
    initialize_single_source(G, s)
    for i in range(len(G.V)-1):
        for u, v, weight in G.E:
            relax(u, v)
    for u, v, weight in G.E:
        if v.d > u.d + weight:
            return False
    return True

def DAG_shortest_paths(G, s):
    """ Find shortest paths from s to all other vertices on a DAG (directed acyclic graph), works with negative edges """
    G.V = topological_sort(G)
    initialize_single_source(G, s)
    q = list(G.V)
    while q:
        u = q.pop(0)
        for v, weigth in G.adj(u):
            relax(u, v)

def dijkstra(G, s):
    """ Find shortest paths from s to all other vertices, works only with non-negative edges """
    initialize_single_source(G, s)
    Q = MinHeap(G.V)
    while Q.size() > 0:
        u = Q.extract_min()
        for v, weight in G.adj(u):
            relax(u, v)
            Q.build_min_heap()


def test1():
    """ Testing Bellman-Ford """
    s = Vertex("s")
    t = Vertex("t")
    x = Vertex("x")
    y = Vertex("y")
    z = Vertex("z")

    s.add_edge(t, 6)
    s.add_edge(y, 7)
    t.add_edge(x, 5)
    t.add_edge(y, 8)
    # y.add_edge(t, -10)    # remove comment to create a negative cycle
    t.add_edge(z, -4)
    x.add_edge(t, -2)
    y.add_edge(x, -3)
    y.add_edge(z, 9)
    z.add_edge(s, 2)
    z.add_edge(x, 7)

    g = Graph(s, t, x, y, z)
    g.print()
    print("Bellman-Ford returns: ", bellman_ford(g, s))
    print(f"Bellman-Ford Shortest path from {s} to...")
    for v in g.V:
        if v != s:
            print(f"{v}: {v.d}")

#test1()

def test2():
    """ Testing DAG-shortest-paths """
    r = Vertex("r")
    s = Vertex("s")
    t = Vertex("t")
    x = Vertex("x")
    y = Vertex("y")
    z = Vertex("z")

    r.add_edge(s, 5)
    r.add_edge(t, 3)
    s.add_edge(x, 6)
    s.add_edge(t, 2)
    t.add_edge(x, 7)
    t.add_edge(y, 4)
    t.add_edge(z, 2)
    x.add_edge(y, -1)
    x.add_edge(z, 1)
    y.add_edge(z, -2)

    g = Graph(r, s, t, x, y,z)
    g.print()
    DAG_shortest_paths(g, s)
    print(f"DAG Shortest paths from {s} to...")
    for v in g.V:
        if v != s:
            print(f"{v}: {v.d}")

#test2()

def test3():
    """ Testing Dijkstra """
    s = Vertex("s", comparator="d")
    t = Vertex("t", comparator="d")
    x = Vertex("x", comparator="d")
    y = Vertex("y", comparator="d")
    z = Vertex("z", comparator="d")

    s.add_edge(t, 10)
    s.add_edge(y, 5)
    t.add_edge(x, 1)
    t.add_edge(y, 2)
    x.add_edge(z, 4)
    y.add_edge(t, 3)
    y.add_edge(x, 9)
    y.add_edge(z, 2)
    z.add_edge(s, 7)
    z.add_edge(x, 6)

    g = Graph(s, t, x, y, z)
    dijkstra(g, s)
    print(f"Dijkstra Shortest paths from {s} to...")
    for v in g.V:
        if v != s:
            print(f"{v}: {v.d}")

#test3()