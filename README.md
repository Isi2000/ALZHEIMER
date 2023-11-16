# Social network analysis of Alzheimer research collaboration network

## Abstract

## Introduction

Alzheimer's disease is a progressive and irreversible neurological disorder that affects the brain, leading to cognitive decline and memory loss. It is the most common cause of dementia, which is an umbrella term for several diseases resulting in a decline in mental ability severe enough to interfere with daily life.

Age is the most significant known risk factor for dementia, however it is essential to note that dementia is not a normal part of aging. Alzheimer's more frequently affects adults over 65 years old, with a higher prevalence in women.

According to the World Health Organization (WHO) data, Alzheimer's affects more than 55 million people worldwide. Even more striking is the data suggesting that the numbers are growing on a daily basis, with a projection reaching 78 million by 2030 (citazione).

Up to now, there are no therapies that can halt or reverse the illness, and all available therapies aim to mitigate the symptoms.

Alzheimer's disease poses a significant and growing public health challenge, emphasizing the critical need for ongoing research to better understand its underlying mechanisms, develop effective treatments, and ultimately find a cure. 

Graph theory, and particularly social network analysis, are crucial tools for evaluating the quality and effectiveness of research in this field. In our project, we utilized tools developed in graph theory to systematically analyze the structure of the Alzheimer's disease collaboration network. Furthermore we used the
Louvain algorithm for performing a community detection.

(Qui io ripercorrerei velocemente quello che abbiamo fatto e scriverei come abbiamo strutturato il resto della relazione).



## Materials and Methods 

### Dataset
### Construction of the authors collaboration network

We start by constructing the author-paper bipartite network $ G = (U, V, E)$, where the disjoint and independent sets of nodes $U$ and $V$ represent authors and papers, while the links between them denote the authorship relation. 
Subsequently, we derive the coauthorship collaboration network from the original bipartite network by projecting it onto the set of author nodes. 

Ih this new graph, denoted as $G' = (V, E)$, each author is represented by a vertex $v_i$, while the existence of an edge between two different authors means that there exists at least one path between them in the original bipartite graph $G'$, indicating a shared paper.

We decided to employ a weighted projection of $G$ to obtain $G'$. The weight of each edge corresponds to the number of common nodes in the original bipartite graph $G$, reflecting the number of papers authors have published together. 

This network structure aligns with the concept that frequent collaborators should exhibit stronger connections in the coauthorship collaboration network compared to authors with fewer shared publications.

...
(Qui dobbiamo scrivere anche che abbiamo tolto dal grafo i nodi isolati e forse anche il fatto che usiamo il reciproco dei pesi quando calcoliamo grandezze che usano il percorso più corto tra due nodi.)

### Small world-ness and scale free property



### Characteristic of the authors collaboration network



### Indentification of the most influential nodes


### Community detection and Louvain algorithm



## Results

## Discussion

## Conclusion