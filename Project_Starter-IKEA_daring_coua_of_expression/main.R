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
# Final Project
# Challenge 2 - Tree Species Classification using UAV Imagery
# Team: IKEA Coua

#### Step 1 - Download data and create directories ####

# Import function scripts
source("R/make_directories.R")

# Use the function to make data and output directories
make_directories()

# ATTENTION: 
# After creating the directories, we need to manually download data from Google Drive
# and save them in the 'data' folder before proceeding further.

####---------------------------------------------------------------


#### Step 2 - Find individual tree crowns ####

# Install and load packages
if(!"sf" %in% installed.packages()) {install.packages("sf")}
if(!"terra" %in% installed.packages()) {install.packages("terra")}
if (!"itcSegment" %in% installed.packages()) {install.packages("itcSegment")}
library(sf)
library(terra)
library(itcSegment)

# Import function scripts
source("R/SegmentTreeCrowns.R")

# Find the path to CHM.tif
## Update it to search masked at the end
chm_path <- list.files(path = "data/", pattern = glob2rx("CHM.tif"), full.names = TRUE)

# Use the function to create the masked CHM.tif
tree_polygons <- SegmentTreeCrowns(chm_path)

####---------------------------------------------------------------


#### Step 3 - Combine mean of multispectral and thermal value with polygons to make training data ####

# Install and load packages
if (!"dplyr" %in% installed.packages()) {install.packages("dplyr")}
library(dplyr)

# if (!"terra" %in% installed.packages()) {install.packages("terra")}
# if (!"sf" %in% installed.packages()) {install.packages("sf")}
# library(terra)
# library(sf)

# Import function scripts
source("R/make_training_data.R")

# Generate dataframe that includes all band information and tree height

tree_polygons_path <- "data/Tree_Segmentation_Polygons.shp"

training_data <- make_training_data(tree_polygons_path)

####---------------------------------------------------------------


#### Step 4.1 - Cluster the polygons via KMeans with python ####

# This step will be done in Python. The result plot is saved in folder 'output'.

# Install and load packages to use python functions in R
if (!require("reticulate", character.only = TRUE)) {
  install.packages("reticulate")
  require("reticulate", character.only = TRUE)
}
library(reticulate)

# Use the conda environment "clustering" that was created when running ikea_coua.sh
use_condaenv("clustering")

# Run the python scripts
py_run_file("python/functions/cluster_polygons_KMeans.py")

# Based on the derived graph, the best K equals to 5
K <- 5

####---------------------------------------------------------------

#### Step 4.2 - Cluster the polygons via KMeans with R ####

# Install and load packages
if (!"cluster" %in% installed.packages()) {install.packages("cluster")}
library(cluster)

# if(!"terra" %in% installed.packages()){install.packages("terra")}
# if(!"sf" %in% installed.packages()){install.packages("sf")}
# library(terra)
# library(sf)

# Import function scripts
source("R/ClusterPolygons.R")

# Use the function to cluster the polygons with the derived best K

training_data_path <- "data/training_data.shp"
ClusterPolygons(training_data_path, K = K, withThermal = FALSE)
ClusterPolygons(training_data_path, K = K, withThermal = TRUE)

####---------------------------------------------------------------


#### Step 4.3 Clustering with GMM and calculate silhouette values
py_run_file("python/GMM_clustering_and_silhouette_values_calculation.py")

####---------------------------------------------------------------

#### Step 5 - Visualize the clusters ####

# Install and load packages
if (!"ggplot2" %in% installed.packages()) {install.packages("ggplot2")}
library(ggplot2)

# Import function scripts
source("R/VisualiseClusters.R")

# Visualize the clusters
VisualiseClusters(path="output/Python_Polygons_clustered_Kmeans_with_Thermal.shp")
VisualiseClusters(path="output/Python_Polygons_clustered_Kmeans_without_Thermal.shp")
VisualiseClusters(path="output/Python_Polygons_clustered_GMM_with_Thermal.shp")
VisualiseClusters(path="output/Python_Polygons_clustered_GMM_without_Thermal.shp")
VisualiseClusters(path="output/Python_Polygons_clustered_Kmeans_with_Thermal.shp")
VisualiseClusters(path="output/Python_Polygons_clustered_Kmeans_without_Thermal.shp")

####---------------------------------------------------------------

