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

#### The scale free property 

One of the notable models for complex networks is the **scale-free network**, characterized by a degree distribution that follows a heavy-tailed power law. 
This implies an abundance of nodes with degrees significantly higher than the average, and this property is associated with the network's **robustness**. 
To investigate this, we analyzed the power-law degree distribution of the coauthorship collaboration network using methods outlined in (*citation*).

The analysis involves the following steps:

1. Firstly, we fit the tail of the empirical distribution of the degree with a power-law distribution:

$$
p(d) \propto d^{-\alpha}
$$

Here, \( \alpha \) is a constant parameter, typically \( 2 < \alpha < 3 \). 
In our context, \( d \) represents the degrees of nodes, and \( p(d) \) represents the probability degree distribution of the network, 
normalized to one. 
In most cases, the power law model is applicable only on the tail of the empirical distribution, 
meaning for degrees greater than a minimum d_{\text{min}}. 
The fitting function will be characherized by an estimated scaling parameter $\hat{\alpha}$ and the lower 
bound $d_{\text{min}}$ .
Then we compute the value $D$ of the Kolmogorov-Smirnov (KS) statistics for this fit, which is interpreted as a "distance"
between the empirical distribution and the fitted power law.

Then, in order to assess the goodness of the fit, we use the following procedure:

2. We generate a substantial number of synthetic datasets mimic the distribution of the empirical data below \(d_{\text{min}}\) 
while following the fitted power law above \(d_{\text{min}}\). 
In particular, we generate from the fitted power law a number of synthetic datasets equal to the number of elements in the 
original dataset which have degree greater than \(d_{\text{min}}\); while for the remaining elements we sample uniformly at random
from the observed data set that have degree less than \(d_{\text{min}}\).

3. We individually fit each synthetic dataset to its own power-law model and calculate the KS statistic for each 
one relative to its own model.

4. Finally, the goodness of the fit is assessed through the *p-value*,  which is computed as the fraction 
of times the KS statistics of the syntetic datases is larger than the observed KS distance. 
The *p-value* is therefore interpreted as a measure of the plausibility of the hypothesis that our data conforms 
to a power-law distribution. 

A large *p-value* suggests that the difference between empirical data and the model can be attributed to 
statistical fluctuations. Conversely, if the *p-value* is smaller than a specified threshold (in our case, \(0.1\)),
the model does not provide a plausible fit for the data, and the hypothesis is rejected.
To achieve accuracy to about two decimal places, we generate \(2500\) synthetic sets. 

##### Scale free property results

The results of the analysis are summarized in the following table:

| Parameter | Value |
| --- | --- |
| $\hat{\alpha}$ | 1.91 |
| $d_{\text{min}}$ | 7 |
| $D$ | 0.029 |

The plot of the empirical degree distribution and the fitted power law is shown in the figure below:

![Degree distribution](./images/degree_distribution.png)

Instead, the plot of the cumulative distribution function (CDF) of the empirical data and the fitted power 
law is shown in the figure below:

![CDF](./images/cumulative_degree_distribution.png)

We found that the *p-value* is equal to 0.0, which is smaller than the threshold of 0.1. 
Therefore, we reject the hypothesis that the data conforms to a power-law distribution.

### Characteristic of the authors collaboration network



### Indentification of the most influential nodes

The identification of the most influential nodes in a network is a fundamental task in network analysis, 
since it allows to identify the nodes that are most important for the structure and the functioning of the network.
There are many metrics that can be used to evaluate the importance of a node in a network, each of them
capturing a different aspect of the node's importance.
In this section, we will describe some of the most common metrics for node importance evaluation,
and we will use them to identify the most influential authors in the Alzheimer's disease collaboration network.

#### Degree centrality

The degree centrality quantifies the importance of a node in a network by computing the degree of each node (
i.e. the number of links that the node has with other nodes in the network),
and then normalizing it by the maximum possible degree in the network (which is given by the number of nodes
minus one): 

$$
C_D(v) = \frac{k_v}{n-1}
$$

