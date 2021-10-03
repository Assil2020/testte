# -*- coding: utf-8 -*-
"""SIC_Assil_Checkpoint8_K_means_&_Hierarchical_Clustering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S6rG9ObbV5earBhw75j3Uel74nxWzeYI
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA 
from sklearn.metrics import silhouette_score
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, normalize

df=pd.read_csv("CC GENERAL.csv")
df.head(5)

df.shape

print(df.info())

print(df.isnull().sum())

stats = df.describe()
stats=stats.transpose()
pd.DataFrame(stats)

df = df.drop("CUST_ID", axis = 1)
df['CREDIT_LIMIT'] = df['CREDIT_LIMIT'].fillna((df['CREDIT_LIMIT'].mean()))
df['MINIMUM_PAYMENTS'] = df['MINIMUM_PAYMENTS'].fillna((df['MINIMUM_PAYMENTS'].mean()))

corrmat = df.corr()
f, ax = plt.subplots(figsize =(15, 10))
sns.heatmap(corrmat, ax = ax, cmap ="YlGnBu", linewidths = 0.1)

plt.figure(figsize=(20,10))
sns.boxplot(data=df)
plt.xticks(rotation=90)

"""##Drop outliers according to z-score

"""

from scipy import stats

z = np.abs(stats.zscore(df))
print(z)

threshold = 3
print(np.where(z > 3))

df = df[(z < 3).all(axis=1)]

df.shape

df_scaled = normalize(df)
df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
df_scaled.head()

"""##Hierarchical clustering"""

X = df_scaled.iloc[:, [0, 13]].values

hierarchical = AgglomerativeClustering(n_clusters=4, affinity='euclidean', linkage='ward')  
y_hc = hierarchical.fit_predict(X)

"""##3. Plot the clusters. 

"""

#Data distribution before using clustering
plt.figure(figsize=(10, 7))
plt.subplots_adjust(bottom=0.1)
plt.scatter(X[:,0],X[:,1])
plt.title('Data distribution before using clustering')
plt.show()

#Data distribution after using clustering
plt.figure(figsize=(10, 7))
plt.subplots_adjust(bottom=0.1)

plt.scatter(X[y_hc == 0, 0], X[y_hc == 0, 1], s = 100, c = 'cyan', label = 'A Customers')
plt.scatter(X[y_hc == 1, 0], X[y_hc == 1, 1], s = 100, c = 'blue', label = 'B Customers')
plt.scatter(X[y_hc == 2, 0], X[y_hc == 2, 1], s = 100, c = 'yellow', label = 'C Customers')
plt.scatter(X[y_hc == 3, 0], X[y_hc == 3, 1], s = 100, c = 'peru', label = 'D Customers')

plt.title('4 Clusters of Customers')
plt.xlabel('BALANCE')
plt.ylabel('PAYMENTS')
plt.legend()

plt.show()

"""##Dendrogram"""

plt.figure(figsize=(10, 7))  
plt.title("Dendrograms")  
dend = shc.dendrogram(shc.linkage(df_scaled, method='ward'))

"""##Different k values and select the best one.

##Number of Clusters

##1- Elbow Method
"""

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

"""For the Elbow Methode, the best number of clusters is 3

##2- Silhouette Scores Method
"""

silhouette_scores = [] 

for n_cluster in range(2, 11):
    silhouette_scores.append(silhouette_score(df_scaled, KMeans(n_clusters = n_cluster).fit_predict(df_scaled))) 
    
# Plotting a bar graph to compare the results 
k = [2, 3, 4, 5, 6, 7, 8 ,9, 10] 
plt.bar(k, silhouette_scores) 
plt.xlabel('Number of clusters', fontsize = 10) 
plt.ylabel('Silhouette Score', fontsize = 10) 
plt.show()

"""For the Silhouette Scores Methode, the best number of clusters is 6

##Plot the clusters

##Three Clusters
"""

kmeans= KMeans(n_clusters=3, n_init=10, init= 'k-means++', algorithm='full', max_iter=300)
y_kmeans = kmeans.fit_predict(X)
labels= kmeans.labels_

pca= PCA(n_components=2)
X_PCA= pca.fit_transform(X)

pca_df = pd.DataFrame(data=X_PCA, columns=['BALANCE','PAYMENTS'])
pca_df['labels']= labels
pca_df.head()

##Plot the clusters with PCA
plt.figure(figsize=(10,8))
ax = sns.scatterplot(x='BALANCE', y='PAYMENTS', hue='labels', data=pca_df, palette='bright')

##Plot the clusters without PCA
plt.figure(figsize=(10, 8))

plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0, 1], s = 100, c = 'blue', label = 'Customers 1')
plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1, 1], s = 100, c = 'orange', label = 'Customers 2')
plt.scatter(X[y_kmeans == 2, 0], X[y_kmeans == 2, 1], s = 100, c = 'green', label = 'Customers 3')

plt.title('3 Clusters of Customers')
plt.xlabel('BALANCE')
plt.ylabel('PAYMENTS')
plt.legend('label')

plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker ='*', s=300, c='black', label = 'Centroids')

"""##Six Clusters"""

kmeans= KMeans(n_clusters=6, n_init=10, init= 'k-means++', algorithm='full', max_iter=300)
y_kmeans = kmeans.fit_predict(X)
labels= kmeans.labels_

pca= PCA(n_components=2)
X_PCA= pca.fit_transform(X)

pca_df = pd.DataFrame(data=X_PCA, columns=['BALANCE','PAYMENTS'])
pca_df['labels']= labels
pca_df.head()

##Plot the clusters with PCA
plt.figure(figsize=(10,8))
ax = sns.scatterplot(x='BALANCE', y='PAYMENTS', hue='labels', data=pca_df, palette='bright')

##Plot the clusters without PCA
plt.figure(figsize=(10, 8))

plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0, 1], s = 100, c = 'blue', label = 'Customers 1')
plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1, 1], s = 100, c = 'orange', label = 'Customers 2')
plt.scatter(X[y_kmeans == 2, 0], X[y_kmeans == 2, 1], s = 100, c = 'green', label = 'Customers 3')
plt.scatter(X[y_kmeans == 3, 0], X[y_kmeans == 3, 1], s = 100, c = 'red', label = 'Customers 4')
plt.scatter(X[y_kmeans == 4, 0], X[y_kmeans == 4, 1], s = 100, c = 'purple', label = 'Customers 5')
plt.scatter(X[y_kmeans == 5, 0], X[y_kmeans == 5, 1], s = 100, c = 'brown', label = 'Customers 6')

plt.title('6 Clusters of Customers')
plt.xlabel('BALANCE')
plt.ylabel('PAYMENTS')
plt.legend('label')

plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker ='*', s=300, c='black', label = 'Centroids')

"""##Best Model

##Three Clusters
"""

hierarchical_ = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward').fit_predict(X)
kmeans_ = KMeans(n_clusters = 3, init = 'k-means++', random_state = 42).fit_predict(X)

Hierarchical_Silhouette_Score = metrics.silhouette_score(X, hierarchical_, metric='euclidean')
kmeansSilhouette_Score = metrics.silhouette_score(X, kmeans_, metric='euclidean')

Clustering_Silhouette_Scores = [ ['KMeans',kmeansSilhouette_Score],['Hierarchical',Hierarchical_Silhouette_Score]]
Clustering_Silhouette_Scores = pd.DataFrame(Clustering_Silhouette_Scores, columns=['Clustering Method', 'Silhouette Score']) 
Clustering_Silhouette_Scores.sort_values(by='Silhouette Score', ascending= False)

"""The best model is Kmeans model

##Six Clusters
"""

hierarchical_ = AgglomerativeClustering(n_clusters=6, affinity='euclidean', linkage='ward').fit_predict(X)
kmeans_ = KMeans(n_clusters = 6, init = 'k-means++', random_state = 42).fit_predict(X)

Hierarchical_Silhouette_Score = metrics.silhouette_score(X, hierarchical_, metric='euclidean')
kmeansSilhouette_Score = metrics.silhouette_score(X, kmeans_, metric='euclidean')

Clustering_Silhouette_Scores = [ ['KMeans',kmeansSilhouette_Score],['Hierarchical',Hierarchical_Silhouette_Score]]
Clustering_Silhouette_Scores = pd.DataFrame(Clustering_Silhouette_Scores, columns=['Clustering Method', 'Silhouette Score']) 
Clustering_Silhouette_Scores.sort_values(by='Silhouette Score', ascending= False)

"""The best model is Kmeans model

##Another validation metric

I'll choose the Spectral Clustering & I'll test this metric & compare with Hierarchical & Kmeans Clustering
"""

spectral = SpectralClustering(n_clusters=3, affinity="nearest_neighbors", assign_labels='discretize',random_state=40)
y_spectral = spectral.fit_predict(X)

hierarchical_ = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward').fit_predict(X)
kmeans_ = KMeans(n_clusters = 3, init = 'k-means++', random_state = 42).fit_predict(X)
spectral_ = SpectralClustering(n_clusters=3, affinity="nearest_neighbors", assign_labels='discretize',
                                      random_state=40).fit_predict(X)

kmeansSilhouette_Score = metrics.silhouette_score(X, kmeans_, metric='euclidean')
Hierarchical_Silhouette_Score = metrics.silhouette_score(X, hierarchical_, metric='euclidean')
Spectral_Silhouette_Score = metrics.silhouette_score(X, spectral_, metric='euclidean')

Clustering_Silhouette_Scores = [['KMeans',kmeansSilhouette_Score],['Hierarchical',Hierarchical_Silhouette_Score], ['Spectral', Spectral_Silhouette_Score]]
Clustering_Silhouette_Scores = pd.DataFrame(Clustering_Silhouette_Scores, columns=['Clustering Method', 'Silhouette Score']) 
Clustering_Silhouette_Scores.sort_values(by='Silhouette Score', ascending= False)

"""Kmean clustering still the best model for our exemple"""

