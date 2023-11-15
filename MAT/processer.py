import os
import json
from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        result = {}  # Create an empty dictionary to store the results
        for item in data:
            if 'Id' in item and 'cited_arts' in item:
                cleaned_cited_arts = [art for art in item['cited_arts'] if art is not None and art != []]
                result[item['Id']] = cleaned_cited_arts
                
        return result  # Return the dictionary

def process_directory(directory_path):
    results = {}  # Create an empty dictionary to accumulate results
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                result = process_json_file(file_path)
                results.update(result)  # Update the results dictionary
    return results  # Return the final dictionary

# Replace 'path_to_directory' with the actual path of your directory containing the JSON files.

path_to_directory = './DATA'
results = process_directory(path_to_directory)
G = nx.Graph()

# Add nodes and edges based on the 'results' dictionary
for node, cited_nodes in tqdm(results.items()):
    G.add_node(node)
    if cited_nodes != None:  # Check if cited_nodes is not empty
        for cited_node in cited_nodes:
            G.add_edge(node, cited_node)

print(G)
# Visualize the graph
pos = nx.spring_layout(G)  # Define a layout for the nodes
nx.draw(G, pos, with_labels=False, node_color='darkgrey', node_size=1, width = 0.05, font_size=10, font_color='black')
plt.title("Networkx Graph")
plt.show()


