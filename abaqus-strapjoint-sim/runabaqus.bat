@echo off
REM Change to the src directory
cd src

REM Get the first scenario's parameters from the CSV
for /f "skip=1 tokens=1-4 delims=," %%a in (../inputs/sim_params.csv) do (
    set "overlap=%%a"
    set "adhesive=%%b"
    set "film_thickness=%%c"
    set "cores=%%d"
    goto :found
)
:found

REM Remove spaces from adhesive name
set "adhesive=%adhesive: =%"

REM Build the .sta filename (adjust pattern as needed)
set "sta_file=../SAP%overlap%_%film_thickness%mu_%adhesive%.sta"

REM Run the simulation with Abaqus
abaqus cae noGUI=run_simulations.py

REM Open a new terminal to monitor the .sta file
start cmd /k "powershell Get-Content -Wait -Path %sta_file%"