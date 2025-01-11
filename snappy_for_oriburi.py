# ####################################################################
# ####                                                               #
# ####    snappy_for_oriburi                                         #
# ####                                                               #
# ####    Copyright(c) Seungjun Lee                                  #
# ####                   Yonsei Univ. (Seoul, South Korea)           #
# ####                   Department of Earth System Science          #
# ####                                                               #
# ####    Version: 1.0                                               #
# ####    last update : 2024.09.05                                   #
# ####    Since 2024.09.18                                           #
# ####                                                               #
# ####################################################################

from esa_snappy import ProductIO
from esa_snappy import WKTReader
from esa_snappy import HashMap
from esa_snappy import GPF
from esa_snappy import jpy

import numpy as np
import matplotlib.pyplot as plt

#%% functions


def readProduct (path, product):

    '''
    [Usage]  deadProduct(path, product)\n

    read single product file\n
    
    all parameters should be str\n

    path:     /path/to/your/sat_sata/
    product:  product file name including format
    '''

    return ProductIO.readProduct(path+product)

def TOPS_split (product, pol, swath, first_burst, last_burst):

    '''
    [Usage]  TOPS_split(product, pol, swath, first_burst, last_busrt)\n

    split subswath and bursts of Sentinel-1A/B (TOPS)\n

    all parameters should be str\n

    product:  target product
    pol:      polarisation 
              'VV' or 'VH' or 'HV' or 'HH'
    swath:    subswath number
              'IW1' or 'IW2' or 'IW3'
    first_burst: lowest burst number of target bursts
    last_burst: highest burst number of target bursts
    '''

    print('')
    print('TOPSSAR-Split\n')

    parameters = HashMap()
    if pol == 'VV' or pol == 'VH':
        parameters.put('selectedPolarisations', pol)
    parameters.put('subswath', swath)
    parameters.put('firstBurstIndex', first_burst)
    parameters.put('lastBurstIndex', last_burst)

    return GPF.createProduct("TOPSAR-Split", parameters, product)

def s1_orb (product, polynomial):

    '''
    [Usage]  s1_orb(product, polynomial)\n

    apply precise orbit for Sentinel-1A/B\n

    all parameters should be str\n

    product:  target product
    polynomial: polynomial degree
                it can be set from '0' to '5'
                '0' is for defualt
    '''

    if polynomial == '0':
        polynomial = '3'
    
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('orbitType', 'Sentinel Precise (Auto Download)')
    parameters.put('polyDegree', polynomial)
    parameters.put('continueOnFail', 'false')

    return GPF.createProduct('Apply-Orbit-File', parameters, product)

def thermal_noise_removal (product, pol):

    '''
    [Usage]  s1_orb(product, polynomial)\n

    apply thermal noise removal\n

    product:  target product
    pol:      polarisation 
              'VV' or 'VH' or 'HV' or 'HH'
    '''

    parameters = HashMap()
    parameters.put('removeThermalNoise', True)
    parameters.put('selectedPolarisations', pol)
    parameters.put('removeThermalNoise', True)

    return GPF.createProduct('ThermalNoiseRemoval', parameters, product)

def remove_GRD_border_noise(product):

    parameters = HashMap()
    parameters.put('borderLimit', 500)
    parameters.put('trimThreshold', 0.5)

    return GPF.createProduct('Remove-GRD-Border-Noise', parameters, product)

