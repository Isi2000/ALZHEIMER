import networkx as nx
from connected_component.py import cc

print("calculate clustering_coefficient")
clustering_coefficient = nx.average_clustering(cc, weight = 'weight')

print(clustering_coefficient)

# Save clustering coefficient to a file
output_file_path = 'clustering_coefficient.txt'
with open(output_file_path, 'w') as file:
    file.write(str(clustering_coefficient))

print(f"Clustering coefficient saved to {output_file_path}")
