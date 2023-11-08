import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
#from collections import Counter
#from itertools import combinations

# Read data

with open('pubmed_data.json', 'r') as file:
    data = [json.loads(line) for line in file]


#print(type(data), data[0])
#print(len(data))

#data is a list of dictionaries

G = nx.Graph()

# Add nodes and edges with the attribute 'bipartite'

for article in data:
    G.add_node(article["Id"], bipartite=0)
    for author in article["Authors"]:
        G.add_node(author, bipartite=1)
        G.add_edge(article["Id"], author)

print(len(data))
print('Number of nodes: ', G.number_of_nodes())
print('Is connected: ', nx.is_connected(G))
print('Is bipartite: ', bipartite.is_bipartite(G))

top_nodes = {n for n, d in G.nodes(data=True) if d["bipartite"] == 0}
bottom_nodes = set(G) - top_nodes

A = bipartite.weighted_projected_graph(G, nodes = bottom_nodes, ratio=False)
print('Number of nodes in the projected graph: ', A.number_of_nodes())
print('Number of edges in the projected graph: ', A.number_of_edges())

print('Connected graph (Authors): ', nx.is_connected(A))

print('Number of connected components (Authors): ', nx.number_connected_components(A))

connected_components = list(nx.connected_components(A))
#filtered_components = [comp for comp in connected_components if len(comp) > 1]

main_component = max(connected_components, key=len)
print('Number of nodes in the main component: ', len(main_component))
print('Number of edges in the main component: ', A.subgraph(main_component).number_of_edges())

# Degree analysis

degrees_sequence = sorted((degree for node, degree in A.degree()), reverse=True)
dmax = max(degrees_sequence)
print('Maximum degree: ', dmax)

os.makedirs('images', exist_ok=True)

#Degree rank plot
plt.figure(figsize=(8, 6))
plt.loglog(degrees_sequence, 'b-', marker='o')
plt.title('Degree rank plot')
plt.ylabel('degree')
plt.xlabel('rank')
plt.savefig('images/degree_rank_plot.png')

#Degree histogram
plt.figure(figsize=(8, 6))
degrees = [G.degree(n) for n in A.nodes()]
plt.hist(degrees, bins=1000, alpha=0.5, color='b')
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Count')
plt.savefig('images/degree_distribution.png')

communities = nx.community.louvain_communities(A)
communities = sorted(communities, key=len, reverse=True)
print('Number of communities: ', len(communities))
print('Number of nodes in the largest community: ', len(communities[0]))
final_partition_modularity = nx.community.modularity(A, communities)
print('Final partition modularity: ', final_partition_modularity)

"""
G = nx.Graph()

def get_combinations_of_2(arr):
    all_combinations = list(combinations(arr, 2))
    return all_combinations

# Add nodes and edges
edges_lists = []

for article in data:
    edges_lists.append(get_combinations_of_2(article["Authors"]))

for edge_list in edges_lists:
    G.add_edges_from(edge_list)

print('Number of nodes: ', G.number_of_nodes())
print('Number of edges: ', G.number_of_edges())

print('Connected graph: ', nx.is_connected(G))

print(nx.number_connected_components(G))

connected_components = list(nx.connected_components(G))
filtered_components = [comp for comp in connected_components if len(comp) > 1]

main_component = max(filtered_components, key=len)
print('Number of nodes in the main component: ', len(main_component))
print('Number of edges in the main component: ', G.subgraph(main_component).number_of_edges())

# Degree analysis

degrees_sequence = sorted((degree for node, degree in G.degree()), reverse=True)
dmax = max(degrees_sequence)
print('Maximum degree: ', dmax)

#Degree rank plot
plt.figure(figsize=(8, 6))
plt.loglog(degrees_sequence, 'b-', marker='o')
plt.title('Degree rank plot')
plt.ylabel('degree')
plt.xlabel('rank')
plt.show()

#Degree histogram
plt.figure(figsize=(8, 6))
degrees = [G.degree(n) for n in G.nodes()]
plt.hist(degrees, bins=1000, alpha=0.5, color='b')
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Count')
plt.show()
"""

"""
degrees = [G.degree(n) for n in G.nodes()]
plt.hist(degrees, bins=20, alpha=0.5, color='b')
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Count')
plt.show()

flattened_list = [frozenset(t) for sublist in edges_lists for t in sublist]
tuple_frequency = Counter(flattened_list)
for tup, freq in tuple_frequency.items():
    if freq > 4:
        print(tuple(tup), freq)


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
"""