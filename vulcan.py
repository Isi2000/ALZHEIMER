import networkx as nx
from networkx.algorithms import bipartite
import json
import numpy as np
import os
from tqdm import tqdm
import pandas as pd

#Read the data
folder_path = 'DATA1'

file_list = [file for file in os.listdir(folder_path) if file.startswith('pubmed_data_') and file.endswith('_nuovi.json')]

data = []

print('Reading the data...')
for file_name in tqdm(file_list):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        file_data = [json.loads(line) for line in file]
        data.extend(file_data)
print('Data loaded successfully!')

df = pd.DataFrame(data)

print('Preprocessing the data...')
# Adding the year interval column
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
"""
print('Saving the results...')
result_df.to_json('./results/num_paper_authors.json', orient='records', lines=True, index = True)
print('Results saved!')

print('Creating the bipartite graph...')
"""
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

nx.write_edgelist(C, './edges.txt')

"""
print('Done!')

print('Computing the degree sequence...')
degree_sequence = sorted((d for n, d in C.degree()), reverse=True)

print('Saving the results...')
np.save('./results/degree_sequence.npy', degree_sequence)
print('Degree sequence saved!')

number_of_authors = C.number_of_nodes()
number_of_collaborations = C.number_of_edges()
density = nx.density(C)
number_of_connected_components = nx.number_connected_components(C)
connected_components = list(nx.connected_components(C))
filtered_connected_components = \
    [comp for comp in tqdm(connected_components) if len(comp) > 1] 


print('Characteristics of the collaborative network: ')
print('Number of nodes (authors): ', number_of_authors)
print('Number of edges: ', number_of_collaborations)
print('Density: ', density)
print('Number of connected components: ', number_of_connected_components)
print('Number of connected components with more than one node: ', len(filtered_connected_components))

largest_cc = max(tqdm(filtered_connected_components, desc="Largest connected component", 
                      unit="component"), key=len)


#Building a network of the largest connected component

largest_cc = max(filtered_connected_components, key=len)

cc = C.subgraph(largest_cc)

number_of_authors_cc = cc.number_of_nodes()
number_of_collaborations_cc = cc.number_of_edges()
clustering_coefficient = nx.average_clustering(cc, weight = 'weight')
clustering_coefficient_unweighted = nx.average_clustering(cc)
average_shortest_path = nx.average_shortest_path_length(cc, \
                                                        weight= lambda u, v, d: 1 / d['weight'] )
average_shortest_path_unweighted = nx.average_shortest_path_length(cc)

print('Characteristics of the largest connected component:')
print('Number of nodes (authors): ', number_of_authors_cc)
print('Number of edges: ', number_of_collaborations_cc)
print('Clustering coefficient: ', clustering_coefficient)
print('Clustering coefficient (unweighted): ', clustering_coefficient_unweighted)
print('Average shortest path: ', average_shortest_path)
print('Average shortest path (unweighted): ', average_shortest_path_unweighted)

#Identification of influential nodes in the collaboration network's largest connected component

# 1. Degree centrality

print('Ranking of authors by degree centrality:-------------------------------------------------- ')
degree_centrality = nx.degree_centrality(cc)
degree_centrality_sorted = sorted(degree_centrality.items(), key = lambda x: x[1], reverse=True)
for influential_author in degree_centrality_sorted[:10]:
    print('Author: ', influential_author[0], 'Degree centrality: ', influential_author[1])

# 2. Betweenness centrality

print('Ranking of authors by betweenness centrality:--------------------------------------------- ')
betweenness_centrality = nx.betweenness_centrality(cc, weight= lambda u, v, d: 1 / d['weight'])
betweenness_centrality_sorted = sorted(betweenness_centrality.items(), key = lambda x: x[1], reverse=True)
for influential_author in betweenness_centrality_sorted[:10]:
    print('Author: ', influential_author[0], 'Betweenness centrality: ', influential_author[1])

# 3. Closeness centrality
print('Ranking of authors by closeness centrality:------------------------------------------------')
closeness_centrality = nx.closeness_centrality(cc, distance= lambda u, v, d: 1 / d['weight'])
closeness_centrality_sorted = sorted(closeness_centrality.items(), key = lambda x: x[1], reverse=True)
for influential_author in closeness_centrality_sorted[:10]:
    print('Author: ', influential_author[0], 'Closeness centrality: ', influential_author[1])

# 4. Eigenvector centrality
print('Ranking of authors by eigenvector centrality:-----------------------------------------------')
eigenvector_centrality = nx.eigenvector_centrality(cc, weight= 'weight')
eigenvector_centrality_sorted = sorted(eigenvector_centrality.items(), key = lambda x: x[1], reverse=True)
for influential_author in eigenvector_centrality_sorted[:10]:
    print('Author: ', influential_author[0], 'Eigenvector centrality: ', influential_author[1])

# 5. PageRank
print('Ranking of authors by PageRank:-------------------------------------------------------------')
pagerank = nx.pagerank(cc, weight= 'weight')
pagerank_sorted = sorted(pagerank.items(), key = lambda x: x[1], reverse=True)
for influential_author in pagerank_sorted[:10]:
    print('Author: ', influential_author[0], 'PageRank: ', influential_author[1])

# Borda count

def Borda_score(descending_list_of_tuples):
    Borda_score = {}
    for i, author in enumerate(descending_list_of_tuples):
        Borda_score[author[0]] = len(descending_list_of_tuples) - 1 - i
    return Borda_score

Borda_score_degree = Borda_score(degree_centrality_sorted)
Borda_score_betweenness = Borda_score(betweenness_centrality_sorted)
Borda_score_closeness = Borda_score(closeness_centrality_sorted)
Borda_score_eigenvector = Borda_score(eigenvector_centrality_sorted)
Borda_score_page_rank = Borda_score(pagerank_sorted)

Borda_score_list = [Borda_score_degree, Borda_score_betweenness, \
                    Borda_score_closeness, Borda_score_eigenvector, Borda_score_page_rank]

Borda_score_sum = {}

for author in Borda_score_degree.keys():
    Borda_score_sum[author] = sum([Borda_score[author] for Borda_score in Borda_score_list])

Borda_score_sum_sorted = sorted(Borda_score_sum.items(), key = lambda x: x[1], reverse=True)

print('Ranking of authors by Borda score:----------------------------------------------------------')
for influential_author in Borda_score_sum_sorted[:10]:
    print('Author: ', influential_author[0], 'Borda score: ', influential_author[1])
"""
