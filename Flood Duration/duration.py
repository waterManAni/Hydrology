import pandas as pd
import os
from classify import *
import sys


def get_inputs ():
    tcf=sys.argv[1]
    ratingcurve=sys.argv[2]
    hydrofolder=sys.argv[3]
    outputdur=sys.argv[4]
    outputstat=sys.argv[5]
    return tcf,ratingcurve,hydrofolder,outputdur,outputstat


tcf,ratingcurve,hydrofolder,outputdur,outputstat= get_inputs()
FreqClasses, CCClasses, DurClasses, TPClasses=Eventdefn(tcf)

rcH=pd.read_csv(ratingcurve)['WSEL'].to_list()
rcQ=pd.read_csv(ratingcurve)['Q'].to_list()



flist=[]
for f in os.walk(hydrofolder):
    for file in f[2]:
        if file.find ('.csv')>1 and file.find ('.xf')<0:
            flist.append (file)
outputdf=pd.DataFrame(columns=['file','WSEL','Inundation Period','Frequency','Duration','TP'])
statdf= pd.DataFrame(columns=['WSEL','Frequency','Duration','Median_TP','Median_File','Median_hr','Min_hr','Max_hr'])

for i in range(len(flist)):
    hyddb=pd.read_csv(os.path.join (hydrofolder,flist[i]))
    dt=(hyddb['Time (hrs)'][1]-hyddb['Time (hrs)'][0])
    print ('reading hydrograph: ',str(i+1),'of ',str(len (flist) ))
    for k in range (len(rcH)):
        wse=rcH[k]
        Q=rcQ[k]    
        m=(sum(hyddb['Calculated hydrograph:'] >= Q))*dt
        Freq,remtext=eventclassify (flist[i], FreqClasses)
        Dur,remtext=eventclassify (remtext, DurClasses)
        TP,remtext=eventclassify (remtext, TPClasses)
        outputdf.loc[len(outputdf)]=[flist[i],wse,m,Freq,Dur,TP]

outputdf.to_csv(outputdur,index=False)

for grbywsel in outputdf.groupby ('WSEL'):
        for grbyfr in grbywsel[1].groupby ('Frequency'):
            AppendStat=[]
            for grbydur in grbyfr[1].groupby ('Duration'):
                TPStat = Duration_stat(grbydur[1])
                try:
                    if TPStat[7]>AppendStat[7]:
                        AppendStat=TPStat
                except:
                    AppendStat=TPStat #if appendstat is empty, just get first group of stats i.e. first duration in a frequency group
            statdf.loc[len(statdf)]=AppendStat

statdf.to_csv(outputstat,index=False)