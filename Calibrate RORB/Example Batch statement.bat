@echo off
SetLocal

set stm="C:\users\Path to storm file with one observed hydrograph.stm"
set catg="C:\Users\path to catg file with one I+O reporting location.catg"
set StartKc=105
set EndKc=105
set Kcsteps=10
set StartIL=50
set EndIL=70
set ILsteps=20
set StartCL=0
set EndCL=10
set CLsteps=2
set RORB="T:\animesh.paudel\Python\RORB_Calibrate\RORB_CMD.exe"


call "T:\animesh.Paudel\Python\RORB_Calibrate\RORB_Conda.bat"

pause