# library imports
import networkx as nx
# from pyvis.network import Network
import matplotlib.pyplot as plt
from networkx import Graph
from sage.graphs.hyperbolicity import hyperbolicity
from sage.graphs.graph_input import from_networkx_graph
from sage.all import *
from collections import deque
from sage.graphs.distances_all_pairs import distances_all_pairs
from itertools import combinations


# Given a sagemath graph, compute the interval thinness (leanness) using AO Mohammed et al approach
# input: precomputed distance matrix D
#        sagemath graph G
#        list Q of all vertex pairs {x,y} of G sorted in nonn-increasing order with respect to d(x,y)
# output: lambda, the leanness of G
def compute_leanness(G, Q, distance_matrix):
    leanness = 0
    # Iterate through all vertex pairs.
    for x, y in Q:
        if distance_matrix[x][y] <= leanness:
            return leanness

        # Create empty dictionary S where keys are distances and values are sets of pairs (u, v)
        S = {i: set() for i in range(distance_matrix[x][y] + 1)}

        for w in G:
            if distance_matrix[x][y] == distance_matrix[x][w] + distance_matrix[y][w]:
                # Insert pair w  into S[d(x, w)]
                S[distance_matrix[x][w]].add((w))
                # Remove pairs (x, w) and (w, y) from Q
                if (x, w) in Q:
                    Q.remove((x, w))
                if (w, y) in Q:
                    Q.remove((w, y))

        start = leanness // 2
        end = distance_matrix[x][y] - leanness // 2

        for i in range(start, end + 1):
            if len(S[i]) > 1:
                # Iterate through all combinations of pairs in S[i]
                for u, v in combinations(S[i], 2):
                    if leanness < distance_matrix[u][v]:
                        leanness = distance_matrix[u][v]
    return leanness


def compute_alpha_i_metric(G):
    return 0


def compute_pseudoconvexity(G):
    return 0


def compute_helly_gap(G):
    return 0


# aka insize
def compute_triangle_thinness(G):
    return 0


def compute_slimness(G):
    return 0


def analyze(fileName):
    ######################################
    print("Loading graph" + fileName)

    # load through networkx (lowercase g) -- networkx provides some functionality
    filehandle = open(fileName, "rb")
    g = nx.read_edgelist(filehandle, nodetype=int)
    filehandle.close()

    # load to sagemath (capital G) -- sagemath provides different functionality, e.g., hyperbolicity, viewing
    G = Graph()
    from_networkx_graph(G, g)
    distance_matrix = distances_all_pairs(G)
    print(distance_matrix)

    # Q is a list of all possible pairs of  vertices in G in non-increasing order
    Q = [(u, v) for u in G.vertices() for v in G.vertices() if u != v]
    Q.sort(key=lambda pair: distance_matrix[pair[0]][pair[1]], reverse=True)
    print("Distances for each pair:")
    for x in Q:
        print(distance_matrix[x[0]][x[1]])

    print(f"Leanness: {compute_leanness(G, Q, distance_matrix)}")

    ######################################
    # display graph
    G.show(method="js", vertex_labels=True, edge_labels=False,  # optional - internet, needs sage.plot
           link_distance=200, gravity=.05, charge=-500,
           edge_partition=[[("11", "12", "2"), ("21", "21", "a")]],
           edge_thickness=4)
    # nx.draw(g)
    plt.draw()
    plt.show()

    ######################################
    # run analysis (subroutines)
    print("Number of nodes n:", g.number_of_nodes())
    print("Number of edges m:", g.number_of_edges())
    print("Diameter:", nx.diameter(g))
    print("Radius:", nx.radius(g))

    ######################################
    # - hyperbolicity
    L, C, U = hyperbolicity(G, algorithm='BCCM');
    print("Hyperbolicity: " + str(L))

    # - cluster diameter
    # - tree.txt length
    # - tree.txt breadth
    # - tree.txt width
    # - cop win number??
    # - various centrality measures (betweenness, closeness, etc....)

    print("Degree Centrality Data")
    print(nx.degree_centrality(g))
    print("ok")


# load graphs
fileName = "data/graphA.txt"
analyze(fileName)
