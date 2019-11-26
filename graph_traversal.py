""" BFS, DFS and Topological sort """

import sys
from queue import Queue, LifoQueue
from graph_structs import Vertex, Graph


def BFS(G, s):
    """ Implementation of Breadth First Search """
    for u in G.V:
        u.color = "white"
        u.d = sys.maxsize
        u.p = None
    s.color = "gray"
    s.d = 0
    Q = Queue()
    Q.put(s)
    while not Q.empty():
        u = Q.get()
        print(f"searching {u}")
        for v, weight in G.adj(u):
            if v.color == "white":
                v.color = "grey"
                v.d = u.d + 1
                v.p = u
                Q.put(v)
                print(f"found {v}, distance from {s} is {v.d}")
        print(f"finished {u}")


global time


def DFS(G, debug=True):
    """ Implements Depth First Search """
    global time
    for u in G.V:
        u.color = "white"
        u.p = None
    time = 0
    for u in G.V:
        if u.color == "white":
            if debug:
                print(f"found {u} at time {time}")
            DFS_vist(G, u, debug=debug)


def DFS_vist(G, u, debug=True):
    """ Sub-routine in DFS """
    if debug:
        print(f"searching {u}")
    global time
    time += 1
    u.d = time
    u.color = "grey"
    for v, weigth in G.adj(u):
        if v.color == "white":
            if debug:
                print(f"found {v} at time {time}")
            v.p = u
            DFS_vist(G, v, debug=debug)
    u.color = "black"
    time += 1
    u.f = time
    if debug:
        print(f"finished {u} at time {time}")


def topological_sort(G):
    """ Implementation of Toplogical Sort using DFS """
    DFS(G, debug=False)
    result = []
    for u in G.V:
        result.append(u)
    result.sort(key=lambda x: x.f, reverse=True)
    return result


def test():
    v1 = Vertex(1)
    v2 = Vertex(2)
    v3 = Vertex(3)
    v4 = Vertex(4)
    v5 = Vertex(5)
    v6 = Vertex(6)
    v7 = Vertex(7)

    v1.add_edge(v2)
    v1.add_edge(v3)
    v2.add_edge(v3)
    v1.add_edge(v5)
    v5.add_edge(v4)
    v4.add_edge(v3)
    v6.add_edge(v7)
    g = Graph(v1, v2, v3, v4, v5, v6, v7)
    g.print()
    print(g.E)
    print("BFS:")
    BFS(g, v1)
    print("\nDFS:")
    DFS(g)
    print("\nTopological sort:")
    topological_sort(g)

# test()