def calibration (product, band, pol, output):
    
    '''
    [Usage]  calibration(product, band, pol, output)\n

    apply radiometric calibration\n

    all parameters should be str\n

    product:  target product
    band:     source band
              you can check band name by using band_info(product)
              'all' for all bands
    pol:      polarisation 
              'VV' or 'VH' or 'HV' or 'HH'
    output:   output band
              'Sigma0' or 'Gamma0' or 'Beta0' or 'Complex'
    '''

    parameters = HashMap()
    if output == 'Sigma0':
        parameters.put('outputSigmaBand', True)
    if output == 'Gamma0':
        parameters.put('outputGammaBand', True)
        parameters.put('outputSigmaBand', False)
    if output == 'Beta0':
        parameters.put('outputBetaBand', True)
    if output == 'Complex':
        parameters.put('outputImageInComplex', True)
    
    if band == 'all':
        print('all source bands')
    else:
        parameters.put('sourceBands', band)
    if pol == 'VV' or pol == 'VH':
        parameters.put('selectedPolarisations', pol)
    parameters.put('outputImageScaleInDb', False)

    return GPF.createProduct("Calibration", parameters, product)

def subset_wkt (product, wkt):
    
    '''
    [Usage]  subset_wkt(product, wkt)\n

    subset image by geolocation\n

    all parameters should be str\n

    product:  target product
    wtk:      geolocation coordinate of Area of Interest (AOI)
              'POLYGON((72.80 19.05, 72.80 19.00, 72.90 19.00, 72.90 19.05, 72.80 19.05))'
    '''
    
    SubsetOp = jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
    geometry = WKTReader().read(wkt)
    HashMap = jpy.get_type('java.util.HashMap')
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters = HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', geometry)
    return GPF.createProduct('Subset', parameters, product)

def deburst (product, pol):

    '''
    [Usage]  deburst(product, pol)\n

    deburst Sentinel-1A/B (TOPS)\n

    all parameters should be str\n

    product:  target product
    pol:      polarisation 
              'VV' or 'VH' or 'HV' or 'HH'
    '''
    
    parameters = HashMap()
    if pol == 'VV' or pol == 'VH':
        parameters.put("Polarisations", pol)
    return GPF.createProduct("TOPSAR-Deburst", parameters, product)

def TOPS_merge (product1, product2):
    sourceProducts= HashMap()
    sourceProducts.put('masterProduct', product1)
    sourceProducts.put('slaveProduct', product2)

    parameters = HashMap()
    
    return GPF.createProduct("TOPSAR-Merge", parameters, sourceProducts)

def TOPS_deramp (product):

    parameters = HashMap()

    return GPF.createProduct("TOPSAR-DerampDemod", parameters, product)

def backgeocoding (product_ref, product_sec):
    '''
    for i in range (len(product_sec)):
        product_ref.append(product_sec[i])
    '''
    sourceProducts = HashMap()
    sourceProducts.put('masterProduct', product_ref)
    sourceProducts.put('slaveProduct', product_sec)

    parameters = HashMap()
    parameters.put("Digital Elevation Model", "Copernicus 30m Global DEM")
    parameters.put("demResamplingMethod", "BICUBIC_INTERPOLATION")
    parameters.put("Resampling Type", "BISINC_5_POINT_INTERPOLATION")
    parameters.put("Output Deramp and Demod Phase", False)
    parameters.put('nodataValueAtSea',False)
    parameters.put('maskOutAreaWithoutElevation', False)
    
    return GPF.createProduct("Back-Geocoding", parameters, sourceProducts)

def ESD (product):
    
    parameters = HashMap()
    parameters.put("Registration Window Width", 512)
    parameters.put("Registration Window Height", 512)
    parameters.put("Search Window Accuracy in Azimuth Direction", 16)
    parameters.put("Search Window Accuracy in Range Direction", 16)
    parameters.put("Window oversampling factor", 128)
    parameters.put("Cross-Correlation Threshold", 0.1)
    parameters.put("cohThreshold", 0.3)
    parameters.put("esdEstimator", 'Periodogram')
    parameters.put("weightFunc", 'Inv Quadratic')
    parameters.put("temporalBaselineType", 'Number of images')
    parameters.put("integrationMethod", 'L1 and L2')
    parameters.put("doNotWriteTargetBands", False)
    parameters.put("useSuppliedRangeShift", False)
    parameters.put("overallRangeShift", 0.0)
    parameters.put("useSuppliedAzimuthShift",False)
    parameters.put("overallAzimuthShift",0.0)
    
    return GPF.createProduct("Enhanced-Spectral-Diversity", parameters, product)

