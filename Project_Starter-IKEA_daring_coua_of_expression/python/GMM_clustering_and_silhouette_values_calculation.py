#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Geoscripting 2023
# Final Project
# Challenge 2 - Tree Species Classification using UAV Imagery
# Team: IKEA Coua
"""

 # This file is part of the Project_Starter-IKEA_daring_coua_of_expression distribution
 # (https://git.wur.nl/geoscripting-2023-january/staff/project/Project_Starter-IKEA_daring_coua_of_expression).
 # Copyright (c) 2023 IKEA_daring_coua_of_expression.
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #

import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import copy



#%%
'''

Part 1

- Apply Gaussian mixture model (GMM) for tree species clustering in both dataset:
  1. the data with thermal part
  2. the data without thermal part
  
- the data do not need to be normalised


- try to find the suitable n components by minimized BIC and AIC, 
  but it doesn't show a very clear point, 
  so we use the same 'n' as it in step1  
 

- Get the identification of tree species


'''


# Gaussian mixture model (GMM)
# reference: https://www.researchgate.net/publication/330509635_Crop_type_mapping_without_field-level_labels_Random_forest_transfer_and_unsupervised_clustering_techniques

from sklearn.mixture import GaussianMixture as GMM


# read file from the data folder
multiGDF = gpd.read_file('data/training_data.shp')



# drop the unneccessary columns
# here we try two methods in clustering, the one including the thermal data, and another one we drop it
multiGDF_clear = multiGDF.drop(columns=['geometry'])
multiGDF_clear_without_thermal = multiGDF.drop(columns=['geometry','Thrml1','Thrml2','Thrml3'])



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


# add the new column in the original data set and output results as shapefile

multiGDF_thermal_copy = copy.deepcopy(multiGDF)
multiGDF_thermal_copy['cluster'] = gm_y_thermal
multiGDF_thermal_copy.to_file( filename = 'output/Python_Polygons_clustered_GMM_with_Thermal.shp', driver = 'ESRI Shapefile' )


multiGDF_no_thermal_copy = copy.deepcopy(multiGDF)
multiGDF_no_thermal_copy['cluster'] = gm_y_without_thermal
multiGDF_no_thermal_copy.to_file( filename = 'output/Python_Polygons_clustered_GMM_without_Thermal.shp', driver = 'ESRI Shapefile' )



#%%
'''
Part 2

Because we don't have validation data, so we try to use Silhouette Score to 
measure how similar a data point is within-cluster (cohesion) compared to 
other clusters (separation), which means how good the clustering is.

We apply 3 data set (both for with thermla and without thermal part):
    1. the data generate by K means in python
    2. the data generate by clara in R
    3. the data generate by GMM in python


Then we find the Silhouette Score for GMM is -0.06
So we make a loop to see how much the n should be in GMM, that Silhouette Score
can be positive, and we also draw a line chart
(the answer is 20 from the chart)


'''
from sklearn.metrics import silhouette_score

# calculate Silhouette Score to check how good the clustering it is 
# reference: https://www.guavus.com/technical-blog/unsupervised-machine-learning-validation-techniques/


# Read in the normalised data and clustering result from KMeans from csv
r_with_thermal = pd.read_csv('data/R_KMeans_Normalised_Polygon_data_with_Thermal.csv', sep=' ')
r_without_thermal = pd.read_csv('data/R_KMeans_Normalised_Polygon_data_with_Thermal.csv', sep=' ')

py_with_thermal = pd.read_csv('output/Python_KMeans_Normalised_Polygon_data_with_Thermal.csv', sep=',')
py_without_thermal = pd.read_csv('output/Python_KMeans_Normalised_Polygon_data_without_Thermal.csv', sep=',')


# Apply silhouette score in the data generate from Python Kmeans
silhouette_km_py = silhouette_score(py_with_thermal.iloc[:, 0:(len(py_with_thermal.columns)-1)], py_with_thermal['cluster'])
print('the accuracy with thermal data of kmeans in Python is ',silhouette_km_py)

silhouette_km_thermal_py = silhouette_score(py_without_thermal.iloc[:, 0:(len(py_without_thermal.columns)-1)], py_without_thermal['cluster'])
print('the accuracy with no thermal data of kmeans in R is ',silhouette_km_thermal_py)


# Apply silhouette score in the data generate from R (clara)
silhouette_km_r = silhouette_score(r_with_thermal.iloc[:, 0:(len(r_with_thermal.columns)-1)], r_with_thermal['cluster'])
print('the accuracy with thermal data of kmeans in R is ',silhouette_km_r)

silhouette_km_thermal_r = silhouette_score(r_without_thermal.iloc[:, 0:(len(r_without_thermal.columns)-1)], r_without_thermal['cluster'])
print('the accuracy with no thermal data of kmeans in R is ',silhouette_km_thermal_r)



# Apply silhouette score in the data generate from GMM

silhouette_gmm = silhouette_score(multiGDF_clear, gm_y_thermal)
print('the accuracy with thermal data of GMM is ',silhouette_gmm)

silhouette_gmm_without_thermal = silhouette_score(multiGDF_clear_without_thermal, gm_y_without_thermal)
print('the accuracy with no thermal data of GMM is ',silhouette_gmm_without_thermal)


# plot the scores in bar chart

name_list = ['Kmeans (Python)','Clara (R)','GMM (Python)']

with_thermal = [silhouette_km_py , silhouette_km_r, silhouette_gmm]
no_thermal = [silhouette_km_thermal_py ,silhouette_km_thermal_r, silhouette_gmm_without_thermal]


x =list(range(len(with_thermal)))

total_width, n = 1.5, 3
width = 0.3
 
plt.bar(x, with_thermal, width=width, label='with thermal data',fc = 'y')
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, no_thermal, width=width, label='without thermal data',tick_label = name_list,fc = 'g')
plt.legend()
plt.xlabel('Package')
plt.ylabel('Silhouette Score')
plt.title('Clustering Silhouette Scores of Different Methods')
plt.savefig('output/Clustering Silhouette Scores of Different Methods.png')
plt.show()



#%%
'''
Part 3

# This is just for taking a look of how much the silhouette score will be 
# in K means if the K is in range of (2,20)

range_n_clusters = list (range(2,20))
print ("Number of clusters from 2 to 9: \n", range_n_clusters)

for n_clusters in range_n_clusters:
    clusterer = KMeans (n_clusters=n_clusters).fit(scaled_clear_without_thermal)
    preds = clusterer.predict(scaled_clear_without_thermal)
    centers = clusterer.cluster_centers_

    score = silhouette_score (scaled_clear_without_thermal, preds, metric='euclidean')
    print ("For n_clusters = {}, silhouette score is {}".format(n_clusters, score))

'''

# making a loop to find suiteble N with higher silhouette score
# reference: https://gist.github.com/SolClover/b743b226fd2d7e1ffc8cfe66671f32fd

# Create empty list
S=[]

# Range of clusters to try (2 to 10)
K=range(2,50)

# Select data for clustering model

for k in K:
    # Set the model and its parameters
    model = GMM(n_components=k, n_init=20, init_params='kmeans')
    # Fit the model 
    labels = model.fit_predict(multiGDF_clear)
    # Calculate Silhoutte Score and append to a list
    S.append(silhouette_score(multiGDF_clear, labels, metric='euclidean'))


# Plot the resulting Silhouette scores on a graph
plt.figure(figsize=(16,8), dpi=300)
plt.plot(K, S, 'bo-', color='black')
plt.xlabel('k')
plt.ylabel('Silhouette Score')
plt.title('Identify the number of clusters by Silhouette Score (GMM)')
plt.savefig('output/Identify the number of clusters by Silhouette Score (GMM).png')
plt.show()






