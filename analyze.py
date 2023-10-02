# libriary imports
import networkx as nx
#from pyvis.network import Network
import matplotlib.pyplot as plt
from sage.graphs.hyperbolicity import hyperbolicity
from sage.graphs.graph_input import from_networkx_graph
from sage.all import *


# Given a sagemath graph, compute the interval thinness (leanness) using AO Mohammed et al approach
# input: precomputed distance matrix D
#        sagemath graph G
#        list Q of all vertex pairs {x,y} of G sorted in nonn-increasing order with respect to d(x,y)
# output: lambda, the leanness of G
def compute_leanness(G, Q):
    leanness = 0
    for x, y in Q:
        if distance_matrix[x][y] <= leanness:
            return leanness
        
        # Create empty sets S[i]
        S = [set() for _ in range(distance_matrix[x][y] + 1)]
        
        for w in G:
            if distance_matrix[x][y] == distance_matrix[x][w] + distance_matrix[y][w]:
                # Insert w into S[d(x, w)]
                S[distance_matrix[x][w]].add(w)
                # Remove pairs {x, w}, {w, y} from Q
                if (x, w) in Q:
                    Q.remove((x, w))
                if (w, y) in Q:
                    Q.remove((w, y))
        
        start = leanness // 2
        end = distance_matrix[x][y] - leanness // 2
        
        for i in range(start, end + 1):
            for u, v in S[i]:
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

    distance_matrix = G.shortest_path_matrix()
    Q = [(u, v) for u in G.vertices() for v in G.vertices() if u != v]
    print(f"compute_leanness(G, Q)")

    ######################################
    # display graph
    G.show(method="js", vertex_labels=True, edge_labels=False,         # optional - internet, needs sage.plot
       link_distance=200, gravity=.05, charge=-500,
       edge_partition=[[("11", "12", "2"), ("21", "21", "a")]],
       edge_thickness=4)
    #nx.draw(g)
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
    L,C,U = hyperbolicity(G, algorithm='BCCM');
    print("Hyperbolicity: " + str(L))
    

    # - cluster diameter
    # - tree length
    # - tree breadth
    # - tree width
    # - cop win number??
    # - various centrality measures (betweenness, closeness, etc....)

    print("Degree Centrality Data")
    print(nx.degree_centrality(g))
    print("ok")

# load graphs
fileName = "data/small.txt"
analyze(fileName)