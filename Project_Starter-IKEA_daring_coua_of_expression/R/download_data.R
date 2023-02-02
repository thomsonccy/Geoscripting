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

# This function downloads the UAV imagery data from Google Drive. 

download_data <- function() {
  
  # # Install package to download data
  # if (!"googledrive" %in% installed.packages()) {install.packages("googledrive")}
  # library(googledrive)

  url_chm <- "https://drive.google.com/file/d/1GEcclCfwj89ADj07ufB7TT1eIbj8k35r"
  url_multispectral <- "https://drive.google.com/file/d/10RGT18lGckzY59w1qDNxUVYGIMxS-KqP"
  url_thermal <- "https://drive.google.com/file/d/1eywPSRIadMMm3obWkDpnHvq3aaRnNhBU"

  # Download CHM, Multispectral, and Thermal images
  if (!file.exists("data/CHM.tif")) {
    drive_download(url_chm, "data/CHM.tif")
  }

  if (!file.exists("data/Multispectral.tif")) {
    drive_download(url_multispectral, "data/Multispectral.tif")
  }

  if (!file.exists("data/Thermal.tif")) {
    drive_download(url_thermal, "data/Thermal.tif")
  }
}
