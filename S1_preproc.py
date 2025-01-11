print('''
        ##############################################
        ##############################################\n
        Sentinel-1 Preproc Script for SLC Data Using SNAP Software... \n
        mode1:
        Split-POE Apply-Radiometric Calibration-Deburst\n
        mode2:
        Split-POE Apply-Radiometric Calibration-Deburst-Merge\n
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
    parser.add_argument("-sd", "--sDate", required=True, help="Scene start Year")
    parser.add_argument("-ed", "--eDate", required=True, help="Scene end Year")
    parser.add_argument("-bs", "--burstStart", required=True, help="Start Burst Number")
    parser.add_argument("-be", "--burstEnd", required=True, help="End Burst Number")
    parser.add_argument("-p", "--pol", required=True, help="Polarisation")
    parser.add_argument("-m", "--mode", required=True, help="mode 1: Single \nmode 2:All Swaths")
    parser.add_argument("-sn", "--sNum", required=False, help="Swath Number if mode==1\nIW1 or IW2 or IW3")
    parser.add_argument("-o", "--output", required=True, help="Complex or Sigma0 or Gamma0 or Beta0")
    parser.add_argument("-c", "--cut", required=True, help="Polygon of Subset Area (WKT)\nnone for nothing")
    args = parser.parse_args()
    
    import snappy_for_oriburi as snappy
    from os import listdir
    import numpy as np
    
    files = np.sort(listdir(args.fPath))
    pfiles = []
    for i in files:
        if i[-1] == 'p':
            if (int(i[17:21]) >= int(args.sDate)) and (int(i[17:21]) <= int(args.eDate)):
                pfiles.append(i)
                print(i)
        else: continue
    del files
    
    print('\nThe Number of Scenes: %d' %(len(pfiles)))
    print('Start Year: %s' %(args.sDate))
    print('End   Year: %s' %(args.eDate))
    print('Mode: %s' %(args.mode))
    
    if args.mode == '1':
        for i in pfiles:
            prod = snappy.readProduct(args.fPath,i)
            split = snappy.TOPS_split(prod, args.pol, args.sNum, args.burstStart, args.burstEnd)
            del prod
            
            orb = snappy.s1_orb(split, '0')
            del split
            
            cal = snappy.calibration(orb, 'all', args.pol, args.output)
            del split
            
            if args.output == 'Complex':
                snappy.save(cal, args.sPath+i[17:17+8]+'_cpx_split_orb_cal.dim')
                del cal
                continue
            
            deb = snappy.deburst(cal, args.pol)
            del cal
            
            subset = snappy.subset_wkt(deb, args.cut)
            del deb
            
            snappy.save(subset, args.sPath+i[17:17+8]+'-'+args.output+'_split_orb_cal.dim')
            del subset
            
    if args.mode == '2':
        from esa_snappy import HashMap, GPF
        for i in pfiles:
            prod = snappy.readProduct(args.fPath,i)
            
            split = []
            split.append(snappy.TOPS_split(prod, args.pol, 'IW1', args.burstStart, args.burstEnd))
            split.append(snappy.TOPS_split(prod, args.pol, 'IW2', args.burstStart, args.burstEnd))
            split.append(snappy.TOPS_split(prod, args.pol, 'IW3', args.burstStart, args.burstEnd))
            del prod
            
            orb = []
            for j in range(3):
                orb.append(snappy.s1_orb(split[j], '0'))
            del split
            
            cal = []
            for j in range(3):
                cal.append(snappy.calibration(orb[j], 'all', args.pol, args.output))
            del orb
            
            
            deb = []
            for j in range(3):
                deb.append(snappy.deburst(cal[j], args.pol))
            del cal
            
            sourceProducts= HashMap()
            sourceProducts.put('masterProduct', deb[0])
            sourceProducts.put('slaveProduct1', deb[1])
            sourceProducts.put('slaveProduct2', deb[2])
            parameters = HashMap()

            merge = GPF.createProduct("TOPSAR-Merge", parameters, sourceProducts)
            
            del deb
            
            subset = snappy.subset_wkt(merge, args.cut)
            del merge
            
            snappy.save(subset, args.sPath+i[17:17+8]+'_'+args.output+'_split_orb_cal_mrg.dim')
            del subset

if __name__ == "__main__":
    
    main()