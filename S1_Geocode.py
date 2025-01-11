print('''
        ##############################################
        ##############################################\n
        Sentinel-1 Geocode Using SNAP Software... \n
        Geocoding the preprocessed data\n
        Copyright: Seung Jun Lee
                   Yonsei Univ. Dept. Earth System Science.
                   Satellite Geosciences Lab.\n
        ##############################################
        ##############################################\n\n
        ''')

def main():
    import warnings
    import os
    warnings.filterwarnings('ignore')
    
    import argparse
    parser = argparse.ArgumentParser(description="Process a tif file.")
    parser.add_argument("-f", "--fPath", required=True, help="Path to the Sentinel-1 files")
    parser.add_argument("-s", "--sPath", required=True, help="Path to the save file")
    parser.add_argument("-m", "--ml", required=True, help="1 for Applying Multi_Look\n0 for nothing")
    parser.add_argument("-Az", "--az", required=False, help="Azimuth look number")
    parser.add_argument("-Rg", "--rg", required=False, help="Range look number")
    parser.add_argument("-d", "--dem", required=True, help="DEM name\n'CDEM' or 'Copernicus 30m Global DEM' or 'Copernicus 90m Global DEM' or'GETASSE30' or 'SRTM 1Sec Grid' or 'SRTM 1Sec HGT' or 'SRTM 3Sec'")
    parser.add_argument("-o", "--output", required=True, help="dB for deciBel\nInt for Intensity")
    parser.add_argument("-i", "--inc", required=False, help="Local incidence angle\nTrue of False")
    parser.add_argument("-sf", "--save_format", required=True, help="tif for Geotiff Format\ndim for BEAM-DIMAP")
    args = parser.parse_args()
    
    import snappy_for_oriburi as snappy
    from os import listdir
    import numpy as np
    
    files = np.sort(listdir(args.fPath))
    print('\n\n')
    pfiles = []
    for i in files:
        if i[-1] == 'm':
            pfiles.append(i)
            print(i)
    del files
    print('The Number of Scenes: %d' %len(pfiles))
    
    prod = snappy.readProduct(args.fPath, pfiles[0])

    if args.ml == '1':
        prod = snappy.multi_look(prod, 'all', args.rg, args.az)

    if args.output == 'dB':
        prod = snappy.Linear2dB(prod)

    prod = snappy.terrain_correction(prod, 'all', args.dem, args.inc)
    prod.removeBand(prod.getBand(snappy.extBandNames(prod)[1]))

    if args.ml == '1':
        snappy.save(prod, args.sPath+prod.getName()[0:4]+'_ml_'+args.output+'_'+'_tc.'+args.save_format)

    if args.ml == '0':
        snappy.save(prod, args.sPath+prod.getName()[0:4]+'_'+args.output+'_'+'_tc.'+args.save_format)

    for i in pfiles:
        prod = snappy.readProduct(args.fPath, i)
        
        if args.ml == '1':
            prod = snappy.multi_look(prod, 'all', args.rg, args.az)
            
        if args.output == 'dB':
            prod = snappy.Linear2dB(prod)
        
        prod = snappy.terrain_correction(prod, 'all', args.dem, args.inc)
        prod.removeBand(prod.getBand(snappy.extBandNames(prod)[0]))
        
        if args.ml == '1':
            snappy.save(prod, args.sPath+prod.getName()[4::]+'_ml_'+args.output+'_'+'_tc.'+args.save_format)
            
        if args.ml == '0':
            snappy.save(prod, args.sPath+prod.getName()[4::]+'_'+args.output+'_'+'_tc.'+args.save_format)
        
            
if __name__ == "__main__":
    
    main()
