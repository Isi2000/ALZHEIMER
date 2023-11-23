import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import powerlaw
from collections import Counter

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

#Read data for degree distribution

degree_sequence = np.load('./results/degree_sequence.npy')

#Removing the zeros
degree_sequence = degree_sequence[degree_sequence != 0]

# Computing the degree probability mass function

pwl_distri = powerlaw.pdf(degree_sequence)

# Plotting the degree distribution

plt.figure(figsize=(10, 7))
plt.yscale('log')
plt.xscale('log')

powerlaw.plot_pdf(degree_sequence, color='b', linewidth=2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.xlabel('Degree', fontsize=16)
plt.ylabel('Probability $P(k)$', fontsize=16)
plt.title('Degree Distribution', fontsize=18)

plt.savefig('./images/degree_distribution.png')

# Fit function

fit_function = powerlaw.Fit(degree_sequence, discrete=True)
xmin = fit_function.power_law.xmin # minimum value to fit
alpha = fit_function.power_law.alpha # exponent
sigma = fit_function.power_law.sigma # standard deviation of alpha
D = fit_function.power_law.D # Kolmogorov-Smirnov statistic (good fit if D is small)

print(f'xmin = {xmin}')
print(f'alpha = {alpha}')
print(f'sigma = {sigma}')
print(f'D = {D}')

# Visualize distribution and the fit

plt.figure(figsize=(10, 7))
fig = powerlaw.plot_pdf([x for x in degree_sequence if x > xmin], 
                        color='b', linewidth=2, label = 'Empirical data')
fit_function.power_law.plot_pdf(ax = fig, color='r', linestyle='--',
                                label = 'Power law fit')

fig.legend(fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Degree ($k$)', fontsize=16)
plt.ylabel('Probability $P(k)$', fontsize=16)
plt.title('Degree Distribution', fontsize=18)
plt.savefig('./images/degree_distribution_fit.png')

