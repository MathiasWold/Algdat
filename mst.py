""" Minimum Spanning Trees using Kruskal and Prim """

import sys
from queue import PriorityQueue
from graph_structs import Graph, Vertex
from heaps import MinHeap


def make_set(v):
    """ Initializes a set with only one vertex """
    v.p = v
    v.rank = 0


def union(v1, v2):
    """ Unites two vertices by linking their roots """
    link(find_set(v1), find_set(v2))


def link(v1, v2):
    """ Links two vertices by looking at their ranks """
    if v1.rank > v2.rank:
        v2.p = v1
    else:
        v1.p = v2
        if v1.rank == v2.rank:
            v2.rank += 1


def find_set(v):
    """ Finds the root of the set containing v """
    if v != v.p:
        v.p = find_set(v.p)
    return v.p


def kruskal(G):
    """ Implementation of Kruskal to find MST """
    result = []
    total_weight = 0
    for u in G.V:
        make_set(u)
    # sorts the edges by weight in increasing order
    G.E.sort(key=lambda edge: edge[2])
    for u, v, weight in G.E:
        # edge format: (u, v, weight)
        if find_set(u) != find_set(v):
            result.append((u, v, weight))
            total_weight += weight
            union(u, v)
    print(result, "Minimal weight:", total_weight)


def prim(G, s):
    """ Implementation of Prims to find MST """

    for v in G.V:
        v.rank = sys.maxsize
        v.p = None
    s.rank = 0
    Q = MinHeap(G.V)

    while Q.size() > 0:
        u = Q.extract_min()
        for v, weigth in G.adj(u):
            if v in Q and weigth < v.rank:
                # updates the predecessor and rank such that we are getting spanning tree with lowest total edge weight
                v.p = u
                v.rank = weigth
                # update heap since ranks have changed
                Q.build_min_heap()

    # find all the edges that spans the tree
    result = []
    total_weight = 0
    for u in G.V:
        for v, weigth in G.adj(u):
            if v.p == u and (u, v, weigth) not in result:
                result.append((u, v, weigth))
                total_weight += weigth

    print(result, "Minimal weight:", total_weight)


v1 = Vertex(1)
v2 = Vertex(2)
v3 = Vertex(3)
v4 = Vertex(4)
v5 = Vertex(5)
v6 = Vertex(6)
v7 = Vertex(7)

# adding undirected edges by adding directed edges from both u to v and v to u
v1.add_edge(v2, 2)
v2.add_edge(v1, 2)
v1.add_edge(v3, 4)
v3.add_edge(v1, 4)
v2.add_edge(v3, 12)
v3.add_edge(v2, 12)
v1.add_edge(v5, 32)
v5.add_edge(v1, 32)
v5.add_edge(v4, 11)
v4.add_edge(v5, 11)
v4.add_edge(v3, 2)
v3.add_edge(v4, 2)
v6.add_edge(v7, 1)
v7.add_edge(v6, 1)
v5.add_edge(v6, 9)
v6.add_edge(v5, 9)
v5.add_edge(v7, 2)
v7.add_edge(v5, 2)
v7.add_edge(v3, 4)
v3.add_edge(v7, 4)

g = Graph(v1, v2, v3, v4, v5, v6, v7)
g.print()
print("MST by Kruskal:")
kruskal(g)
print("MST by Prim, started in v1 ... v7:")
for v in g.V:
    prim(g, v)
