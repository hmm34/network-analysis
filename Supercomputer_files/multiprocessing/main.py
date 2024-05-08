#!/usr/bin/env python

# library imports
import math
import networkx as nx
import sys
import matplotlib.pyplot as plt
from networkx import Graph
from numpy import Infinity
#from sage.all import *
# from sage.graphs.hyperbolicity import hyperbolicity
# from sage.graphs.graph_input import from_networkx_graph
# from collections import deque
# from sage.graphs.distances_all_pairs import distances_all_pairs
from itertools import combinations
import time
import multiprocessing
from multiprocessing import Manager
import faulthandler
import logging
import cProfile
import pstats
import os
import psutil
from concurrent.futures import ProcessPoolExecutor, as_completed


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

def compute_alpha_i_metric(args_list):
    q, distance_matrix, edge, nodes = args_list
    v, w = edge
    k = 0
    for u in nodes:
        if u == v or u == w or distance_matrix[u][w] != distance_matrix[u][v] + 1:
            continue
        for x in nodes:
            if x == v or x == w or distance_matrix[x][v] != distance_matrix[x][w] + 1:
                continue
            k = max(k, distance_matrix[u][v] + distance_matrix[v][x] - distance_matrix[u][x])
    q.put(edge)
    return k


# def compute_alpha_i_metric_parallel(g, distance_matrix):
#     edges = list(nx.edges(g))
#     nodes = list(nx.nodes(g))
#     m = Manager()
#     q = m.Queue()
#     args_list = [(q, distance_matrix, edge, nodes) for edge in edges]
#     with multiprocessing.Pool() as pool:
#         results = pool.map_async(compute_alpha_i_metric,  args_list)
#         while not results.ready():
#             size = q.qsize()
#             print(size)
#             time.sleep(300)
            
#     return max(results.get())

def compute_alpha_i_metric(args_list):
    q, distance_matrix, edges_chunk, nodes = args_list
    max_k = float('-inf')
    for edge in edges_chunk:
        v, w = edge
        k = 0
        for u in nodes:
            if u == v or u == w or distance_matrix[u][w] != distance_matrix[u][v] + 1:
                continue
            for x in nodes:
                if x == v or x == w or distance_matrix[x][v] != distance_matrix[x][w] + 1:
                    continue
                k = max(k, distance_matrix[u][v] + distance_matrix[v][x] - distance_matrix[u][x])
        if k > max_k:
            max_k = k
            max_edge = edge
        q.put(edge)
    return max_k

