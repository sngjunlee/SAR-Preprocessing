# SAR-Preprocessing
Python program for Sentinel-1 pre-processing using SNAP software.

SNAP10 is recommended and snap-python must be configured.<br/>
Linux environment is recommended.

* snappy_for_oriburi.py is libraray that contains modules of each snap function. It is intended to use snap-python with  oriburi.py
  * It is recommended to locate snappy_for_oriburi.py in site-packages file of your python environment. 

* S1_preprc.py is for preprocessing before coregistration of multi-temporal s1 images.<br/>
  * mode1: Split-POE Apply-Radiometric Calibration-Deburst
  * mode2: Split-POE Apply-Radiometric Calibration-Deburst-Merge
  
* S1_stack.py is for coregistration of multi-temporal s1 images.<br/>
  * mode1: S1 Back-Geocoding
  * mode2: Cross-Correlation Co-registration
  * mode3: DEM-Assisted Co-Registration

* S1_Geocode.py is for geocode images.<br/>
  * output format: BEAM-DIMAP or GeoTiff

# anaconda installation and create virtual-environments for Ubuntu-18.04

# snap-python configuration for Ubuntu-18.04
