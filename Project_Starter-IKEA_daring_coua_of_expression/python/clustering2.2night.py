# 
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



'''
step1

- Apply K means for tree species clustering in both dataset:
  1. the data with thermal part
  2. the data without thermal part
  
- Rescale the both data set

- Find suitebale K by using the elbow curve method and print the curve out
  as two png images and see whether the K will be different based on different 
  data set (acctually, they are same)
 

- Get the identification of tree species


- Output the geoJson file named 'clustring_result.geojson'


'''


# read file from the data folder
multiGDF = gpd.read_file('data/training_data.shp')



# drop the unneccessary columns
# here we try two methods in clustring, the one including the thermal data, and another one we drop it
multiGDF_clear = multiGDF.drop(columns=['geometry'])
multiGDF_clear_without_thermal = multiGDF.drop(columns=['geometry','Thrml1','Thrml2','Thrml3'])



# rescale the data to get better result
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()

# the same idea in both data (1. the data with thermal part, 2.the data without thermal part
scaler.fit(multiGDF_clear) 
scaled_multiGDF_clear = scaler.transform(multiGDF_clear)

scaler.fit(multiGDF_clear_without_thermal) 
scaled_clear_without_thermal = scaler.transform(multiGDF_clear_without_thermal)



# try to find the suitable K for K means by using the elbow curve method
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
'''

step2

- Apply Gaussian mixture model (GMM) for tree species clustering in both dataset:
  1. the data with thermal part
  2. the data without thermal part
  
- the data do not need reseacle


- try to find the suitable n components by minimized BIC and AIC, 
  but it doesn't show a very clear point, 
  so we use the same 'n' as it in step1  
 

- Get the identification of tree species


'''


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


# add the new column in the original data set
multiGDF['GMM_clustring'] = gm_y_thermal
multiGDF['GMM_clustring_without_thermal'] = gm_y_without_thermal



#%%
'''
step3

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


from sklearn import datasets
from sklearn.metrics import silhouette_samples,silhouette_score

# calculate Silhouette Score to check how good the clustering it is 
# reference: https://www.guavus.com/technical-blog/unsupervised-machine-learning-validation-techniques/


# Apply silhouette score in the data generate from K means

silhouette_km = silhouette_score(scaled_clear_without_thermal, y_without_thermal)
print('the accuracy with thermal data of kmeans in python is',silhouette_km)

silhouette_km_thermal = silhouette_score(scaled_multiGDF_clear, y)
print('the accuracy with no thermal data of kmeans in python is',silhouette_km_thermal)




#################   unfinished   #####################################
# Apply silhouette score in the data generate from R(clara)

r = gpd.read_file('output/Polygons_clustered_Kmeans_with_Thermal.shp')
r
r_without_thermal = gpd.read_file('output/Polygons_clustered_Kmeans_without_Thermal.shp')


# the same idea in both data (1. the data with thermal part 2.the data without thermal part
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

r_copy = r
r_copy_without_thermal = r_without_thermal

r_copy = r_copy.drop(columns=['geometry','cluster'])
r_copy_without_thermal = r_copy_without_thermal.drop(columns=['geometry','Thrml1','Thrml2','Thrml3','cluster'])



scaler.fit(r_copy) 
scaled_r = scaler.transform(r_copy)


scaler.fit(r_copy_without_thermal) 
scaled_r_without_thermal = scaler.transform(r_copy_without_thermal)


silhouette_km_r = silhouette_score(scaled_r, r['cluster'])
print('the accuracy with thermal data of kmeans in R is ',silhouette_km_r)


silhouette_km_thermal_r = silhouette_score(scaled_r_without_thermal, r_without_thermal['cluster'])
print('the accuracy with no thermal data of kmeans in R is ',silhouette_km_thermal_r)



# Apply silhouette score in the data generate from GMM

silhouette_gmm = silhouette_score(multiGDF_clear, gm_y_thermal)
print('the accuracy with thermal data of GMM is ',silhouette_gmm)

silhouette_gmm_without_thermal = silhouette_score(multiGDF_clear_without_thermal, gm_y_without_thermal)
print('the accuracy with no thermal data of GMM is ',silhouette_gmm_without_thermal)




#%%
'''
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
#%%

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
plt.title('Identify the number of clusters using Silhouette Score')
plt.show()
















'''
# plot the identification of the tree species
multiGDF.plot( column = 'clustring' )
plt.legend()
plt.title('Clustering Result of Tree Species\n(with thermal data)')




multiGDF.plot( column = 'clustring_without_thermal',legend=True, cmap='tab20')
plt.legend()
plt.title('Clustering Result of Tree Species\n(without thermal data)')


'''
