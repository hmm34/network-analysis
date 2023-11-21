import networkx as nx

# Define the dimensions of the grid
rows = 7
cols = 5

# Generate a 2D grid graph
G = nx.grid_2d_graph(rows, cols)

# Convert nodes to integers
G = nx.convert_node_labels_to_integers(G)

# Specify the file path to save the graph
file_path = "data/grid graphs/grid_graph_2-5"  # Changed file path for clarity

# Save the edgelist to a file including edge data
nx.write_edgelist(G, file_path)

# Read the edgelist from the file
loaded_graph = nx.read_edgelist(file_path, nodetype=int)

# Print the loaded graph
print("Loaded Graph Nodes:", loaded_graph.nodes())
print("Loaded Graph Edges:", loaded_graph.edges())

print(f"Graph has been saved and loaded successfully.")
