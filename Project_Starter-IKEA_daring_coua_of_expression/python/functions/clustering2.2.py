#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 10:18:52 2023

@author: Wang386
"""

import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import os

# read file from the data folder
multiGDF = gpd.read_file('data/training_data.shp')



# drop the unneccessary columns
# here we try two methods in clustring, the one including the thermal data, and another one we drop it
multiGDF_clear = multiGDF.drop(columns=['geometry'])
multiGDF_clear_without_thermal = multiGDF.drop(columns=['geometry','Thrml_1','Thrml_2','Thrml_3'])



# rescale the data to geet better result
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()

# the same idea in both data (1. the data with thermal part, 2.the data without thermal part
scaler.fit(multiGDF_clear) 
scaled_multiGDF_clear = scaler.transform(multiGDF_clear)

scaler.fit(multiGDF_clear_without_thermal) 
scaled_clear_without_thermal = scaler.transform(multiGDF_clear_without_thermal)




# try to find the suitable K for K means
# this is the elbow curve method
# reference: https://www.analyticsvidhya.com/blog/2021/05/k-mean-getting-the-optimal-number-of-clusters/
Sum_of_squared_distances = []
K = range(1,30)
for num_clusters in K :
    kmeans = KMeans(n_clusters=num_clusters)

    kmeans.fit(scaled_multiGDF_clear)

    Sum_of_squared_distances.append(kmeans.inertia_)


# plot the figure and find the point, which is 5
plt.plot(K,Sum_of_squared_distances,'bx-')
plt.xlabel('Values of K') 
plt.ylabel('Sum of squared distances/Inertia') 
plt.title('Elbow Method For Optimal k (with thermal data)')
plt.savefig('output/Elbow Method For Optimal k (with thermal data).png')
plt.show()

# here is the same elbow curve method to find suitable K
# but this is for the data droped thermal part
Sum_of_squared_distances = []
K = range(1,30)
for num_clusters in K :
    kmeans = KMeans(n_clusters=num_clusters)

    kmeans.fit(scaled_clear_without_thermal)

    Sum_of_squared_distances.append(kmeans.inertia_)


# plot the figure and find the point, which is 5
plt.plot(K,Sum_of_squared_distances,'bx-')
plt.xlabel('Values of K') 
plt.ylabel('Sum of squared distances/Inertia') 
plt.title('Elbow Method For Optimal k (without thermal data)')
plt.savefig('output/Elbow Method For Optimal k (without thermal data).png')
plt.show()



# apply the K = 5 to the KMeans
kmeans = KMeans(n_clusters = 5)


# fit in the scaled data with thermal part
y = kmeans.fit_predict(scaled_multiGDF_clear)


# fit in the scaled data with no thermal part
y_without_thermal = kmeans.fit_predict(scaled_clear_without_thermal)
                                      


# add clustring result to the original data  
multiGDF['clustring'] = y
multiGDF['clustring_without_thermal'] = y_without_thermal



# save it in the output fold
multiGDF.to_file(filename='output/clustring_result.geojson', driver='GeoJSON')
    


#%%

# Gaussian mixture model (GMM)
# reference: https://www.researchgate.net/publication/330509635_Crop_type_mapping_without_field-level_labels_Random_forest_transfer_and_unsupervised_clustering_techniques

from sklearn import mixture
from sklearn.mixture import GaussianMixture as GMM

# this method is trying to find the suitable n_components for data with thermal
# however for this data, it is much more comlex than the example data in the link,
# we tried several times but can't find a suitable one
# so we set n_components as 5
# reference:https://jakevdp.github.io/PythonDataScienceHandbook/05.12-gaussian-mixtures.html

n_components = np.arange(1, 30)
models = [GMM(n, covariance_type='full', random_state=0).fit(multiGDF_clear)
          for n in n_components]

plt.plot(n_components, [m.bic(multiGDF_clear) for m in models], label='BIC')
plt.plot(n_components, [m.aic(multiGDF_clear) for m in models], label='AIC')
plt.legend(loc='best')
plt.xlabel('n_components');




# fit in gm with unscaled data with thermal, because GM is less sensitive to scale
gm = GMM(n_components=5).fit(multiGDF_clear)
gm_y_thermal = gm.predict(multiGDF_clear)



# fit in gm with unscaled data with no thermal
gm = GMM(n_components=5).fit(multiGDF_clear_without_thermal)
gm_y_without_thermal = gm.predict(multiGDF_clear_without_thermal)



multiGDF['GMM_clustring'] = gm_y_thermal
multiGDF['GMM_clustring_without_thermal'] = gm_y_without_thermal



# unfinished


from sklearn import datasets
from sklearn.metrics import silhouette_samples,silhouette_score
# calculate Silhouette Score to check how good the clustering it is 

score1 = silhouette_score(, kmeans.labels_, metric='euclidean')
print(score1)

silhouette_vals = silhouette_samples(multiGDF_clear_without_thermal,gm_y_without_thermal)

score2 = silhouette_score(, kmeans.labels_, metric='euclidean')
print(score2)


'''
# plot the identification of the tree species
multiGDF.plot( column = 'clustring' )
plt.legend()
plt.title('Clustering Result of Tree Species\n(with thermal data)')




multiGDF.plot( column = 'clustring_without_thermal',legend=True, cmap='tab20')
plt.legend()
plt.title('Clustering Result of Tree Species\n(without thermal data)')


'''
