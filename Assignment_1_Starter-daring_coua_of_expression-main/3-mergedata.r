# Script to load extracted-elevation.csv and the meuse dataset, 
# combine them into a dataframe, and save it as meuse-extended.csv 
# in the subdirectory output.
# And the extra stuff :)

# Install package
if(!"sp" %in% installed.packages()){install.packages("sp")}
library(sp)

# Extract the elevation from the last task
elev.abs <- read.table(file ='output/extracted-elevation.csv')

# Load the Meuse dataset 
data(meuse)

# Create a dataframe to combine the two elevation
meuseextended <- data.frame(elev.abs, meuse$elev)

# Save it in a csv file, with the column name elev.abs
write.table(meuseextended, file = "output/meuse-extended.csv", row.names=FALSE, 
            col.names = c("elev.abs","meuse.elev"), sep =",",quote=FALSE)

# Extra
# Plot the correlation between Meuse and elevation information from satellites 
plot(meuse$elev,elev.abs[,1])
correlation=cor(meuseextended)[[2]]

# Plot a histogram for height above the sea level
hist(elev.abs[,1], col = "lightblue", border = "pink", 
     main = "Height above the sea level", xlab = "Height in m", ylab = "Frequency")

# Display the correlation to user
if (correlation >= 0.7) {
  sprintf("The two data are correlated at %s, which is high", correlation)
  } else if (correlation < 0.7 & correlation > 0.4) {
    sprintf("The two data are correlated at %s, which is quite different", correlation)
    } else {sprintf("The two data are not correlated (%0.4s)", correlation)}
    #  it could be explain because the relative elevation is calculated relatively to the meuse elevation which not considered
    # as a perfectly horizontal surface. That explain the difference between the relative and the absolute elevation (calculated from the sea level, flat surface)

# Display the correlation height above the sea level to user 
sprintf("The mean height above the sea level is %0.4s", mean(elev.abs[,1]))
