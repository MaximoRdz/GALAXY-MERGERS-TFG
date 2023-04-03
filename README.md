# GALAXY-MERGERS-TFG

<img src="IMAGES/NGC_RGB_1.png?raw=true" alt="drawing" width="350"/>

Máximo Rodríguez Herrero 
Universidad Autónoma de Madrid

## Overview

This observational study of the NGC 5394 and 5395 merging system, conducted with the $2.2m$ telescope of the Calar Alto Observatory (Spain), focused on the system's structure and stellar population. The study confirmed that NGC 5395 is a spiral galaxy, while NGC 5394 is hypothesized to be a barred spiral galaxy, pending further research. The presence of high population I stars and the distortion of the spiral arms in the intermediate region suggest that the galaxies are beginning to merge.

## Usage

### Object Visibility

Every insight about the object's visibility, air-mass, night-sky path followed etc. is provided by the class ObjectVisibility defined in `visibility.py` and implemented in the notebook `NGC5395_visibility.ipynb`

## Data Reduction & Science Results

The project is entirely contained in the notebook `Galaxy_Mergers.ipynb` although some of the functions are defined separately in the file `functions_maxi.py`.

### Table of contents `Galaxy_Mergers.ipynb` 

#### Data Load
#### Alingment to the CCD coordinates
#### Index slicing: Creating the mask for each type of image
#### Master Bias
#### Master Flats
##### Median of every exposure and resize the frames if necessary
#### Science Image Reduction
##### Sky Substraction
##### Final Reduction
###### H ALPHA
###### NGC 5395 R
###### NGC 5395 V
###### NGC 5395 B
#### Flux Calibration
##### Calibration Stars Selection
##### CalibrationStars User Guide `CalibrationStars`
##### Unit conversion: $mag/arcsec^2$
#### Stellar Composition Analysis
#### Color Image
#### Structural Comparissons




