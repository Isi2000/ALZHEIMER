
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import json

with open('pubmed_data.json', 'r') as file:
    data = [json.loads(line) for line in file]
print(type(data))

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for item in data:
    source_id = item["Id"]
    cited_articles = item["Cited_Articles"]

    # Add nodes (if not already added)
    G.add_node(source_id)

    for target_id in cited_articles:
        # Add edges from source_id to the cited articles
        G.add_edge(source_id, target_id)

# Now you can perform various operations on the graph 'G'
# For example, you can get basic information about the graph:
print(f"Number of nodes: {len(G.nodes)}")
print(f"Number of edges: {len(G.edges)}")

pos = nx.spring_layout(G, seed=42)  # You can choose a different layout if needed

plt.figure(figsize=(10, 10))
nx.draw(G, pos, with_labels=False, node_size=1, node_color='blue', font_size=6, width=0.1)
plt.title("Citation Graph")
plt.axis('off')
plt.show()