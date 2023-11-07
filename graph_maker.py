
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import json

with open('pubmed_data.json', 'r') as file:
    data = [json.loads(line) for line in file]
print(type(data))

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for item in data:
    source_id = item["Id"]
    cited_articles = item["Cited_Articles"]

    # Add nodes (if not already added)
    G.add_node(source_id)

    for target_id in cited_articles:
        # Add edges from source_id to the cited articles
        G.add_edge(source_id, target_id)


# Number of nodes and edges
num_nodes = len(G.nodes)
num_edges = len(G.edges)
print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")

# Degree distribution
in_degrees = dict(G.in_degree())
out_degrees = dict(G.out_degree())

# Connected components
weakly_connected_components = list(nx.weakly_connected_components(G))


# Centrality measures (e.g., in-degree and out-degree centrality)
in_degree_centrality = nx.in_degree_centrality(G)
out_degree_centrality = nx.out_degree_centrality(G)

# Network density
density = nx.density(G)

# Clustering coefficients
clustering_coefficients = nx.clustering(G)

# Transitivity
transitivity = nx.transitivity(G)

# Reciprocity
reciprocity = nx.reciprocity(G)


# Central node identification (e.g., nodes with high in-degree centrality)
top_nodes_by_in_degree = sorted(in_degree_centrality, key=in_degree_centrality.get, reverse=True)[:5]

# Assortativity
assortativity = nx.degree_assortativity_coefficient(G)



# Degree distribution
in_degrees = dict(G.in_degree())
out_degrees = dict(G.out_degree())

# Plot in-degree distribution
plt.figure(figsize=(8, 6))
plt.hist(list(in_degrees.values()), bins=20, alpha=0.5, color='b')
plt.title('In-Degree Distribution')
plt.xlabel('In-Degree')
plt.ylabel('Count')
plt.show()

# Plot out-degree distribution
plt.figure(figsize=(8, 6))
plt.hist(list(out_degrees.values()), bins=20, alpha=0.5, color='r')
plt.title('Out-Degree Distribution')
plt.xlabel('Out-Degree')
plt.ylabel('Count')
plt.show()

# Connected components
strongly_connected_components = list(nx.strongly_connected_components(G))
weakly_connected_components = list(nx.weakly_connected_components(G))

# Plot the number of strongly connected components
plt.figure(figsize=(8, 6))
plt.bar(['Strongly Connected'], [len(strongly_connected_components)], color='g')
plt.title('Number of Strongly Connected Components')
plt.ylabel('Count')
plt.show()

# Plot the number of weakly connected components
plt.figure(figsize=(8, 6))
plt.bar(['Weakly Connected'], [len(weakly_connected_components)], color='y')
plt.title('Number of Weakly Connected Components')
plt.ylabel('Count')
plt.show()