import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import powerlaw
from tqdm import tqdm

# Read the data

data_list = []

with open('./results/num_paper_authors.json', 'r') as file:
    for line in file:
        data_list.append(json.loads(line))

num_paper_authors_df = pd.DataFrame(data_list)

filtered_df = num_paper_authors_df.loc[(num_paper_authors_df['YearInterval'] >= 1935) 
                                       & (num_paper_authors_df['YearInterval'] <= 2015)]

# Plotting the results

os.makedirs('images', exist_ok=True)

plt.figure(figsize=(10, 6))
plt.scatter(filtered_df['YearInterval'], filtered_df['AvgAuthorsPerArticle'])
plt.xlabel('Year interval')
plt.ylabel('Average number of authors per article')
plt.title('Average number of authors per article over time')
plt.savefig('./images/avg_authors_per_article.png')

plt.figure(figsize=(10, 6))
plt.scatter(filtered_df['YearInterval'], filtered_df['NumArticles'], 
            s=30, c='b', marker='o', label = 'Number of Articles')
plt.scatter(filtered_df['YearInterval'], filtered_df['NumAuthors'], s=30, c='r', marker='o',
            label = 'Number of Authors')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Number of Articles and Authors')
plt.title('Number of Articles per Year')
plt.savefig('images/number_of_articles_per_year.png')

#-----------------------------------------------------------------------------------------------

# Read data for degree distribution
degree_sequence = np.load('./results/degree_sequence.npy')

# Removing the zeros
degree_sequence = degree_sequence[degree_sequence != 0]

# Fit function
fit_function = powerlaw.Fit(degree_sequence, discrete=True)
xmin = fit_function.power_law.xmin  # minimum value to fit
alpha = fit_function.power_law.alpha  # exponent
sigma = fit_function.power_law.sigma  # standard deviation of alpha
D = fit_function.power_law.D  # Kolmogorov-Smirnov statistic (good fit if D is small)

print('\n', f'xmin = {xmin}')
print(f'alpha = {alpha}')
print(f'sigma = {sigma}')
print(f'D = {D}')

# Plotting the degree distribution and fit
plt.figure(figsize=(10, 7))
plt.yscale('log')
plt.xscale('log')

# Plotting the empirical data with both line and points
data = [x for x in degree_sequence if x > xmin]
fig = powerlaw.plot_pdf(data, color='b', marker='o', linewidth=2, label='Empirical data')

# Plotting the fit of the power law
fit_function.power_law.plot_pdf(ax=fig, color='r', linestyle='--', label='Power law fit')

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Degree', fontsize=16)
plt.ylabel('Probability Density', fontsize=16)
plt.title('Degree Distribution with Power Law Fit', fontsize=18)
plt.legend()

plt.savefig('./images/degree_distribution.png')

# Calculate n_tail and n
n_tail = np.sum(degree_sequence >= xmin)
n = len(degree_sequence)
head_data = degree_sequence[degree_sequence < xmin]

# Number of datasets to generate
num_datasets = 100

# List to store the D values
D_values = []

# Generate datasets with specified probability distribution
for _ in tqdm(range(num_datasets), desc="Generating datasets", unit="dataset"):
    generated_data_tail = fit_function.power_law.generate_random(n_tail, estimate_discrete=True)
    generated_data_head = np.random.choice(head_data, n - n_tail)
    generated_data = np.concatenate((generated_data_tail, generated_data_head))
    generated_data_fit = powerlaw.Fit(generated_data, discrete=True)
    D_value = generated_data_fit.power_law.D
    #x_min = generated_data_fit.power_law.xmin
    D_values.append(D_value)

# Calculate the p-value

p_value = np.sum(D_values >= D) / num_datasets
print(p_value)

# Plot the D values distribution

plt.figure(figsize=(10, 7))
plt.hist(D_values, bins=50)
plt.xlabel('D value', fontsize=16)
plt.ylabel('Frequency', fontsize=16)
plt.title('D values distribution', fontsize=18)
plt.savefig('./images/D_values_distribution.png')


# Ho un paio di dubbi: 
# 1. Probabilmente sarebbe utile mettere un xmax quando si generano i dati ma, leggendo la documentazione di 
# powerlaw, ho visto che non c'è un modo banale per farlo con powerlaw.generate_random (c'è proprio scritto
# 'If xmax is present, it is currently ignored'). Non so se ha senso perderci tempo, magari non cambia molto.
# 
# 2. Per generare i dati bisognerebbe fare così:
# - si contanto il numero di elementi della coda (n_tail) e il numero di elementi della testa (n - n_tail) del dataset
# originale, ovvero il numero di elementi che sono rispettivamente >= xmin e < xmin.
# - Poi con probabilità p = n_tail / n si genera un elemento dalla power law 'fit_function' (tale che x > x_min) e con 
# probabilità 1 - p si pesca (secondo una distribuzione uniforme) un elemento dalla testa del dataset originale (tale che x <x_min).
# - Si ripete questo processo fino a quando non si ottiene un dataset di lunghezza n (lunghezza del dataset originale).
# Si fa così per ottenere dei dataset che seguono la stessa distribuzione di probabilità del dataset originale.
# Ho provato a farlo esattamente in quel modo ma ci mette una vita a generare un dataset...
# Quello che ho fatto io è stato semplicemente generare n_tail elementi dalla power law e n - n_tail elementi dalla testa
# del dataset originale (tale che x < x_min).
# Secondo me è uguale ma volevo un attimo ragionarci con te.