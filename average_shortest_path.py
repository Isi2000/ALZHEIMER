from connected_component import cc
import networkx as nx
from igraph import *
from itertools import combinations

nodes = cc.nodes()
combinations_list = list(combinations(nodes, 2))
paths = []
print("average_shortest_path computation")
for i in tqdm(combinations_list):
    paths.append(cc.get_shortest_path(i[0], i[1]))
    


# Save clustering coefficient to a file
output_file_path = 'average_shortest_path.txt'
with open(output_file_path, 'w') as file:
    file.write(str(average_shortest_path))

print(f"Average shortest path saved to {output_file_path}")
