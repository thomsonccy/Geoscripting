# Script to download data and save information to locations.csv

# Load the required function
source("R/WriteElevation.r")

# Install package
if(!"sp" %in% installed.packages()){install.packages("sp", quiet = TRUE)}
library(sp)

# Use the function created to download and unzip 
WriteElevation()

# Take the locations from the Meuse dataset
data(meuse)
location_meuse=data.frame(meuse$x,meuse$y)

# Save the locations in a csv file
write.table(location_meuse, file = "data/locations.csv", row.names = FALSE, 
            quote = FALSE, col.names = FALSE)