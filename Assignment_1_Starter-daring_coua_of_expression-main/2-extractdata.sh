#!/bin/bash
# Script to pass the coordates in locations.csv to elevation.tif using
# gdallocationinfo to extract the elevation values in elevation.tif.
# Save the result as extracted-elevation.csv in the output subdirectory.

# Create variables for the files
tif_file=data/elevation.tif
csv_file=data/locations.csv
temp_tif=data/temp.tif
temp_csv=data/temp.csv
outdir="output"
outtif="extracted-elevation.csv"

# Reproject elevation.tif from RD New coordinate system to WGS84 
# Save it as temp.tif
gdalwarp -s_srs "EPSG:4326" -t_srs "EPSG:28992" $tif_file $temp_tif

# Feed gdallocationinfo process using a pipe to iterate through locations.csv
# Save the result as temp.csv
cat $csv_file | gdallocationinfo -geoloc $temp_tif > $temp_csv

# Use grep to remove unnecessary lines (Report, Location, Band) and the string "Value:"
# Save the result as as extracted-elevation.csv 
grep -v -e "Report" -e "Band" -e "P" -e '^[[:space:]]*$' $temp_csv | cut -d: -f2- > $outdir/$outtif

# Remove temporary files
rm $temp_tif $temp_csv
