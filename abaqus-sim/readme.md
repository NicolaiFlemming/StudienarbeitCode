# Abaqus Strap Joint Simulation

This project automates the setup and execution of strap joint simulations in Abaqus using Python scripting. It provides a flexible framework for running both batch simulations and single-point analyses of CFRP strap joints with different adhesive types.

## Features

- Batch processing of multiple simulation scenarios
- Support for different adhesive materials (DP490, AF163)
- Configurable parameters (overlap length, adhesive thickness)
- Multi-core processing support
- Automatic file organization and naming

## File Structure

```text
abaqus-sim/
├── inputs/
│   ├── sim_params.csv         # CSV file with simulation parameters
│   └── sim_params_example.csv # Example parameter file for reference
├── src/
│   ├── run_simulations.py     # Main script to run simulations
│   ├── stop_abaqus.py        # Utility to stop running simulations
│   └── StrapJoint.py         # Core model and material definitions
```

## Usage

### Batch Mode

1. Generate simulation parameters using either Design of Experiments (DOE) script:
   ```sh
   python ../doe/lhsplan.py  # Latin Hypercube Sampling
   # or
   python ../doe/ccdplan.py  # Central Composite Design
   ```

2. Run simulations from the root (`abaqus-strapjoint-sim`) directory:
   ```sh
   abaqus cae noGui=src/run_simulations.py
   ```

### Single Point Mode

For running a single simulation with specific parameters:
```sh
abaqus cae noGui=src/run_simulations.py -- --single <overlap> <adhesive> <film_thickness> <cores>
```
Example:
```sh
abaqus cae noGui=src/run_simulations.py -- --single 45.0 DP490 0.25 28
```

## Input Parameters

The `sim_params.csv` file should contain the following columns:

| Column | Description | Range |
|--------|-------------|--------|
| Overlap | Joint overlap length in mm | 30.0 - 60.0 |
| Adhesive | Adhesive type | 'DP490' or 'AF163' |
| Film_thickness | Adhesive thickness in mm | 0.1 - 0.35 |
| Cores | Number of CPU cores to use | 1 - available cores |

## Monitoring Progress

To monitor the current simulation progress:
```sh
Get-Content -Wait -Path ./<job_name>.sta
```
Where `<job_name>` follows the format: `SAP<overlap>_<thickness>mu_<adhesive>`

## Output Files

- `.odb` files: Contains simulation results (one per scenario)
- `.sta` files: Contains simulation status and progress
- `.msg` files: Contains detailed simulation messages and any errors

## Monitoring

Monitor the current progress by running this code in a separate terminal at the root directory:

```sh
Get-Content -Wait -Path ./<part_name>.sta
```

## Stopping Simulations

To safely stop all running simulations:
```sh
python src/stop_abaqus.py
```

## Requirements

- Abaqus CAE with Python support
- Python packages (for parameter generation):
  - pandas
  - numpy
  - pyDOE3 (for LHS)

## See Also

- Main project README for overall workflow
- DOE folder README for parameter generation and model generation details