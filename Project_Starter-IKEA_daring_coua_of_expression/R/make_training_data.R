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

# This function takes in the dataframe of the segmented individual tree polygons, 
# which included tree heights, and added the data from both thermal and multispectral 
# bands to it, and returns the new dataframe. 

make_training_data <- function(tree_polygons_path) {
  
  # if (!"terra" %in% installed.packages()) {install.packages("terra")}
  # if (!"sf" %in% installed.packages()) {install.packages("sf")}
  # if (!"dplyr" %in% installed.packages()) {install.packages("dplyr")} 
  # library(terra)
  # library(sf)
  # library(dplyr)
  if (!file.exists(tree_polygons_path)){return(print("The folder used in the make_training_data function doesn't seem to exist, try another path")) }
  
  tree_polygons <- st_read(tree_polygons_path)
  # Import data from folder
  multispectral <- rast("data/Multispectral.tif")
  thermal <- rast("data/Thermal.tif")

  # Extract data from polygon (mean function)
  thermal_mean <- thermal %>%
                  terra::rasterize(tree_polygons, ., field = "ID") %>%
                  terra::zonal(thermal, ., fun = "mean", na.rm = TRUE) %>%
                  dplyr::select(-Thermal_4)   # remove band 4 as it is not useful (according to metadata)

  multispectral_mean <- multispectral %>%
                      terra::rasterize(tree_polygons, ., field = "ID") %>%
                      terra::zonal(multispectral, ., fun = "mean", na.rm = TRUE)

  training_data <- thermal_mean %>%
                  dplyr::inner_join(multispectral_mean, by = "ID") %>%
                  dplyr::inner_join(tree_polygons, by = "ID") %>%
                  dplyr::select(-ID, -X, -Y, -CA_m2)  # remove unnecessary columns
  
  # Shorten the column names
  names(training_data)[1:8] <- c('Thrml1', 'Thrml2', 'Thrml3', 'Mltsp1', 
                                 'Mltsp2', 'Mltsp3', 'Mltsp4', 'Mltsp5')
  
  # Convert the dataframe to an sf.dataframe
  training_data <- st_transform(st_set_geometry(training_data, "geometry"), st_crs(tree_polygons))
  
  # Export data as shapefile so it can be read by the Python script in the next step (to determine K)
  st_write(training_data, "data/training_data.shp", driver = "ESRI Shapefile", delete_dsn = TRUE)
  
  return(training_data)
}