def stack_corr (mProduct, sProduct):
    
    sourceProducts = HashMap()
    sourceProducts.put('masterProduct', mProduct)
    sourceProducts.put('slaveProduct', sProduct)

    print('\n\nGenerating stack ...')
    parameters = ""
    parameters = HashMap()
    parameters.put('Initial Offset Method', 'Product Geolocation')
    parameters.put('Output Extents', 'Master')
    product_stack = GPF.createProduct("CreateStack", parameters, sourceProducts)

    print('\n\nCalculating Cross Correlation ...')
    parameters = ""
    parameters = HashMap()
    parameters.put('Test GCPs are on  land', True)
    parameters.put('Apply Fine Registration for SLCs', True)
    parameters.put('Number of GCPs', 100000)
    parameters.put('Coarse Window Width', 128)
    parameters.put('Coarse Window height', 128)
    parameters.put('Row Interpolation Factor', 4)
    parameters.put('Column Interpolation Factor', 4)
    parameters.put('Max Interations', 30)
    parameters.put('Fine Window Width', 32)
    parameters.put('Fine Window Height', 32)
    parameters.put('Coherence based registration', False)
    product_stack = GPF.createProduct("Cross-Correlation", parameters, product_stack)

    print('\n\nApplying Warp ...')
    parameters = ""
    parameters = HashMap()
    parameters.put('RMS Threshold (pixel accuracy)', 0.05)
    parameters.put('Warp polynomial Order', 6)
    parameters.put('Interpolation Method', 'Cubic convolution (6 points)')
    
    return GPF.createProduct("Warp", parameters, product_stack)

def stack_dem (product_ref, product_sec):

    
    print('\n\tProcessing DEM-Assisted-Coregistration ...\n')
    
    sourceProducts = HashMap()
    sourceProducts.put('masterProduct', product_ref)
    sourceProducts.put('slaveProduct', product_sec)

    parameters = HashMap()
    parameters.put('digitalElevationModel', 'Copernicus 30m Global DEM (Auto Download)')
    parameters.put('nodataValueAtSea',False)
    parameters.put('maskOutAreaWithoutElevation', False)
    
    return GPF.createProduct("DEM-Assisted-Coregistration", parameters, sourceProducts)

def stack_dem_corr (mProduct, sProduct):

    
    sourceProducts = HashMap()
    sourceProducts.put('masterProduct', mProduct)
    sourceProducts.put('slaveProduct', sProduct)    
        
    parameters = HashMap()
    parameters.put('digitalElevationModel', 'Copernicus 30m Global DEM (Auto Download)')
    parameters.put('nodataValueAtSea',False)
    parameters.put('maskOutAreaWithoutElevation', False)

    product_stack = GPF.createProduct("DEM-Assisted-Coregistration", parameters, sourceProducts)

    print('\n\nCalculating Cross Correlation ...')
    parameters = ""
    parameters = HashMap()
    parameters.put('Number of GCPs', 50000)
    parameters.put('Coarse Window Width', 128)
    parameters.put('Coarse Window height', 128)
    parameters.put('Row Interpolation Factor', 4)
    parameters.put('Column Interpolation Factor', 4)
    parameters.put('Max Interations', 10)
    parameters.put('Fine Window Width', 8)
    parameters.put('Fine Window Height', 8)
    product_stack = GPF.createProduct("Cross-Correlation", parameters, product_stack)

    print('\n\nApplying Warp ...')
    parameters = ""
    parameters = HashMap()
    parameters.put('RMS Threshold (pixel accuracy)', 0.05)
    parameters.put('Warp polynomial Order', 3)
    parameters.put('Interpolation Method', 'Cubic convolution (6 points)')
    
    return GPF.createProduct("Warp", parameters, product_stack)

