
import networkx as nx
from connected_component import cc
from multiprocessing import Pool
from tqdm import tqdm
import time

# Get the first 10,000 nodes from the graph
nodes_to_process = list(cc.nodes())[:10000]

def compute_clustering_coefficient(node):
    return nx.clustering(cc, node, weight='weight')

print("Calculating clustering_coefficient")

# Record start time
start_time = time.time()

# Use tqdm for progress tracking
with Pool() as pool, tqdm(total=len(nodes_to_process)) as pbar:
    clustering_coefficients = list(tqdm(pool.imap_unordered(compute_clustering_coefficient, nodes_to_process)))
    pbar.update()

# Calculate the average clustering coefficient
average_clustering_coefficient = sum(clustering_coefficients) / len(clustering_coefficients)

# Record end time
end_time = time.time()

print(f"Average Clustering Coefficient: {average_clustering_coefficient}")
print(f"Time taken: {end_time - start_time} seconds")

# Save clustering coefficient to a file
output_file_path = 'clustering_coefficient.txt'
with open(output_file_path, 'w') as file:
    file.write(str(average_clustering_coefficient))

print(f"Clustering coefficient saved to {output_file_path}")
