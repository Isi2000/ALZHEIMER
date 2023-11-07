
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import json

# Read the JSON data line by line
with open('pubmed_data.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Create a DataFrame
df = pd.DataFrame(data)

# Now you can proceed with the rest of your code
print(df.columns)


# Create a NetworkX graph from the DataFrame
G = nx.from_pandas_edgelist(df, 'Id', 'Cited_Articles')

# Now you can perform various operations on the graph 'G'
# For example, you can get basic information about the graph:
print(f"Number of nodes: {len(G.nodes)}")
print(f"Number of edges: {len(G.edges)}")


