from connected_component import cc
import networkx as nx

print("clustering coefficient unweighted")
clustering_coefficient_unweighted = nx.average_clustering(cc)
print(clustering_coefficient_unweighted)
# Save clustering coefficient to a file
output_file_path = 'clustering_coefficient_unweighted.txt'
with open(output_file_path, 'w') as file:
    file.write(str(clustering_coefficient_unweighted))

print(f"Clustering coefficient saved to {output_file_path}")
