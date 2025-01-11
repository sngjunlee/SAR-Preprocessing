print('''
        ##############################################
        ##############################################\n
        Sentinel-1 Co-Registration Using SNAP Software... \n
        mode1:
        S1 Back-Geocoding\n
        mode2:
        Cross-Correlation Co-registration\n
        mode3:
        DEM-Assisted Co-Registration\n
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
    parser.add_argument("-m", "--mode", required=True, help="mode 1: S1 Back-Geocoding\nmode 2:Cross-Correlation Co-registration\nmode 3:DEM-Assisted Co-registration")
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
        
    ref = snappy.readProduct(args.fPath, pfiles[0])
    print('Reference Product: %s' %ref.getName())
    for i in pfiles[1::]:
        prod = snappy.readProduct(args.fPath, i)
        if args.mode == '1':
            stack = snappy.backgeocoding(ref, prod)
            snappy.save(stack, args.sPath+ref.getName()[0:4]+'_'+prod.getName()+'_stack.dim')
        
        if args.mode == '2':
            stack = snappy.stack_corr(ref, prod)
            snappy.save(stack, args.sPath+ref.getName()[0:4]+'_'+prod.getName()+'_stack.dim')
    
        if args.mode == '3':
            stack = snappy.stack_dem(ref, prod)
            snappy.save(stack, args.sPath+ref.getName()[0:4]+'_'+prod.getName()+'_stack.dim')
            
if __name__ == "__main__":
    
    main()