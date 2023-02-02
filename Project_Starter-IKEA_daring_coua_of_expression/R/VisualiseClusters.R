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

# This function takes in the polygons' dataframe, which includes values from multispectral 
# bands, CHM, and the resulted clusters from the previous step. It then graphs the polygons 
# based on their clusters (default number of clusters K=5) and outputs the map as a PNG. 
# The user can choose whether the result of the image includes the thermal bands or not. 
# The function does not return anything. 

VisualiseClusters <- function(path, K = 5){
  

  # Install necessary packages and load them
   if(!"ggplot2" %in% installed.packages()){install.packages("ggplot2")}
   if(!"sf" %in% installed.packages()){install.packages("sf")}
   library(ggplot2)
   library(sf)
  # ##############################
    polygons_clustered_df= st_read(path)
  

    fn <- paste0(gsub(".*[/\\\\](.*)\\..*", "\\1", path),".png")
    
    title <-"Tree Species Clustering "
    

    
  
  # Plot the clusters
  #### Reference 1: https://geocompr.robinlovelace.net/adv-map.html
  #### Reference 2: https://datacarpentry.org/semester-biology/materials/spatial-data-plot-projections-R/
  #### Reference 3: https://www.statology.org/ggplot-font-size/
  clusters <- ggplot(data = polygons_clustered_df, aes(fill = cluster)) + 
    geom_sf() +
    ggtitle(title, subtitle = paste0("Method: KMeans (K = ", K, ")")) + 
    theme(plot.title = element_text(size = 12), 
          axis.text = element_text(size = 7)) + 
    coord_sf(datum = sf::st_crs(polygons_clustered_df))  # reproject the map to UTM 50S
  
  ggsave(plot = clusters, filename = paste0('output/', fn), 
         width = 1600, height = 1300, units = "px")
  
  paste0("The image ", fn, " has been exported successfully. ")
}