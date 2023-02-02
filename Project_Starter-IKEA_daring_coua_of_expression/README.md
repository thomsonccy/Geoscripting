# Geoscripting project proposal
* Title: Unsupervised tropical tree species classification using UAV imagery
* Team: IKEA + daring_coua_of_expression
* Number of the topic chosen: 2
* Objective: Classify tropical tree species in a given UAV image based on its corresponding multispectral data and canopy height model (CHM) data. 

## Task 1: Why
Identification of tree species is essential for forest conservation management and conducting biodiversity studies connected to forestry. Space4Good and Masarang Foundation intend to map and count the different tree species in Indonesia using UAV data. However, tropical forests cover large areas and are dense and mixed with different trees species, making it difficult to perform the task through human efforts alone. A machine-learning based solution is needed to classify the tree species based on the UAV data.   

## Task 2: What
* Link to data (Google Drive): https://drive.google.com/drive/folders/15WlbT6ZWsYhH8sM6_9_vlljqYAd-2PRe
* Access method: You can choose either to directly download the data from the drive (and put them in the data folder). 
* Data size: three TIF files, about 100 MB in total. 

### Data description (copied from metadata): 

#### Canopy Height Model (CHM.tif)
The CHM describes the height of the trees in the plot.
The units are in meters, thus the ground floor of the forest is set to 0 meters.
The highest tree in the plot is around 60+ meters.
The spatial resolution is 1 metre.

#### Multispectral Image (Multispectral.tif)
This image is comprised of 5 bands: Blue, Green, Red, Red-Edge, NIR.
The values on each band have not been normalized.
A linear normalization could help bring the values to a range between 0 and 255.
The spatial resolution is ~0.1205 metre.

#### Thermal Image (Thermal.tif)
The thermal image consists of four bands. 
Band 4 is a generated output from the processing software that includes no useful information.
Bands 1 to 3 display the heat eminating from the source, so red = hot, green = cold.
The spatial resolution is ~0.2431 metre.

## Task 3: How

After downloading all the data and set up R and python environment (conda environement with clustering.yaml), the first step is to use ITC delineation approach to find local maxima within a rasterized canopy height model (CHM), designates these as tree tops, then uses a decision tree method to grow individual crowns around the local maxima. A data frame of the segmented individual tree polygon is therfore created including the CHM in which we add the thermal and the multispectral images.

After this we apply an unsupervised machine learning algorithm. The algorithm will cluster the grids in the image based on the similarity of their pattern compared to other grids' values. We decided to compare three different method of clustering: clara, Kmeans,Gaussian Mixture Models. 

We also determine the optimal number of clusters (number of tree species). For Kmeans, we use the Elbow Method to find the suiteble point. For GMM, we create a loop to find the point where has the lowest AIC and BIC.

Due to the lack of validation data, we use Silhouette scores for unsupervised machine learning to evaeluate the quality of the cluster and make comperation among different method.

Finally we plot the result in a map, that represent the clusters and therefore the different tree species.

### Output

* Images [.png]  -> shows the optimal number of clusters in Kmeans.

* Images [.png]  -> shows the optimal number of clusters in GMM.

* Images [.png]  -> shows the Silhouette Score among Kmeans, Clara and GMM.

* 6 maps for visualisation [.png] -> shows the resulted image with a legend indicating the different clusters. 

* Python Script(s) -> the script(s) employed to run step 4

* R Scripts -> the scripts employed to run the main and combine all the step including the python script.

### Steps to run this project

1. Clone this project to your local home directory

2. Run the bash script "ikea_coua.sh" (use chmod u+x)

    - chmod u+x ikea_coua.sh  # Gives user execute permissions
    - ./ikea_coua.sh # run the script
    
    The script will 

    - create a conda environment using "ikea_coua.yaml" file
    - open the R project in Rstudio

3. Open main.R or main_notebook.Rmd from the project, which will open the R script or R notebook respectively

4. Run the R script or R notebook depending on your preferences

### Steps in the R script

1.  Download data from Google Drive
    (https://drive.google.com/drive/folders 15WlbT6ZWsYhH8sM6_9_vlljqYAd-2PRe)

2.   Find individual tree crowns using CHM.tif
    - Find the threshold minimum tree height
    - Apply itcSegment package to segments the individual trees as polygons
    - Create a dataframe containing the polygons, which includes the tree heights.

3.  Create the data frame of the segmented individual tree polygon which contain CHM, Thermal Image, Multispectral.

4. Python script: Generate 2 clusters of trees:

    - Perform standardization by centering and scaling
    - Determine the optimal number of clusters (K) 
    - Apply two different clustering method: the Kmeans, Gaussian Mixture Models clustering
    - Validation for the three cluster data with Silhouette Score

5. Kmeans clustering to generate a cluster of trees with clara package.

6. Visualisation of the classify tropical tree species with all the cluster method.



### Possible Changes

- Find better packages to improve the identification of tree canopy, eg. Spatial Wavelet Analysis
- Figure out the problem of negetive Silhouette Scores in GMM
- Improve the accuracy of the three algorithm



### References

Wang, Sherrie, George Azzari, and David B. Lobell. "Crop type mapping without field-level labels: Random forest transfer and unsupervised clustering techniques." Remote sensing of environment 222 (2019): 303-317.

Schäfer, Elisa, et al. "Mapping tree species diversity of a tropical montane forest by unsupervised clustering of airborne imaging spectroscopy data." Ecological indicators 64 (2016): 49-58.


