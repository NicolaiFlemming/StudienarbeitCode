from pyDOE3 import ccdesign
import numpy as np
import pandas as pd
import os

Cores = 28
Adhesive = 'AF163'  # 'AF163' or 'DP490'

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

output_path = 'abaqus-strapjoint-sim/inputs'
output_filename = os.path.join(output_path, 'sim_params.csv')

export_df = df2[['Overlap', 'Adhesive', 'Film_thickness', 'Cores']]
export_df.to_csv(output_filename, index=False)