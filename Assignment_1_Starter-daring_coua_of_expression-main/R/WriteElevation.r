# Function to download data and delete zip file

WriteElevation <- function() {
  # Download file from url and save as file argument
  file_url <- "https://github.com/GeoScripting-WUR/IntroToRaster/releases/download/meuse-elevation/assignment_1_elevation.zip"
  file_name <- "data/location.zip"
  
  # Check if the directory and file exist already
  if (!dir.exists("data")) {dir.create("data")}
  if (!dir.exists("output")) { dir.create("output")}
  if (!file.exists(file_name)) {download.file(url = file_url, destfile = file_name)}
  
  # Unzip the file
  unzip("data/location.zip", exdir = "data")
  
  # Delete zip file
  unlink("data/location.zip")
}
