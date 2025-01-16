## SAR-Preprocessing
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

## Anaconda3 installation for Ubuntu-18.04

## Create vitual-environments in Ananconda3
You can create virtual environment by typing the code below in the anaconda prompt<br/>
<br/>
conda create -n [env-name] python==[python-version]
- ex) conda create -n env-test python==3.10

You can check the created environments wiht the code below.<br/>
<br/>
conda info --envs<br/>
<br/>
Locate the snappy_for_oriburi.py in the path below.<br/>
"/home/username/anaconda3/envs/env-test/lib/python3.10/site-packages/"


## snap-python configuration for Ubuntu-18.04