def coherence_estimation (product, band):
  

    parameters = HashMap()
    parameters.put('sourceBands', band)
    parameters.put('Subtract flat-earth phase', True)
    parameters.put('Subtract topogrphic phase', True)
    parameters.put('Digital Elevation Model', 'Copernicus 30m Global DEM (Auto Download)')    

    return GPF.createProduct("Coherence", parameters, product)

def multi_look (product, band, Rg, Az):
    
    '''
    [Usage]  Multi_Look(product, band, Rg, Az)\n

    apply multilooking\n

    all parameters should be str\n

    product:  target product
    band:     source band
              you can check band name by using band_info(product)
              'all' for all bands
    Rg:       number of pixels to apply multi looking in range direction
    Az:       number of pixels to apply multi looking in azimuth direction
    '''
    parameters = HashMap()
    parameters.put('nRgLooks', Rg)
    parameters.put('nAzLooks', Az)
    if band == 'all':
        print('all source bands')
    else:
        parameters.put('sourceBands', band)
    parameters.put('outputIntensity', True)
    parameters.put('grSquarePixel', True)
    
    return GPF.createProduct("Multilook", parameters, product)

def speckle_filter(product, band, filter_name, kernel_size):

    '''
    [Usage]  speckle_filter(product, band, filter_name, kernel_size)\n

    apply speckle filtering\n

    all parameters should be str\n

    product:  target product
    band:     source band
              you can check band name by using band_info(product)
              'all' for all bands
    filter_name: name of speckle filter
                 'Lee' or 'Refined Lee' or 'BOXCAR' or 'MEDIAN' or 'Frost' or 'Gamma Map' or
                 'Lee Sigma' or 'IDAN'
    kernel_size: size of kernel
                 same size in each x and y direction
    '''

    parameters = HashMap()
    parameters.put('filter', filter_name)
    parameters.put('filterSizeX', kernel_size)
    parameters.put('filterSizeY', kernel_size)
    if band == 'all':
        print('all source bands')
    else:
        parameters.put('sourceBands', band)

    return GPF.createProduct("Speckle-Filter", parameters, product)

def terrain_correction (product, band, dem_name, local_incidence_angle):

    '''
    [Usage]  terrain_correction(product, band, dem_name)\n

    apply terrain correction\n

    all parameters should be str\n

    product:  target product
    band:     source band
              you can check band name by using band_info(product)
              'all' for all bands
    dem_name: name of dem (Auto Download)
              'CDEM' or 'Copernicus 30m Global DEM' or 'Copernicus 90m Global DEM' or
              'GETASSE30' or 'SRTM 1Sec Grid' or 'SRTM 1Sec HGT' or 'SRTM 3Sec'
    '''
    
    parameters = HashMap()
    if band == 'all':
        print('all source bands')
    else:
        parameters.put('sourceBands', band)

    parameters.put('pixelSpacingInMeter', 10.0)
    parameters.put('demName', dem_name)
    parameters.put('demResamplingMethod', 'CUBIC_CONVOLUTION')
    parameters.put('imageResamplingMethod', 'CUBIC_CONVOLUTION') #NEAREST_NEIGHBOR
    parameters.put('nodataValueAtSea',False)
    parameters.put('maskOutAreaWithoutElevation', False)
    parameters.put('pixelSpacing(m)', 10)
    if local_incidence_angle == True:
        parameters.put('saveLocalIncidenceAngle', True)
    else:
        parameters.put('saveLocalIncidenceAngle', False)

    return GPF.createProduct("Terrain-Correction", parameters, product)

def Linear2dB (product):
    
    '''
    [Usage]  terrain_correction(product, band, dem_name)\n

    convert band to dB\n

    product:  target product
    '''
    parameters = HashMap()

    return GPF.createProduct('LinearToFromdB', parameters, product)

