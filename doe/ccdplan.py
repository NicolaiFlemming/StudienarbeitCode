from pyDOE3 import ccdesign
import numpy as np
import pandas as pd
import os
import configparser
import sys
from pathlib import Path

# Read configuration
config = configparser.ConfigParser()

# Try different possible locations for config.ini
script_dir = Path(__file__).parent.resolve()
possible_config_paths = [
    script_dir.parent / 'config.ini',  # ../config.ini
    Path.cwd() / 'config.ini',         # ./config.ini
    Path.cwd().parent / 'config.ini'   # ../config.ini from working directory
]

config_found = False
for config_path in possible_config_paths:
    if config_path.is_file():
        config.read(str(config_path))
        config_found = True
        break

if not config_found:
    print("Error: config.ini not found. Tried the following locations:")
    for path in possible_config_paths:
        print(f"- {path}")
    sys.exit(1)

# Get values from config
Cores = config.getint('simulation', 'cpu_cores')
Adhesive = config.get('simulation', 'adhesive_type')

#create a central composite design with 2 factors and 2 center points, one for the factorial points and one for the axial points
design = ccdesign(2, center=(1, 1), face='ccc')

df = pd.DataFrame(design, columns=['X1', 'X2'])

factor_ranges = [
    (30, 60), #Overlap
    (0.1, 0.35) # Film_thickness
    ]

# Uncoding parameters for Overlap (X1)
min_X1, max_X1 = factor_ranges[0]
center_X1 = (max_X1 + min_X1) / 2
step_X1 = (max_X1 - min_X1) / 2

# Uncoding parameters for Film_thickness (X2)
min_X2, max_X2 = factor_ranges[1]
center_X2 = (max_X2 + min_X2) / 2
step_X2 = (max_X2 - min_X2) / 2

df['Overlap'] = (center_X1 + df['X1'] * step_X1).round(4)
df['Film_thickness'] = (center_X2 + df['X2'] * step_X2).round(4)

df2 = df[['Overlap', 'Film_thickness']]
df2['Adhesive'] = Adhesive
df2['Cores'] = Cores

# Try to find the correct inputs directory
script_dir = Path(__file__).parent.resolve()
possible_input_paths = [
    script_dir.parent / 'abaqus-sim' / 'inputs',  # ../abaqus-sim/inputs
    Path.cwd() / 'abaqus-sim' / 'inputs',         # ./abaqus-sim/inputs
    Path.cwd().parent / 'abaqus-sim' / 'inputs'   # ../abaqus-sim/inputs from working directory
]

input_dir = None
for path in possible_input_paths:
    if path.is_dir():
        input_dir = path
        break
    elif not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
            input_dir = path
            break
        except Exception as e:
            continue

if input_dir is None:
    print("Error: Could not find or create inputs directory. Tried the following locations:")
    for path in possible_input_paths:
        print(f"- {path}")
    sys.exit(1)

output_filename = str(input_dir / 'sim_params.csv')
export_df = df2[['Overlap', 'Adhesive', 'Film_thickness', 'Cores']]
export_df.to_csv(output_filename, index=False)