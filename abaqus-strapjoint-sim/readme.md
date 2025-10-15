# Abaqus Strap Joint Simulation

This project automates the setup and execution of strap joint simulations in Abaqus using Python scripting. Simulation parameters are read from a CSV file and passed to the Abaqus CAE environment for batch processing.

## File Structure

```
abaqus-strapjoint-sim/
├── inputs/
│   └── sim_params.csv         # CSV file with simulation parameters generated using the R script in doe/ccdplan
├── src/
│   ├── run_simulations.py     # Main script to run all simulations
│   └── StrapJoint.py          # Contains the StrapJoint model and material definitions
```

## How to Run

From the root directory (`abaqus-strapjoint-sim`), execute:



This will read the simulation scenarios from `inputs/sim_params.csv` and run each scenario in Abaqus CAE using the [`StrapJoint`](src/StrapJoint.py) model.

## Requirements

- Abaqus CAE installed and available in your system path
- Python scripts compatible with Abaqus Python interpreter

## Input Parameters

Edit [`inputs/sim_params.csv`](inputs/sim_params.csv) to define your simulation scenarios. Example:

```
Overlap,Adhesive,Film_thickness,Cores
30.0,DP490,0.1,10
```

## Output

Simulation results and CAE files will be saved in the root directory.

## Monitoring

Monitor the current progress by running this code in a separate terminal at the root directory:

```sh
Get-Content -Wait -Path ./<part_name>.sta
```