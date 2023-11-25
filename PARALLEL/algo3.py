from connected_component import cc
import networkx
print("average_shortest_path computation")
average_shortest_path = nx.average_shortest_path_length(cc, weight= lambda u, v, d: 1 / d['weight'] )


# Save clustering coefficient to a file
output_file_path = 'average_shortest_path.txt'
with open(output_file_path, 'w') as file:
    file.write(str(average_shortest_path))

print(f"Average shortest path saved to {output_file_path}")
