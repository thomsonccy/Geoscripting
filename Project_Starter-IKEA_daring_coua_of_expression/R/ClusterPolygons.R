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

# Geoscripting 2023
# Final Project - Challenge 2
# Team: IKEA Coua

# This function takes in a dataframe of the polygons of segmented individual trees,
# uses K-means to cluster the polygons into K groups (default K=5) based on the
# spectral and canopy height property of each polygon, outputs a geojson file of
# the clustered polygons, and returns the dataframe of the clustered polygons.

ClusterPolygons <- function(polygons_path, K = 5, withThermal = c(TRUE, FALSE)) {
  
  # # Uncomment this chunk if use this function separately from the main script
  # ##############################
  # # Install necessary packages and load them
  # if(!"terra" %in% installed.packages()){install.packages("terra")}
  # if(!"sf" %in% installed.packages()){install.packages("sf")}
  # if(!"cluster" %in% installed.packages()){install.packages("cluster")}
  # library(terra)
  # library(sf)
  # library(cluster)
  # ##############################
  
  # Make sure the polygon file exists
  if (!file.exists(polygons_path)){
    stop("The folder used in the make_training_data function doesn't seem to exist, try another path") 
  } else {
    polygons <- st_read(polygons_path)
  }
  
  # Define parameters based on whether or not to consider thermal bands
  if(!withThermal){
    polygons_subset <- st_set_geometry(polygons[4:(ncol(polygons)-1)], NULL)  # keep only the columns of multispectral bands and height
    shp_fn <- "R_Polygons_clustered_Kmeans_without_Thermal.shp"
    csv_fn <- "R_KMeans_Normalised_Polygon_data_without_Thermal.csv"
  } else {
    polygons_subset <- st_set_geometry(polygons, NULL)      # keep all columns except geometry
    shp_fn <- "R_Polygons_clustered_Kmeans_with_Thermal.shp"
    csv_fn <- "R_KMeans_Normalised_Polygon_data_with_Thermal.csv"
  }
  
  # Normalise data before performing KMeans clustering
  #### Reference 1: https://stats.stackexchange.com/questions/21222/are-mean-normalization-and-feature-scaling-needed-for-k-means-clustering
  #### Reference 2: https://stackoverflow.com/questions/44050028/min-max-scaling-normalization-in-r-for-train-and-test-data
  
  polygons_subset <- as.data.frame(apply(polygons_subset, MARGIN = 2, 
                                         FUN = function(x, na.rm = TRUE) (x-min(x))/(max(x)-min(x))))
  
  # Cluster the polygons by KMeans
  #### Reference 1: https://www.datanovia.com/en/lessons/clara-in-r-clustering-large-applications/
  #### Reference 2: https://github.com/csog/r-tutorial/blob/master/Clustering/Clustering-Examples-k-means-PAM-CLARA.R
  
  set.seed(33806)  # make sure the clustering result is reproducible
  
  clara_result <- clara(polygons_subset, k = K, metric = "manhattan",
                        samples = nrow(polygons), sampsize = nrow(polygons),
                        pamLike = TRUE, correct.d = TRUE, rngR = TRUE)
  
  # Add the clusters back to the original polygons' dataframe
  polygons_clustered_df <- cbind(polygons, cluster = as.factor(clara_result$cluster))
  
  # Output the clustered polygons as a shapefile
  st_write(polygons_clustered_df, dsn = paste0("output/", shp_fn),
           quiet = TRUE, delete_dsn = TRUE, driver = "ESRI Shapefile")  # allow overwrite
  
  # Also output the data used for clustering and the clustering result as a CSV
  write.table(cbind(polygons_subset, cluster = as.factor(clara_result$cluster)), 
              file = paste0("data/", csv_fn), row.names = FALSE)
  
  return(polygons_clustered_df)
  
}