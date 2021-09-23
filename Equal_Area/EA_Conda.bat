@echo off

:READ THE PATH OF THE BATCH FILE

set cd=%~dp0

set Condaactivate="C:\Users\Animesh.Paudel\Miniconda3/Scripts/activate.bat"
set environment=hydrology38

set EA="%cd%\Equal_Area.py"


call  %Condaactivate% %environment%


python %EA% %profiles% %outputfolder%