@echo off
SetLocal

set stm="C:\path to storm file with observed hydrograph.stm"
set catg="C:\path to catg file with one obs and simulated reporting location only.catg"
set StartKc=105
set EndKc=105
set Kcsteps=10
set StartIL=50
set EndIL=70
set ILsteps=20
set StartCL=0
set EndCL=10
set CLsteps=2


call "T:\animesh.Paudel\Python\RORB_Calibrate\RORB_Conda.bat"

pause