import networkx as nx
from networkx.algorithms import bipartite
import json
import numpy as np
import os
from tqdm import tqdm
import pandas as pd

#Read the data
folder_path = '../DATA1'

file_list = [file for file in os.listdir(folder_path) if file.startswith('pubmed_data_') and file.endswith('_nuovi.json')]


data = []

print('Reading the data...')
for file_name in tqdm(file_list):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path    return len(authors_list)
    
df['Year'] = df['Year'].apply(convert_year)

df['YearInterval'] = (df['Year'] // 5) * 5

# Computing the number of articles and authors per year interval
print('Computing the number of articles and authors per year interval...')
num_articles_per_interval = df['YearInterval'].value_counts().sort_index()

df['NumAuthors'] = df['Authors'].apply(count_authors)
num_authors_per_interval = df.groupby('YearInterval')['NumAuthors'].sum().sort_index()

result_df = pd.DataFrame({
    'YearInterval': num_articles_per_interval.index,
    'NumArticles': num_articles_per_interval.values,
    'NumAuthors': num_authors_per_interval.values
})

# Computing the average number of authors per article
result_df['AvgAuthorsPerArticle'] = result_df['NumAuthors'] / result_df['NumArticles']

os.makedirs('results', exist_ok=True)

# Saving the results in a JSON file
print('Saving the results...')
result_df.to_json('./results/num_paper_authors.json', orient='records', lines=True, index = True)
print('Results saved!')

print('Creating the bipartite graph...')

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

print('Done!')

print('Projecting the graph on the authors nodes (collaboration network)... ')

article_nodes = {n for n, d in tqdm(B.nodes(data=True)) if d["bipartite"] == 0}
authors_nodes = set(B) - article_nodes

C = bipartite.weighted_projected_graph(B, authors_nodes) #weighted projection

print('Done!')

nx.write_edgelist(C, "./edge_list.txt")

#communities = nx.community.louvain_communities(C)
#communities = sorted(communities, key=len, reverse=True)

#output_file_path = 'communities.txt'
#with open(output_file_path, 'w') as file:
#    file.write(str(communities))

#print(f"communities saved to {output_file_path}")








