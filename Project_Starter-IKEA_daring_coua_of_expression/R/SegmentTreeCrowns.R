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

# This function takes in the path of a CHM .tif, reads it in as a raster, finds
# the threshold tree height (m) at the position of the input percentile (default 
# is 0.05, i.e. the 5th percentile), and segments the individual trees as polygons. 
# The function returns the dataframe of the polygons, which includes the tree heights. 

SegmentTreeCrowns <- function(chm_path, percentile = 0.05){

  # # Uncomment this chunk if use this function separately from the main script
  # ##############################
  # # Install necessary packages and load them
  # if(!"sf" %in% installed.packages()) {install.packages("sf")}
  # if(!"terra" %in% installed.packages()) {install.packages("terra")}
  # if (!"itcSegment" %in% installed.packages()) {install.packages("itcSegment")}
  # library(sf)
  # library(terra)
  # library(itcSegment)
  # ##############################

  # Load CHM as data frame
  chm <- rast(chm_path)
  CHM_df <- as.data.frame(chm, xy = TRUE)

   # Find the threshold tree height at given percentile
  threshold <- global(chm, fun = function(x) {stats::quantile(x, probs = c(percentile), na.rm = TRUE)})[1, 1]

  # Individual Tree Crowns segmentation with LiDAR data
  tree_poly <- st_as_sf(itcLiDAR(X = CHM_df$x, Y = CHM_df$y,
                                 Z = CHM_df$CHM, epsg = 32750,
                                 resolution = 1, MinSearchFilSize = 3,
                                 MaxSearchFilSize = 9, TRESHSeed = 0.35, cw=3,
                                 TRESHCrown = 0.35, minDIST = 30, maxDIST = 100,
                                 HeightThreshold = threshold), crs = "EPSG:32750")
  
 

  # Write polygons as shapefile 
  st_write(tree_poly, "data/Tree_Segmentation_Polygons.shp", driver = "ESRI Shapefile", delete_dsn = TRUE)
  
  return(tree_poly)
}
