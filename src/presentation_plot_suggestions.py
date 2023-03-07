#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 7 10:21:14 2023

@author: Avi
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings; warnings.filterwarnings(action='once')

large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'axes.titlesize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")
#%matplotlib inline

# Version
print(mpl.__version__)  #> 3.0.0
print(sns.__version__)  #> 0.9.0

#%% Violin plot (to show the distribution of a chosen variable for all the datasets)

# Import Data
df1 = pd.read_csv("data/sig.csv")
df2 = pd.read_csv("data/total_dataset.csv")
df3 = pd.read_csv("data/phimumu.csv")
df4 = pd.read_csv("data/kmumu.csv")

df1.insert(0, 'File Path', 'sig.csv')
df2.insert(0, 'File Path', 'total_dataset.csv')
df3.insert(0, 'File Path', 'phimumu.csv')
df4.insert(0, 'File Path', 'kmumu.csv')

df_combined = df1.append(df2).append(df3).append(df4)

# Print the merged dataset
#print(merged_df)

# Create Figure and Axes
fig, ax = plt.subplots(figsize=(13, 10), dpi=80)

# Plot Violin Plot
sns.violinplot(x='File Path', y='Kstar_M', data=df_combined, scale='width', inner='quartile', ax=ax)

# Add Title
ax.set_title("Violin Plot of Kstar_M by Event file", fontsize=22)

# Show Plot
plt.show()


#%% continuous variable data
'''
# Import Data
df1 = pd.read_csv("data/sig.csv")
df2 = pd.read_csv("data/total_dataset.csv")
df3 = pd.read_csv("data/phimumu.csv")
df4 = pd.read_csv("data/kmumu.csv")

df1.insert(0, 'File Path', 'sig.csv')
df2.insert(0, 'File Path', 'total_dataset.csv')
df3.insert(0, 'File Path', 'phimumu.csv')
df4.insert(0, 'File Path', 'kmumu.csv')

df_combined = df1.append(df2).append(df3).append(df4)

# Prepare data
x_var = 'B0_ID'
groupby_var = 'File Path'
df_agg = df_combined.loc[:, [x_var, groupby_var]].groupby(groupby_var)
vals = [df[x_var].values.tolist() for i, df_combined in df_agg]

# Draw
plt.figure(figsize=(16,9), dpi= 80)
colors = [plt.cm.Spectral(i/float(len(vals)-1)) for i in range(len(vals))]
n, bins, patches = plt.hist(vals, 30, stacked=True, density=False, color=colors[:len(vals)])

# Decoration
plt.legend({group:col for group, col in zip(np.unique(df_combined[groupby_var]).tolist(), colors[:len(vals)])})
plt.title(f"Stacked Histogram of ${x_var}$ colored by ${groupby_var}$", fontsize=22)
plt.xlabel(x_var)
plt.ylabel("Frequency")
plt.ylim(0, 25)
plt.xticks(ticks=bins[::3], labels=[round(b,1) for b in bins[::3]])
plt.show()
'''

#%% Dendrogram plot
'''

import pandas as pd
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

# Load the datasets from CSV files into a list of dataframes
#dfs = [pd.read_csv(f"dataset_{i}.csv") for i in range(1, 13)]

# Calculate the total number of observations in each dataset
#n_obs = [df.shape[0] for df in dfs]
n_obs = [1500, 56000, 340, 25, 300, 30, 1, 1, 1, 1, 1, 1]
# Perform hierarchical clustering using the "single" linkage method
Z = hierarchy.linkage(n_obs, method="single")

# Plot the dendrogram
plt.figure()
dn = hierarchy.dendrogram(Z)
plt.show()
'''