where $k_v$ is the degree of the node $v$ and $n$ is the number of nodes in the network.
The degree centrality assigns a higher score to the nodes with a higher degree, meaning that the nodes with
more links are considered more important.

QUI MI è VENUTO UN DUBBIO: DOBBIAMO CONSIDERARE IL FATTO CHE IN NOSTRO GRAFO è PESATO??

#### Betweenness Centrality

Betweenness centrality is a measure that assesses the importance of a node in a network by calculating the 
number of shortest paths passing through that node for all pairs of nodes in the network. 
The measure is then normalized by the maximum possible number of shortest paths between all pairs of nodes 
in the network. 
Mathematically, it is expressed as:

$$
C_B(v) = \frac{\sum_{s \neq v \neq t} \sigma_{st}(v)}{\sum_{s \neq t} \sigma_{st}}
$$

Here, $\sigma_{st}$ represents the number of shortest paths between nodes $s$ and $t$, and $\sigma_{st}(v)$ 
denotes the number of those paths that traverse the node $v$. Betweenness centrality identifies nodes that act 
as crucial bridges between different sections of the network, playing a pivotal role in the flow of information.

In our specific context, we need to consider the coauthorship collaboration network as a weighted graph. 
Consequently, when calculating shortest paths, we must treat paths with higher weights as "shortest", reflecting 
more frequent collaborations between authors. However, in algorithms for computing shortest paths, weights are 
often interpreted as distances or costs, implying that shorter paths have lower weights.

Therefore, in our calculations for betweenness centrality, we must account for the weighted nature of the graph 
by taking the reciprocal of the weights. 
This adjustment ensures that the algorithms correctly identify paths with the highest collaborative significance, 
aligning with the notion that heavier weights represent stronger connections between authors.

#### Closeness centrality

The closeness centrality is defined as the inverse of the average distance between a node and all other nodes.
For each node $v$ in the network, the closeness centrality is computed by calculating the average of the distances 
from the node $v$ to all other nodes in the network (length of the shortest path between $v$ and the other nodes),
and then taking the reciprocal of this value:

$$
C_C(v) = \frac{1}{\frac{1}{n-1} \sum_{u \neq v} d(v,u)}
$$

where $d(v,u)$ is the length of the shortest path between the nodes $v$ and $u$, and $n$ is the number of nodes
in the network.

Closeness centrality provides a metric for evaluating how proximate a node is to all other nodes within a network. 
Nodes exhibiting high closeness centrality can efficiently reach all other nodes in the network in a limited number 
of steps. This measure is indicative of how rapidly information can disseminate from a particular node to the 
entire network.

Similar to the considerations for betweenness centrality, the computation of shorter paths in a weighted graph 
necessitates the adjustment of weights. 
Also in this case, we take the reciprocal of the weights to properly account for the weighted nature of the graph. 

#### Eigenvector centrality

The eigenvector centrality measures the importance of a node in a network by considering the importance of 
its neighbors, providing a recursive definition of node importance.

The eigenvector centrality \(x_i\) for node \(i\) is defined as:

$$
x_i = \frac{1}{\lambda} \sum_k a_{k,i} \, x_k
$$

where \(A = (a_{i,j})\) represents the adjacency matrix of the network, \(\lambda \neq 0\) is a constant, 
and \(x_k\) is the centrality of node \(k\). The same relationship can be expressed in matrix form as:

$$
\lambda x = x A
$$

where \(\lambda\) is the eigenvalue and \(x\) is the eigenvector of the adjacency matrix \(A\).

Consequently, the eigenvector centrality is given by the eigenvectors associated with the largest eigenvalue 
of the adjacency matrix of the network.

For computing the eigenvector centrality of the coauthorship collaboration network, we employed the power 
iteration method. 
This iterative technique starts with a random vector and repeatedly multiplies it by the adjacency matrix 
of the network until the vector converges to the eigenvector associated with the largest eigenvalue of the 
adjacency matrix. At each iteration, the vector is normalized to prevent it from growing indefinitely.

#### Final ranking with borda count

