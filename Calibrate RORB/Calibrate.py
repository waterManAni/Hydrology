import os
import shutil
import pandas as pdd
from matplotlib import pyplot as plt
import math
import sys

def read_hydrograph (outfile):
    lines = []
    with open(outfile) as samp:
        lines = samp.readlines()
    samp.close()
    for i in range (0, len (lines)):
        if lines[i].find ('Hydrograph summary')>0:
            brk= i
    hydrograph = lines[brk+8:]
    hydcln=[]
    for h in hydrograph:
        clnline=h.replace('  ',' ')
        clnline=clnline.replace('  ',' ')
        clnline=clnline.replace('  ',' ')
        hydcln.append(clnline)
    hydrographframe=pdd.DataFrame(hydcln,columns=['text'])
    hydrographframe = hydrographframe['text'].str.split(' ', expand=True)
    hydrographframe = hydrographframe.replace('\n','', regex=True)
    hydrographframe =hydrographframe.iloc [:,2:6]
    hydrographframe.columns = hydrographframe.iloc[0]
    hydrographframe = (hydrographframe.drop(0)).reset_index (drop=True)
    columnames= hydrographframe.head()
    for c in columnames:
        hydrographframe [c]= hydrographframe[c].astype('float')
    return hydrographframe

def rmse (observed, calculated):
    ms=0.0001
    for i in range(len (observed)):
            ms = ms + (observed[i]-calculated[i])*(observed[i]-calculated[i])
    return math.sqrt(ms/(len (observed)))

def plotflows (time, obs, calc,Filen, rmse):
    fig= plt.figure()
    plt.xlabel ('Time')
    plt.ylabel ('Q (m3/s)')
    plt.title ('IL: '+str(IL)+ ', CL: '+str(CL)+', Kc: '+str(Kc)+', RMSE= '+str(int(rmse)), loc='center')
    plt.plot (x,y1, label = 'Calculated')
    plt.plot (x,y2, label = 'Actual')
    plt.legend (loc='best')
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
parsample= r'T:\animesh.paudel\Python\RORB_Calibrate\Sample.par'
catgname= os.path.splitext((os.path.split (Catg))[1])[0]
try: 
    os.mkdir(plotdir)
except: 
    print ('plotting in plots directory')



ILs= [*range(StartIL,EndIL+ILsteps,ILsteps)]
CL10s=[*range(int(StartCL*10),int(EndCL*10)+int(CLsteps*10),int(CLsteps*10))]
KCs=[*range(StartKc,EndKc+Kcsteps,Kcsteps)]
totalruns=str(len(ILs)*len (CL10s)*len(KCs))

curpythondirectory= r'T:\animesh.paudel\Python\RORB_Calibrate'
os.chdir(curpythondirectory)


lines = []
with open(parsample) as samp:
    lines = samp.read()
errorstat = pdd.DataFrame(columns=['IL','CL','Kc','RMSE'])


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
                 y1 =hydrographs['Hyd001'].to_list()
                 y2=hydrographs['Hyd002'].to_list()
                 x=hydrographs['Time'].to_list()
                 rms = rmse(y2, y1)
                 errorstat.loc[len(errorstat)] = [IL,CL,Kc,rms]
                 plotflows (x,y2,y1,Filen,rms)

         


errorstat.to_csv(os.path.join(curpath,'rmse.csv'),index=False)