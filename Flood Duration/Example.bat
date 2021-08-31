@echo off

SetLocal

set tcf="C:\tcf file with one ecf.tcf"
set ratingcurve="C:\path to rating curve.csv"
set hydrographfolder="C:\folder containing to hydrographs in tuflow format with filenames including AEP, TP and duration"
set outputdur="C:\path to all durations\Durations.csv"
set outputstat="C:\path to median durations etc.csv"


call "T:\animesh.Paudel\Python\Duration\Duration_Conda.bat"

pause