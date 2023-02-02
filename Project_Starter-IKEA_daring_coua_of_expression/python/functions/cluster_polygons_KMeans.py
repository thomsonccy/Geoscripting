#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Geoscripting 2023
# Final Project
# Challenge 2 - Tree Species Classification using UAV Imagery
# Team: IKEA Coua

"""
# Import necessary modules
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


def find_best_K( tree_polygons_path, with_thermal ):
    '''
    Takes in the file path of the shapefile of which the attribute table contains 
    geometry of the segmented tree polygons, values from multispectral and thermal 
    bands, and CHM. The function calculates the inertia value of a range of K for 
    the KMeans clustering method, and outputs a plot of inertia values for different
    K's in the 'output' folder. 
    
    Note that the user needs to check the image and use the elbow curve method to find the 
    best K before continuing the next step. 

    Parameters
    ----------
    tree_polygons_path : str
        File path of the tree polygons with band values and CHM.
    with_thermal : boolean
        Whether we include the thermal band values when performing clustering. 

    Returns
    -------
    polygonsGDF : GeoDataFrame
        Dataframe of the input tree polygons. 
    polygonsDF_normalised : DataFrame 
        Normalised data of the band values and CHM. 

    '''
    # Ensure with_thermal is a boolean
    if type( with_thermal ) != bool: 
        print("Please enter only 'True' or 'False' for the parameter with_thermal.")
        return
        
    # Read file according to path
    polygonsGDF = gpd.read_file(tree_polygons_path)

    # Drop unneeded columns and save in a new dataframe
    if with_thermal: 
        polygonsDF = polygonsGDF.drop( columns = ['geometry'] )
        title = 'Elbow Method for Finding Optimal K (with thermal data)'
    else: 
        polygonsDF = polygonsGDF.drop( columns = ['geometry','Thrml1','Thrml2','Thrml3'] )
        title = 'Elbow Method for Finding Optimal K (without thermal data)'

    # Normalise the data with min-max method to have optimal clustering results
    #### Reference: code from WUR course Data-driven Supply Chain
    scaler = MinMaxScaler()
    scaler.fit( polygonsDF )
    polygonsDF_normalised = pd.DataFrame( scaler.transform( polygonsDF ), columns = polygonsDF.columns.values.tolist())

    # Find the most suitable K for K means by using the elbow curve method
    #### Reference: https://www.analyticsvidhya.com/blog/2021/05/k-mean-getting-the-optimal-number-of-clusters/
    inertia = []
    Kvalues = []
    for K in range(1, 31) :
        Kvalues.append(K)
        kmeans = KMeans(n_clusters = K)
        kmeans.fit( polygonsDF_normalised )
        inertia.append( kmeans.inertia_ )
 
    # Plot and output the figure 
    # K value at the elbow point equals to 5
    output_str = 'output/' + title + '.png'
    plt.plot( Kvalues, inertia,'bx-' )
    plt.xlabel('K Values') 
    plt.ylabel('Inertia') 
    plt.title( title )
    plt.savefig( output_str )
    plt.show()
    
    print( 'The image has been saved as ' + output_str )
    
    return polygonsGDF, polygonsDF_normalised



def cluster_polygons_KMeans( tree_polygons_path, with_thermal, K = 5 ): 
    '''
    Takes in the file path of the shapefile of which the attribute table contains 
    geometry of the segmented tree polygons, values from multispectral and thermal 
    bands, and CHM. The function clusters the polygons based on the given K by  
    the KMeans clustering method, and outputs a shapefile with the input data 
    and the clustering result in the 'output' folder. 

    Parameters
    ----------
    tree_polygons_path : str
        File path of the tree polygons with band values and CHM.
    with_thermal : boolean
        Whether we include the thermal band values when performing clustering. 
    K: int
        Number of clusters to be performed via KMeans method. Default is 5. 

    Returns
    -------
    None.

    '''
    # Find K via graph and get the normalised data
    polygonsGDF, polygonsDF_normalised = find_best_K(tree_polygons_path, with_thermal)
    
    # Perform KMeans
    #### Reference: code from WUR course Data-driven Supply Chain
    kmeans = KMeans(n_clusters = K)
    prediction = kmeans.fit_predict( polygonsDF_normalised )
    polygonsGDF['cluster'] = prediction
    polygonsDF_normalised['cluster'] = prediction
    
    
    # Output the polygons with clustering result 
    
    if with_thermal: 
        shp_fn = 'output/Python_Polygons_clustered_Kmeans_with_Thermal.shp'
        csv_fn = "output/Python_KMeans_Normalised_Polygon_data_with_Thermal.csv"
    else: 
        shp_fn = 'output/Python_Polygons_clustered_Kmeans_without_Thermal.shp'
        csv_fn = "output/Python_KMeans_Normalised_Polygon_data_without_Thermal.csv"
        
    polygonsGDF.to_file( filename = shp_fn, driver = 'ESRI Shapefile' )

    print( 'The shapefile has been saved as ' + shp_fn )
    
    polygonsDF_normalised.to_csv( csv_fn, index = False )



def main(): 
    
    cluster_polygons_KMeans(tree_polygons_path = 'data/training_data.shp', with_thermal = True)
    cluster_polygons_KMeans(tree_polygons_path = 'data/training_data.shp', with_thermal = False)
    
    

if __name__ == "__main__": 
    main()