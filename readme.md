# CFRP Strap Joint Analysis Framework

This repository contains a comprehensive framework for analyzing Carbon Fiber Reinforced Polymer (CFRP) strap joints using a combination of Finite Element Method (FEM) simulations and surrogate modeling techniques.

## Project Structure

```text
StudienarbeitCode/
├── abaqus-strapjoint-sim/    # FEM simulation framework
│   ├── inputs/               # Simulation parameters and inputs
│   └── src/                  # Abaqus Python scripts
├── doe/                      # Design of Experiments
│   ├── ccdplan.py           # Central Composite Design generator
│   └── lhsplan.py           # Latin Hypercube Sampling generator
├── modeling/                 # Surrogate modeling and analysis
│   ├── extract_values.py    # Extract results from ODB files
│   ├── extract_rf1_single.py # Extract RF1 from single ODB file
│   ├── krg_training.py      # Kriging model training and plots
│   ├── krg_optimization.py  # Kriging-based optimization
│   ├── rsm_mapping.py       # Response Surface Methodology mapping
│   └── rsm_verification.py  # RSM model verification
└── config.ini               # Centralized configuration file
```

## Features

### FEM Simulation
- Automated Abaqus CAE simulations
- Support for multiple adhesive types (DP490, AF163)
- Parametric joint geometry
- Multi-core processing support
- Batch processing capabilities

### Design of Experiments
- Latin Hypercube Sampling (LHS)
- Central Composite Design (CCD)
- Parameter space exploration

### Surrogate Modeling
- Response Surface Methodology (RSM)
  - Second-order polynomial response surface
  - Verification and mapping tools
- Kriging Models
  - Gaussian process regression
  - Model training and optimization
  - Uncertainty quantification
  - Plot generation

## Configuration

The project uses a centralized `config.ini` file for key parameters:

```ini
[simulation]
adhesive_type = DP490  # or AF163
cpu_cores = 28

[optimization]
n_iterations = 5
```

## Workflow

### 1. Configuration
Update `config.ini` with your desired settings:
- Set adhesive type (DP490 or AF163)
- Configure CPU cores for simulations
- Set optimization iterations

### 2. Generate Input Parameters
Create input parameter CSV file using either:

```sh
python doe/lhsplan.py  # Latin Hypercube Sampling
# or
python doe/ccdplan.py  # Central Composite Design
```

This generates `abaqus-strapjoint-sim/inputs/sim_params.csv`

### 3. Run FEM Simulations
Execute Abaqus simulations as described in `abaqus-strapjoint-sim/readme.md`:

```sh
cd abaqus-strapjoint-sim
abaqus cae noGui=src/run_simulations.py
```

### 4. Extract Results
Extract results from ODB files:

```sh
python modeling/extract_values.py
```

Select the ODB files and specify output location when prompted.

### 5. Surrogate Modeling

#### For Response Surface Models (RSM)
Continue with the RSM mapping script:

```sh
python modeling/rsm_mapping.py
```

This will generate:

- 2D contour plots
- 3D surface plots with contours
- RSM model equations and statistics

#### For Kriging Models (KRG)
a. Run optimization to identify optimal sampling points:

```sh
python modeling/krg_optimization.py
```

This performs iterative optimization to find points with maximum uncertainty.

b. After optimization, generate plots:

```sh
python modeling/krg_training.py
```

This will generate:

- Response surface predictions
- Uncertainty maps
- Validation plots

## Requirements

### Software
- Abaqus CAE 2025
- Python 3.x

### Python Packages
- pandas
- numpy
- scipy
- pyDOE3
- matplotlib
- statsmodels
- scikit-learn (for Kriging models)

## Getting Started

1. Clone the repository
2. Configure `config.ini` with your settings
3. Install required Python packages:
   ```sh
   pip install pandas numpy scipy pyDOE3 matplotlib statsmodels scikit-learn
   ```
4. Follow the workflow steps above

## Documentation

- See `abaqus-strapjoint-sim/readme.md` for detailed simulation setup and troubleshooting
- Individual script files contain additional documentation
- Check error messages and log files for debugging

## Tips

- Start with a small number of samples to test the workflow
- Monitor disk space - simulation files can be large
- Use LHS for Kriging surrogate models, CCD for response surface fitting
- Verify RSM models with `rsm_verification.py` before using predictions
- Kriging optimization iteratively adds points where uncertainty is highest

