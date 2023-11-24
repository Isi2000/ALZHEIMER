from connected_component import cc
import networkx
print("average_shortest_path computation")
average_shortest_path = nx.average_shortest_path_length(cc, weight= lambda u, v, d: 1 / d['weight'] )

print(average_shortest_path)
