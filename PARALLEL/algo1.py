import networkx as nx
from connected_component.py import cc

print("calculate clustering_coefficient")
clustering_coefficient = nx.average_clustering(cc, weight = 'weight')
print(clustering_coefficient)
