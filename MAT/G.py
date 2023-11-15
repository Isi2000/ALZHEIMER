import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import time

# access data and read the dicts line by line
with open('pubmed_data_1.json', 'r') as file:
    data = [json.loads(line) for line in file]
print(type(data))

G = nx.Graph()


bip_0 = [] #authors
bip_1 = [] #ids

for item in data:
    source = item["Id"]
    G.add_node(source, bipartite = 1)
    bip_0.append(source)
    
    for author in item["Authors"]:
        target = author
        G.add_node(target, bipartite = 0)
        bip_1.append(target)
        #we also add edges
        G.add_edge(source, target)



p_G_a = nx.projected_graph(G, bip_1)
print(p_G_a)
p = nx.circular_layout(p_G_a)


nx.draw(p_G_a, p, node_size = 2, width = 0.001)
plt.scatter([],[], color='blue', label='Articles id', s=100)
plt.scatter([],[], color='red', label='Authors', s=100)
plt.legend(scatterpoints=1, frameon=False, labelspacing=1, loc='upper right')
plt.show()









"""        
#layout of the graph
pos = nx.bipartite_layout(G, bip_0)
author_nodes_with_c = [node for node, degree in G.degree() if degree > 5 and G.nodes[node]['bipartite'] == 1]
edge_color = ['Red' if target in author_nodes_with_c else 'white' for source, target in G.edges]
node_color = ['blue' if G.nodes[node]['bipartite'] == 0 else 'red' for node in G.nodes]
nx.draw(G, pos, with_labels=False, node_size=2, node_color=node_color, edge_color=edge_color, width=0.04)
plt.scatter([],[], color='blue', label='Articles id', s=100)
plt.scatter([],[], color='red', label='Authors', s=100)
plt.legend(scatterpoints=1, frameon=False, labelspacing=1, loc='upper right')
plt.show()
"""
