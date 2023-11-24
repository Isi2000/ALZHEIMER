from connected_component import cc
import networkx as nx

print("clustering coefficient unweighted")
clustering_coefficient_unweighted = nx.average_clustering(cc)
print(clustering_coefficient_unweighted)
