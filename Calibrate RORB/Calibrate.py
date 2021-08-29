import os
import shutil
import pandas as pdd
from matplotlib import pyplot as plt
import math
import sys
from PyHMA import HMA
import numpy as np

def hydrographmatch(qoA, qsA,time_scale,lag_allowed,lead_allowed,plotyn):
    hA = HMA(qoA, qsA, b=time_scale, max_lag=lag_allowed, max_lead=lead_allowed, measure='nse', keep_internals=False, calc_rays=False)
    fsim = hA.calc_dense2()
    #dense =high ram usage, orig= medium ram usage, dense2= no internals and ray plotting allowed
    return fsim

def read_hydrograph (outfile):
    lines = []
    with open(outfile) as samp:
        lines = samp.readlines()
    samp.close()
    for i in range (0, len (lines)):
        if lines[i].find ('Hydrograph summary')>0:
            brk= i
    hydrograph = lines[brk+7:]
    hydcln=[]
    for h in hydrograph:
        clnline=h.replace('  ',' ')
        clnline=clnline.replace('  ',' ')
        clnline=clnline.replace('  ',' ')
        hydcln.append(clnline)
    hydrographframe=pdd.DataFrame(hydcln,columns=['text'])
    hydrographframe = hydrographframe['text'].str.split(' ', expand=True)
    hydrographframe = hydrographframe.replace('\n','', regex=True)
    hydrographframe =hydrographframe.iloc [:,2:5]
    hydrographframe.columns = hydrographframe.iloc[0]
    hydrographframe = (hydrographframe.drop(0)).reset_index (drop=True)
    columnames= hydrographframe.head()
    for c in columnames:
        hydrographframe [c]= hydrographframe[c].astype('float')
    # print (hydrographframe)
    return hydrographframe

def rmse (observed, calculated):
    ms=np.square(np.subtract(observed, calculated)).mean()
    return ms

def sig_places(value):
   return ('{:g}'.format(float('{:.1g}'.format(value))))

def plotflow (time,qsA,qoA,Filen,rmse,hmindex):
    fig=plt.figure()
    ax = fig.add_subplot(111)
    #plot simulated
    plt.plot (time,qsA,label='Modelled',color='red')
    spy,spx= np.amax(qsA),time[np.where(qsA==np.amax(qsA))][0]
    ax.axvline(spx, color='red',linestyle='-.',alpha=0.3)
    ax.axhline(spy, color='red',linestyle='-.',alpha=0.3)
    #plot observed
    plt.plot (time,qoA,label='Observed',color='black')
    opy,opx= np.amax(qoA),time[np.where(qoA==np.amax(qoA))][0]
    ax.axvline(opx, color='black',linestyle='-.',alpha=0.3)
    ax.axhline(opy, color='black',linestyle='-.',alpha=0.3)
    

    plt.legend(loc='right')
    plt.xlabel ('Time (hours)')
    plt.ylabel ('Q (m3/s)')
    plt.gca().set_title ('IL: '+str(IL)+ ', CL: '+str(CL)+', Kc: '+str(Kc)+'       RMSE/Peak= '+str(int(round(rms/opy,0))) +', Match: '+str(int(round(hmindex*100,0)))+'%',loc='left')
    outfig= os.path.join (plotdir,Filen+'.jpg')
    fig.savefig(outfig,bbox_inches="tight")
    plt.close ('all')

def tempfiles (curpath, origstm,parsample,IL,CL,Kc):
    tempdir = os.path.join (curpath, 'temp')
    try: 
        os.mkdir(tempdir)
    except: 
        pass
    Filen=str(Kc)+'_'+str(IL)+'_'+str(int((CL*10)))
    tempstm=os.path.join (tempdir, Filen+'.stm')
    shutil.copyfile(origstm, tempstm)
    partext=((lines.replace('Kc',str(Kc))).replace('IL',str(IL))).replace('CL',str(CL))
    partext=(partext.replace('Catchment',Catg)).replace('Storm',tempstm)
    temppar= os.path.join (tempdir,Filen+'.par')
    with open (temppar, "w") as parfile:
        parfile.write(partext)
    parfile.close()
    outfile = os.path.join (tempdir, catgname+'_'+Filen+'.out')
    return temppar,outfile,tempstm,Filen

def getinputs ():
    origstm = sys.argv[1]#read in the arguments from batch file, 0 is the .py file itself
    Catg= sys.argv[2]
    StartKc= int(sys.argv[3])
    EndKc=int(sys.argv[4])
    Kcsteps=int(sys.argv[5])
    StartIL=int(sys.argv[6])
    EndIL=int(sys.argv[7])
    ILsteps=int(sys.argv[8])
    StartCL=float(sys.argv[9])
    EndCL=float(sys.argv[10])
    CLsteps=float(sys.argv[11])
    return origstm, Catg, StartKc,EndKc,Kcsteps,StartIL,EndIL,ILsteps,StartCL,EndCL,CLsteps

origstm,Catg,StartKc,EndKc,Kcsteps,StartIL,EndIL,ILsteps,StartCL,EndCL,CLsteps= getinputs()

curpath=(os.path.split(origstm))[0]
plotdir= os.path.join (curpath,'plots')
curpythondirectory = os.path.dirname(os.path.realpath(__file__))

parsample= os.path.join (curpythondirectory, 'Sample.par')
catgname= os.path.splitext((os.path.split (Catg))[1])[0]
os.chdir(curpythondirectory)

try: 
    os.mkdir(plotdir)
except: 
    print ('plotting in plots directory')



ILs= [*range(StartIL,EndIL+ILsteps,ILsteps)]
CL10s=[*range(int(StartCL*10),int(EndCL*10)+int(CLsteps*10),int(CLsteps*10))]
KCs=[*range(StartKc,EndKc+Kcsteps,Kcsteps)]
totalruns=str(len(ILs)*len (CL10s)*len(KCs))


lines = []
with open(parsample) as samp:
    lines = samp.read()
errorstat = pdd.DataFrame(columns=['IL','CL','Kc','RMSE','MatchIndex'])


i=0
for CL10 in CL10s:
    CL=CL10/10
    for IL in ILs:
             for Kc in KCs:
                 i=i+1
                 print ('Running: ', str (i), ' of ',totalruns )
                 temppar,outfile,tempstm,Filen =tempfiles (curpath,origstm,parsample,IL,CL,Kc)
                 os.system('RORB_CMD.exe'+' "'+temppar+'"')
                 os.remove (temppar) #delete the parameter file created
                 os.remove (tempstm)
                 hydrographs= read_hydrograph (outfile)
                 time = hydrographs ['Time'].to_numpy()
                 qsA =hydrographs['Hyd001'].to_numpy()
                 # qsA[qsA == 0] = 0.01
                 qoA=hydrographs['Hyd002'].to_numpy()
                 # qoA[qoA == 0] = 0.01
                 rms = rmse(qoA, qsA)
                 hA = hydrographmatch(qoA, qsA, 4, 50, 50,'y')
                 errorstat.loc[len(errorstat)] = [IL,CL,Kc,round(rms,0),round(hA,3)]
                 plotflow(time,qsA,qoA, Filen,rms, hA)

         


errorstat.to_csv(os.path.join(curpath,'rmse.csv'),index=False)