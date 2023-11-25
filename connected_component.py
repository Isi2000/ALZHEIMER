import networkx as nx
from networkx.algorithms import bipartite
import json
import numpy as np
import os
from tqdm import tqdm
import pandas as pd

folder_path = '../DATA1'

file_list = [file for file in os.listdir(folder_path) if file.startswith('pubmed_data_') and file.endswith('_nuovi.json')]

data = []
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        file_data = [json.loads(line) for line in file]
        data.extend(file_data)
df = pd.DataFrame(data)
df['Year'] = df['Dates'].str.split('-', expand=True)[0]

def convert_year(year):
    try:
        return int(year)
    except ValueError:
        return pd.NaT

def count_authors(authors_list):
    return len(authors_list)
    
df['Year'] = df['Year'].apply(convert_year)
df['YearInterval'] = (df['Year'] // 5) * 5

num_articles_per_interval = df['YearInterval'].value_counts().sort_index()

df['NumAuthors'] = df['Authors'].apply(count_authors)
num_authors_per_interval = df.groupby('YearInterval')['NumAuthors'].sum().sort_index()

result_df = pd.DataFrame({
    'YearInterval': num_articles_per_interval.index,
    'NumArticles': num_articles_per_interval.values,
    'NumAuthors': num_authors_per_interval.values
})

result_df['AvgAuthorsPerArticle'] = result_df['NumAuthors'] / result_df['NumArticles']

#os.makedirs('results', exist_ok=True)
#result_df.to_json('./results/num_paper_authors.json', orient='records', lines=True, index = True)

B = nx.Graph()

# Add nodes and edges from the DataFrame
for _, row in df.iterrows():
    node_id = row['Id']
    authors = row['Authors']
    B.add_node(node_id, bipartite=0)  # bipartite=0 for 'Id' nodes
    if len(authors) > 0:
        for author in authors:
            B.add_node(author, bipartite=1)  # bipartite=1 for 'Authors' nodes
            B.add_edge(node_id, author)


article_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}
authors_nodes = set(B) - article_nodes

C = bipartite.weighted_projected_graph(B, authors_nodes) #weighted projection
number_of_authors = C.number_of_nodes()
number_of_collaborations = C.number_of_edges()
density = nx.density(C)
number_of_connected_components = nx.number_connected_components(C)
connected_components = list(nx.connected_components(C))
filtered_connected_components = [comp for comp in connected_components if len(comp) > 1] 

"""
print('Characteristics of the collaborative network: ')
print('Number of nodes (authors): ', number_of_authors)
print('Number of edges: ', number_of_collaborations)
print('Density: ', density)
print('Number of connected components: ', number_of_connected_components)
print('Number of connected components with more than one node: ', len(filtered_connected_components))
"""
largest_cc = max(filtered_connected_components, key=len)

cc = C.subgraph(largest_cc)