def chunkify(lst, n):
    """Split a list into approximately equal-sized chunks."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def my_callback(result):
    print("Callback called with result:", result)


def my_error_callback(error):
    print("Error callback called with error:", error)
    



def compute_alpha_i_metric_parallel(g, distance_matrix):
    start_time = time.time()
    g_edges = list(nx.edges(g))
    g_nodes = list(nx.nodes(g))
    m = Manager()
    edges = list(g_edges)  
    nodes = list(g_nodes)  
    distance_matrix = distance_matrix
    q = m.Queue()
    #args_list = [(q, distance_matrix, edge, nodes) for edge in edges]
    size = 0
    edge_chunks = chunkify(edges, 50)
    
    args_list = [(q, distance_matrix, edge_chunk, nodes) for edge_chunk in edge_chunks]
    print("Setting up pool object and with arguments")
    
    remaining_futures = []
    
    try:
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(compute_alpha_i_metric, args) for args in args_list]
            remaining_futures.extend(futures)
            
            for future in as_completed(remaining_futures):
                my_callback(future.result())
                remaining_futures.remove(future)
                
        # All futures have completed, retrieve the results
        results = [future.result() for future in futures]
        print("All results successfully retrieved.")
        return max(results)  
    except Exception as e:
        if isinstance(e, multiprocessing.BrokenProcessPool):
            print("A worker process abruptly terminated:", e)
            my_error_callback(e)
            # Handle the exception, maybe retry the task or log the issue
        else:
            # Handle other exceptions
            print("An error occurred:", e)
        
    finally:
        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time}")
        print("Exiting...")
        
        
        

# def compute_alpha_i_metric_parallel(g, distance_matrix):
#     start_time = time.time()
#     g_edges = list(nx.edges(g))
#     g_nodes = list(nx.nodes(g))
#     m = Manager()
#     edges = list(g_edges)  # Creating a shared list for edges
#     nodes = list(g_nodes)  # Creating a shared list for nodes
#     distance_matrix = dict(distance_matrix) 
#     q = m.Queue()
#     #args_list = [(q, distance_matrix, edge, nodes) for edge in edges]
#     size = 0
#     edge_chunks = chunkify(edges, 50)
    
#     args_list = [(q, distance_matrix, edge_chunk, nodes) for edge_chunk in edge_chunks]
#     print("Setting up pool object and with arguments")
#     with multiprocessing.Pool() as pool:
#         print("map_async function being called")
#         results = pool.map_async(compute_alpha_i_metric, args_list, callback=my_callback, error_callback=my_error_callback)
#         print("Entering while loop until results are ready")
#         while True:
#             if results.ready():
#                 print("The results are ready")
#                 break
#             if size == len(g_edges):
#                 print("The queue size is equal to the number of edges:")
#                 break
#             size = q.qsize()
#             print(f"The current number of edges in the queue is {size} out of {len(g_edges)}")
#             # List active child processes
#             active_processes = multiprocessing.active_children()
#             print(f"The number of active processes is {len(active_processes)}")
#             for process in active_processes:
#                 print(f'Process {process.pid} is alive: {process.is_alive()}')
#             # Getting % usage of virtual_memory ( 3rd field)
#             print('RAM memory % used:', psutil.virtual_memory()[2])
#             # Getting usage of virtual_memory in GB ( 4th field)
#             print('RAM Used (GB):', psutil.virtual_memory()[3]/1000000000)
#             elapsed_time = time.time() - start_time
#             print(f"Elapsed time: {elapsed_time}")
#             time.sleep(30)
#         print("Exited out of while loop")
#         print("Attempting to get result values")
#         result_values = results.get(timeout=360)
#         print("Result values were successfully retrieved")
#     return max(result_values)




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

    # default values
    print("Computing size ...")
    print("Number of nodes n:", g.number_of_nodes())
    print("Number of edges m:", g.number_of_edges())

    # get largest bi-connected component
    # Check if there are any biconnected components
    biconnected_components = list(nx.biconnected_components(g))
    if not biconnected_components:
        print("No biconnected components found.")
    else:
        # Find the largest biconnected component
        largest_biconnected_comp = max(biconnected_components, key=len)
        g = g.subgraph(largest_biconnected_comp).copy()


    # load to sagemath (capital G) -- sagemath provides different functionality, e.g., hyperbolicity, viewing
    # print("Converting to sagemath graph object ...")
    # G = Graph()
    # from_networkx_graph(G, g)


    # default values
    print("Computing size ...")
    print("Number of nodes n (of LBC):", nx.number_of_nodes(g))
    print("Number of edges m (of LBC):", nx.number_of_edges(g))

    print("Computing distance matrix ...")
    distance_matrix = dict(nx.all_pairs_shortest_path_length(g))

    #print(distance_matrix)
    # for i in distance_matrix:
    #     for j in distance_matrix[i]:
    #         value = float(distance_matrix[i][j])
    #         if math.isinf(value):
    #             distance_matrix[i][j] = 0

    # print("Sorting distance pairs  ...")
    # # # Q is a list of all possible pairs of  vertices in G in non-increasing order
    # Q = [(u, v) for u in G.vertices() for v in G.vertices() if u != v]
    # Q.sort(key=lambda pair: distance_matrix[pair[0]][pair[1]], reverse=True)
    # # print("Distances for each pair:")
    # # for x in Q:
    # #     print(distance_matrix[x[0]][x[1]])
    #
    # start_time = time.time()
    # print(f"Leanness: {compute_leanness(G, Q, distance_matrix)}")
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"Computing Leanness Execution time: {execution_time} seconds")
    print("Computing alpha-i metric (of LBC) ...")
    start_time = time.time()
    print(f"Alpha-i-metric: {compute_alpha_i_metric_parallel(g, distance_matrix)}")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Computing Alpha-i-metric Execution time: {execution_time} seconds")

    ######################################
    # display graph (if specified)
    if (len(sys.argv) >= 2 ) and ((sys.argv[1] == "-s") or (sys.argv[1] == "--show")):
        G.show(method="js", vertex_labels=True, edge_labels=False,  # optional - internet, needs sage.plot
               link_distance=200, gravity=.05, charge=-500,
               edge_partition=[[("11", "12", "2"), ("21", "21", "a")]],
               edge_thickness=4)
        # nx.draw(g)
        plt.draw()
        plt.show()


    ######################################
    # run analysis (subroutines)


    # Create your graph 'g' or load it from your data source

    # Find connected components
    # connected_components = list(nx.connected_components(g))
    # if len(connected_components) > 0:
    #     # Find the largest connected component
    #     largest_component = max(connected_components, key=len)
    #     largest_subgraph = g.subgraph(largest_component)
    #     # Calculate the diameter and of the largest connected component
    #     diameter = nx.diameter(largest_subgraph)
    #     radius = nx.radius(largest_subgraph)
    #     print("Diameter of the largest connected component:", diameter)
    #     print("Radius of the largest connected component:", radius)
    # print("Diameter:", nx.diameter(g))
    # print("Radius:", nx.radius(g))

    ######################################
    # - hyperbolicity
    # print("Computing hyperbolicity (of LBC) ...")
    # start_time = time.time()
    # L, C, U = hyperbolicity(G, algorithm='BCCM')
    # end_time = time.time()
    # print("Hyperbolicity: " + str(L))
    # execution_time = end_time - start_time
    # print(f"Computing Hyperbolicity Execution time: {execution_time} seconds")

    # - cluster diameter
    # - tree.txt length
    # - tree.txt breadth
    # - tree.txt width
    # - cop win number??
    # - various centrality measures (betweenness, closeness, etc....)

    #print("Degree Centrality Data")
    #print(nx.degree_centrality(g))
    print("Analysis complete.")


#load graphs
def main():
    fileName = "data"
    analyze(fileName)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()