After the evalution of the importance of each node in the network using the four metrics described above,
we combined the results of the four metrics to obtain a final ranking of the most influential authors in the
Alzheimer's disease collaboration network.

In order to combine the results, we used the Borda count method, which is a single-winner election method in
which voters rank candidates in order of preference.
In particular, for each metric, we ranked the authors in descending order according to the value of the metric,
and we assigned to each author a score equal to the number of authors that are ranked below him.
Then, we summed the scores obtained by each author for each metric, and we ranked the authors according to
the total score.


### Community detection and Louvain algorithm

Community detection is the process of identifying groups of nodes that are more densely connected to each 
other than to the rest of the network. This can be useful in order to understand the structure of the network and to identify nodes wich shares similar
characteristics or functions.
In our context, communities represent groups of authors that have a higher tendency to collaborate with each other.
There is no universally accepted definition of what constituets a community, but there are several measures
that can be used to evaluate the quality of a community partition of a network.
In general, a good community partition is characterized by a high density of edges within communities and a 
low density of edges between communities.
So that, a measure of the quality of a community partition of a network is the modularity, which, for an undirected 
network, is defined as:

$$
Q = \frac{1}{2m} \sum_{i,j} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)
$$ 

where $A_{ij}$ is the element of the adjacency matrix of the network, $k_i$ and $k_j$ are the degrees of the 
nodes $i$ and $j$, $m$ is the number of edges in the network, $c_i$ and $c_j$ are the communities to which 
the nodes $i$ and $j$ belong, and $\delta(c_i, c_j)$ is the Kronecker delta function, which is equal to 1 
if $c_i = c_j$ (the nodes $i$ and $j$ belong to the same community) and 0 otherwise.
Modularity ranges from -1 to 1, and a value greater than 0.3 is generally considered as a good partition.
The modularity is positive if the number of edges within communities is greater than the expected number of
edges in a random network with the same degree distribution.
There are several algorithms for community detection, and many of them are based on the maximization of the
modularity.
In our project, we performed the community detection using the Louvain algorithm, which is a modularity-based,
agglomerative, heuristic method.
This algorithm, proposed by Blondel et al. in 2008, have been shown to be very fast and to produce partitions 
with a high modularity.
It consists of two phases: 
1. The algorithm starts by assigning each node to its own community. Then, for each node in the network, it
evaluates the gain in modularity that would result from moving the node to each of its neighbors' communities as:

$$
\Delta Q = \frac{1}{2m} \left[ \frac{\sum_{in} + k_{i,in}}{2m} - \left( \frac{\sum_{tot} + k_i}{2m} \right)^2 \right] - \frac{1}{2m} \left[ \frac{\sum_{in}}{2m} - \left( \frac{\sum_{tot}}{2m} \right)^2 - \left( \frac{k_i}{2m} \right)^2 \right]
$$

where $\sum_{in}$ is the sum of the weights of the links between the node $i$ and the nodes in the community
to which $i$ belongs, $\sum_{tot}$ is the sum of the weights of the links between the node $i$ and all the
nodes in the network, $k_i$ is the degree of the node $i$, $k_{i,in}$ is the sum of the weights of the links
between the node $i$ and the nodes in the community to which $i$ belongs, and $m$ is the sum of the weights
of all the links in the network.
The order im which the nodes does not have significant influence on the final modularity value, but it 
may affect the computational time. 
The node is then moved to the neighbor's community that results in the largest increase in modularity.
This process is repeated iteratively until no further increase in modularity can be achieved.

2. In the second phase, the algorithm builds a new network whose nodes are the communities found in the first
phase. The weights of the links between the communities are equal to the sum of the weights of the links
between the nodes in the two communities. The algorithm then repeats the first phase on this new network.

The two phases are repeated iteratively until a maximum of modularity is reached.

The Louvain algorithm is an agglomerative and hierarchical method, meaning that it starts from the nodes
and builds the communities from the bottom up.

#### Community detection results




## Results

Per ora i risultati li ho messi nella sezione Materials and Methods, ma poi li sposterò qui.

## Discussion

## Conclusion