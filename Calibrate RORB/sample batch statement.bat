::@echo off
SetLocal

set stm="P:\P21167 KUMINA MINE - HAUL ROAD 15 DD\200 CALCULATIONS\201 Waterways\Hydrology\RORB\Cane River\Model\Calibration\95\95_storm.stm"
set catg="P:\P21167 KUMINA MINE - HAUL ROAD 15 DD\200 CALCULATIONS\201 Waterways\Hydrology\RORB\Cane River\Model\Cane_Existing.catg"
set StartKc=70
set EndKc=120
set Kcsteps=5
set StartIL=0
set EndIL=100
set ILsteps=10
set StartCL=0
set EndCL=10
set CLsteps=1


call "T:\animesh.paudel\Python\RORB_Calibrate\RORB_Conda.bat"