# GALAXY-MERGERS-TFG

<img src="IMAGES/NGC_RGB_1.png?raw=true" alt="drawing" width="350"/>

Máximo Rodríguez Herrero 
Universidad Autónoma de Madrid

## Overview

This observational study of the NGC 5394 and 5395 merging system, conducted with the $2.2m$ telescope of the Calar Alto Observatory (Spain), focused on the system's structure and stellar population. The study confirmed that NGC 5395 is a spiral galaxy, while NGC 5394 is hypothesized to be a barred spiral galaxy, pending further research. The presence of high population I stars and the distortion of the spiral arms in the intermediate region suggest that the galaxies are beginning to merge. Full work available [here](https://github.com/MaximoRdz/GALAXY-MERGERS-TFG/blob/main/GALAXY_MERGERS_MAXIMO.pdf)

The Cafos data is available at `\TFG_EXP_2022`
## Usage

### Object Visibility

Every insight about the object's visibility, air-mass, night-sky path followed etc. is provided by the class ObjectVisibility defined in `visibility.py` and implemented in the notebook `NGC5395_visibility.ipynb`

## Utils in `functions_maxi.py`

- `my_plot` most used plt.imshow 
- `my_plot_log` logarithmic plot
- `cut_master_frames` reshape the frame to fit the science images shape
- `sky_squares_median` compute the sky background median counts
- `sky_histogram` represent the sky median
- `class SkyInteractive` interactively select the area to use to compute the sky median counts
- `class CalibrationStars` interactively select the calibration stars to get the location in the image and its radius

## Data Reduction & Science Results

The project is entirely contained in the notebook `Galaxy_Mergers.ipynb` although some of the functions are defined separately in the file `functions_maxi.py`.

## Table of contents `Galaxy_Mergers.ipynb` 

#### 1. Data Load
#### 2. Alingment to the CCD coordinates
#### 3. Index slicing: Creating the mask for each type of image
#### 4. Master Bias
#### 5. Master Flats
##### 5.1. Median of every exposure and resize the frames if necessary
#### 6. Science Image Reduction
##### 6.1. Sky Substraction `SkyInteractive`
##### 6.2. Final Reduction
###### 6.2.1. H ALPHA
###### 6.2.2. NGC 5395 R
###### 6.2.3. NGC 5395 V
###### 6.2.4. NGC 5395 B
#### 7. Flux Calibration
##### 7.1. Calibration Stars Selection
##### 7.2. CalibrationStars User Guide `CalibrationStars`
##### 7.3. Unit conversion: $mag/arcsec^2$
#### 8. Stellar Composition Analysis
#### 9. Color Image
#### 10. Structural Comparissons


