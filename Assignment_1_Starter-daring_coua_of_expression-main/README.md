# Assignment 1: Bash and R integration

## Your task
You are curious about whether we can use global datasets for local applications. To that end, you want to compare elevation data collected in fieldwork with elevation data derived from satellite altimetry.

You have a dataset collected in the Netherlands that contains measured elevation relative to local river level in R (`data(meuse)` will add a data.frame `meuse` into your environment as long as the `sp` package is loaded, see `?meuse` for more info). In addition, you can get elevation information from satellites that provides absolute height above sea level from `https://github.com/GeoScripting-WUR/IntroToRaster/releases/download/meuse-elevation/assignment_1_elevation.zip`. Your goal is to extract the absolute elevation from the satellite data at the measured locations from the fieldwork, so that you can compare the two datasets.


## Requirements
Create a project that includes three scripts:

1. An R script that downloads the information and saves it. The output from the script should be a file `elevation.tif` that contains downloaded elevation data, and a file `locations.csv` that contains the locations at which to extract the elevation information, both in the subdirectory `data`. Place any functions that you create in the subdirectory `R`.
2. A Bash script that runs `gdallocationinfo` on the `elevation.tif` file by iterating through the entries of the `locations.csv` file to extract the elevation values, and also remove unnecessary lines. Save the result as `extracted-elevation.csv` in the `output` subdirectory.
3. An R script that loads the `extracted-elevation.csv` file and the `meuse` dataset again, and then combines the two into a single data.frame. Call the new column `elev.abs`. Save the result (the `meuse` dataset + the `elev.abs` column) as a comma-separated file `meuse-extended.csv` in the subdirectory `output`. Place any functions that you create in the subdirectory `R`.

Note that, contrary to previous exercises, you should not have to make any adjustments to the Bash script `main.sh`. It simply runs each of the three scripts in order.

Make sure to use Git effectively to collaborate between both team members, document your script well, and keep to the project structure as outlined above. Don't forget to add a software license.

After the submission deadline, do not forget to review the work of the other teams that you need to review. The review is part of your grade for the assignment, so make sure you provide valuable feedback!


## Hints
* See `?write.table`, `?read.table` and `?write.csv` to create a CSV file that has only coordinates separated by spaces and without a table header, and later to read a table that is also separated by spaces, and finally write a comma-separated file.
* The Meuse dataset is using the RD New coordinate system, which has the code EPSG:28992.
* You can iterate through the CSV file either by using a Bash loop, or by feeding the `gdallocationinfo` process using a pipe and standard input.
* Study the [GDALLocationInfo manual page](https://gdal.org/programs/gdallocationinfo.html) well.
* You can save output from a Bash command into a file with a redirect operator `>`, i.e. `gdallocationinfo utm.tif 256 256 > extracted-values.txt`.
* `grep` can be used to keep only the desired lines in the output. See `man grep`.


## Extra
If you are finished with all of the tasks above and curious about the actual result, in the third script you can plot the two values against each other using `plot(elev~elev.abs, data=meuse.extended)` (replace `meuse.extended` with the name of the variable containing the extended meuse dataset), and find the correlation between the two values with `cor()` and `summary(lm())`. Do they correlate well? What is the height above sea level of the river Meuse at the study site? See `mean()` and `hist()`.
