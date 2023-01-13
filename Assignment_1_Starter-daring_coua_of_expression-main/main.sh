#!/bin/bash
# Geoscripting 2023
# Assignment 1
# daring_coua_of_expression
# 13/01/2023

# Run all three parts of the assignment one by one

# Script to download the information and save it in the data subdirectary.
Rscript 1-getdata.r

# Script to extract the elevation values from extract the elevation values in 
# elevation.tif and save it as extracted-elevation.csv in the output subdirectory.
bash 2-extractdata.sh

# Script to load extracted-elevation.csv and the meuse dataset, 
# combine them into a dataframe, and save it as meuse-extended.csv 
# in the subdirectory output.
# Extra: create plot and histogram, show the correlation and mean height above sea level
Rscript 3-mergedata.r

# Extra: open plot and histogram
xdg-open Rplots.pdf