def collocate (mProduct, sProduct):
    
    '''
    [Usage]  collocate(mProduct, sProduct) \n

    collocate geo-coded products\n

    mProduct:  reference product in esa_snappy format
    sProduct:  single secondary image in esa_snappy format or
               secondary images in list
    '''
    
    parameters = HashMap()
    if type(sProduct) == list:
        sourceProducts = jpy.array('org.esa.snap.core.datamodel.Product',len(sProduct)+1)
        sourceProducts[0] = mProduct
        for i in range (len(sProduct)):
            sourceProducts[i+1] = sProduct[i]
        parameters.put('masterProductName', sourceProducts[0].getName())
        
    else:
        sourceProducts = HashMap()
        sourceProducts.put("master", mProduct)
        sourceProducts.put("slave", sProduct)
    
    
    parameters.put('targetProductName', mProduct.getName()+'_collocate')
    parameters.put('resamplingType', 'CUBIC_CONVOLUTION')
    
    return GPF.createProduct('Collocate', parameters, sourceProducts)

def band_info (product):

    '''
    [Usage]  band_info(product)\n

    show simple information of band data\n

    product:  target product
    '''

    print('Band Info')
    name = product.getName()
    print("Name: {}".format(name))
    band_names = product.getBandNames()
    print("Band names: {}".format(", ".join(band_names)))    
    width = product.getSceneRasterWidth()
    print("Width: {} px".format(width))
    height = product.getSceneRasterHeight()
    print("Height: {} px".format(height))

def disp (product, band_name, vmin, vmax):

    '''
    [Usage]  disp(product, band_name, vmin, vmax)\n

    display specific band data\n

    product:  target product
    band_name:name of target band data
    vmin:     min value of band when display
    vmax:     max value of band when display
    '''

    band = product.getBand(band_name)
    w = band.getRasterWidth()
    h = band.getRasterHeight()
    print(w, h)

    band_data = np.zeros(w * h, np.float32)
    band.readPixels(0, 0, w, h, band_data)
    band_data.shape = h, w

    def onclick(event):
        if event.button == 1:
            print(f'pixel coords: x={int(event.xdata)}, y={int(event.ydata)}')
            print('pixel value:', band_data[int(event.ydata), int(event.xdata)])
            print('')

    fig, ax = plt.subplots()
    a = plt.imshow(band_data, cmap='gist_gray', vmin=vmin, vmax=vmax)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.axis('off')
    print('Min Pixel Value:', np.min(band_data))
    print('Max Pixel Value:', np.max(band_data))
    return plt.show()

def save (product, save_dir):

    '''
    [Usage]  save(product, save_dir) \n

    save product as GeoTIFF of BEAM-DIMAP\n

    product:  target product
    save_dir: /path/to/save/directory/productnam.tif or
              /path/to/save/directory/productnam.dim
    '''
    if save_dir[-3::] == 'tif':
        ProductIO.writeProduct(product, save_dir, 'GeoTIFF')
    if save_dir[-3::] == 'dim':
        ProductIO.writeProduct(product, save_dir, 'BEAM-DIMAP')

    print('Product saved in\n', save_dir)
    return

def extBandNames (product):
    name = ",".join(product.getBandNames())

    bands = []
    j = ''
    for i in name:
        if i == ',':
            bands.append(j)
            j = ''
            continue
        else:
            j = j+i
    bands.append(j)
    return bands

def extBand (product, bandName):
    
    import numpy as np
    
    bandData = product.getBand(bandName)
    w = product.getSceneRasterWidth()
    h = product.getSceneRasterHeight()
    
    band_array = np.zeros(w * h, np.float32)
    bandData.readPixels(0, 0, w, h, band_array)
    band_array.shape = h,w

    return band_array

def extBandForOriburi (product, bandName):
    import numpy as np
    
    bandData = product.getBand(bandName)
    w = product.getSceneRasterWidth()
    h = product.getSceneRasterHeight()
    
    band_array = np.zeros(w * h, np.float32)
    bandData.readPixels(0, 0, w, h, band_array)
    band_array.shape = h,w

    return {'Band' : band_array, 'Product Name' : product.getName()}
