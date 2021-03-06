# -*- coding: utf-8 -*-
"""Models.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A2Uw-sUxi6iu-OmeodPQaW5vRTfpMQwS

#**5 MODEL**
"""

# Scale features
scaled_features = pd.DataFrame(StandardScaler().fit_transform(df_final), 
                               index=df_final.index, columns=df_final.columns)

# Clustering
Z = linkage(scaled_features, method='complete')

# Plot dendrogram and highlight cluster
fig, ax = plt.subplots(figsize=(14, 20))
dn = dendrogram(Z, labels=df_final.index, orientation='right',
                leaf_rotation=0, leaf_font_size=14)
plt.show()

# Form flat clusters from the hierarchical clustering defined by linkage matrix
df_final['cluster'] = fcluster(Z, 4, criterion='maxclust')
spb_cluster = df_final.loc['Saint Petersburg', 'cluster']
clust = df_final[df_final.cluster == spb_cluster]

# Convert to list
cities = clust.index.tolist()
cities

# Tsne map function
def tsne_map(features=df_final, l_rate=100):
    """ Generate and plot tsne map based on the matrix
    Args:
        features: selected dataframe
        l_rate: learning rate
    """
    tsne_output = TSNE(learning_rate=l_rate).fit_transform(features.drop('cluster', axis=1))
    tsne_df = pd.DataFrame(index=df_final.index)
    tsne_df['x'] = tsne_output[:, 0]
    tsne_df['y'] = tsne_output[:, 1]
    
    # Separate SPb cluster from others
    tsne_df['cluster'] = 0
    spb_cluster = df_final.loc['Saint Petersburg', 'cluster']
    tsne_df.loc[df_final.cluster == spb_cluster, 'cluster'] = 1


    fig, ax = plt.subplots(figsize=(5, 5))
    sns.scatterplot(data=tsne_df, x='x', y='y', 
                    hue='cluster', palette=['grey', 'blue'],
                    alpha=0.6,
                    ax=ax)
    ax.set_title('t-SNE map of clustering results')
    ax.legend('')
    plt.show()

tsne_map(df_final)

# Initialize and fit the model
pca = PCA()
pca.fit(scaled_features)

# Set up the chart wiht principal components
pca_features = pd.DataFrame(index=range(pca.n_components_))
pca_features.index.name='PCA component'
pca_features['Exp. Variance'] = pca.explained_variance_

# Get PCA features
n_comp = 3
pca = PCA(n_components=n_comp)
pca_features = pd.DataFrame(pca.fit_transform(scaled_features), index=scaled_features.index,
                           columns=['PCA_' + str(n) for n in range(n_comp)])
pca_features.describe()

Z = linkage(pca_features, method='complete')

# Plot dendrogram and highlight cluster
fig, ax = plt.subplots(figsize=(14, 20))
dn = dendrogram(Z, labels=pca_features.index, orientation='right',
                leaf_rotation=0, leaf_font_size=14)
plt.show()

# Form cluster based on pca linkage
pca_features['cluster'] = fcluster(Z, 3, criterion='maxclust')
spb_cluster2 = pca_features.loc['Saint Petersburg', 'cluster']
clust2 = pca_features[pca_features.cluster == spb_cluster2]
clust2.shape

cities_pca = clust2.index.tolist()
cities_pca

tsne_map(pca_features)