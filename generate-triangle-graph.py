import networkx as nx

# Define the dimensions of the king grid
rows = 8
cols = 5

# Generate a 2D king grid graph
G = nx.generators.grid_2d_graph(rows, cols)

# Add diagonal edges to the graph
for node in G.nodes:
    row, col = node
    neighbors = [(row + i, col + j) for i in [-1] for j in [1] if (i, j) != (0, 0)]
    for neighbor in neighbors:
        if neighbor in G.nodes and  (node, neighbor):
            G.add_edge(node, neighbor)

# Convert nodes to integers
G = nx.convert_node_labels_to_integers(G)


# Specify the file path to save the graph
file_path = "data/triangle-graphs/triangle-graph-8-5"

# Save the edgelist to a file including edge data
nx.write_edgelist(G, file_path)

# Read the edgelist from the file
loaded_graph = nx.read_edgelist(file_path, nodetype=int)


print(f"Graph has been saved and loaded successfully.")