import pandas as pdd
import matplotlib.pyplot as plt
import os
import sys

def getea (el):
    profile = el.copy()
    z0=el['Z'].iloc[0]
    z1=el['Z'].iloc[-1]
    x0=el['DIST'].iloc[0]
    x1=el['DIST'].iloc[-1]
    S= (z0-z1)/(x1-x0)
    profile['DIST_1']=profile.DIST.shift(-1)
    profile['Z_1']=profile.Z.shift (-1)
    profile = profile[:-1]
    profile['LocalSlope']=(profile['Z']-profile['Z_1'])/(profile['DIST_1']-profile['DIST'])
    maxslope=profile['LocalSlope'].max()
    minslope=((profile['LocalSlope']>0)*(profile['LocalSlope'])).min()
    for k in range (1001):
        m=minslope+ k*(maxslope-minslope)/1000
        profile['ealine']=z1+m*(x1-profile['DIST'])
        profile['ealine_1']=z1+m*(x1-profile['DIST_1'])
        profile['area']=(profile['DIST_1']-profile['DIST'])*0.5*((profile['ealine']-profile['Z'])+(profile['ealine_1']-profile['Z_1']))
        easum=abs(profile['area'].sum())
        if k==0:
            eafinal=easum
            Se=m
        elif easum<eafinal:
            eafinal=easum
            Se=m
    el ['EALine']=z1+Se*(x1-el['DIST'])
    
    print ('Stream: ',Linename,'\t\tEA Slope: ',round(Se,4),'\t\tTop to Bottom Slope: ',round(S,4) )
    return (Se,S)
    # smax=1
    # smin=0
    # for iteration in range (1000):
    #     print (iteration)

def getinputs ():
    profilecsv=sys.argv[1]
    outputfolder=sys.argv[2]
    return profilecsv, outputfolder
    
profilecsv,outputloc= getinputs()
print ('input Profile: ',profilecsv)
print ('outputs saved to: ',outputloc)
print ("-"*30)

sections=pdd.read_csv(profilecsv)
outfile=pdd.DataFrame(columns=['Stream','EASlope','Slope_AtoB'])
for i in sections.groupby('Name'):
    Linename=str(i[0])
    el=i[1].sort_values(by=['DIST'])
    Se,S= getea (el)
    plt.plot(el['DIST'].to_list(),el['Z'].to_list())
    plt.plot(el['DIST'].to_list(),el['EALine'].to_list())
    plt.savefig(os.path.join(outputloc,Linename+'.jpg'))
    results=[Linename, Se,S]
    outfile.loc [len(outfile)]=results
    plt.close()
outfile.to_csv(os.path.join (outputloc,'results.csv'),index=False)   