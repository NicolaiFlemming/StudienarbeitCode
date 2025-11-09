# Abaqus Joint Simulation

This project automates the setup and execution of CFRP joint simulations in Abaqus using Python scripting. It provides a flexible framework for running both batch simulations and single-point analyses of strap joints (SAP) and stepped joints (SEP) with different adhesive types.

## Features

- Batch processing of multiple simulation scenarios
- Support for both Strap Joints (SAP) and Stepped Joints (SEP)
- Support for different adhesive materials (DP490, AF163)
- Configurable parameters (overlap length, adhesive thickness, joint type)
- Multi-core processing support
- Automatic file organization and naming

## File Structure

```text
abaqus-sim/
├── inputs/
│   ├── sim_params.csv         # CSV file with simulation parameters
│   └── sim_params_example.csv # Example parameter file for reference
├── src/
│   ├── run_simulations.py     # Main script to run single simulations
│   ├── run_batch.py          # Wrapper to run batch simulations
│   ├── stop_abaqus.py        # Utility to stop running simulations
│   ├── StrapJoint.py         # Strap joint (SAP) model and materials
│   └── SteppedJoint.py       # Stepped joint (SEP) model and materials
```

## Usage

### Batch Mode

1. Generate simulation parameters using either Design of Experiments (DOE) script:
   ```sh
   python ../doe/lhsplan.py  # Latin Hypercube Sampling
   # or
   python ../doe/ccdplan.py  # Central Composite Design
   ```

2. Configure joint type in `../config.ini`:
   ```ini
   [simulation]
   joint_type = SAP  # or SEP for stepped joints
   ```

3. Run batch simulations using the wrapper:
   ```sh
   python src/run_batch.py
   ```

### Single Point Mode

For running a single simulation with specific parameters:
```sh
abaqus cae noGui=src/run_simulations.py -- <overlap> <adhesive> <film_thickness> <cores> <joint_type>
```
Example (Strap Joint):
```sh
abaqus cae noGui=src/run_simulations.py -- 45.0 DP490 0.25 28 SAP
```
Example (Stepped Joint):
```sh
abaqus cae noGui=src/run_simulations.py -- 45.0 DP490 0.25 28 SEP
```

## Input Parameters

The `sim_params.csv` file contains the Design of Experiments (DOE) parameters:

| Column | Description | Range |
|--------|-------------|--------|
| Overlap | Joint overlap length in mm | 30.0 - 60.0 |
| Film_thickness | Adhesive thickness in mm | 0.1 - 0.35 |

Configuration parameters (same for all simulations) are in `../config.ini`:

| Parameter | Description | Options |
|-----------|-------------|---------|
| joint_type | Type of joint | 'SAP' (strap) or 'SEP' (stepped) |
| adhesive_type | Adhesive material | 'DP490' or 'AF163' |
| cpu_cores | Number of CPU cores | 1 - available cores |
| abaqus_command | Path to Abaqus | Full path to executable |

## Monitoring Progress

To monitor the current simulation progress:
```sh
Get-Content -Wait -Path ./<job_name>.sta
```
Where `<job_name>` follows the format: 
- Strap Joint: `SAP<overlap>_<thickness>mu_<adhesive>`
- Stepped Joint: `SEP<overlap>_<thickness>mu_<adhesive>`

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