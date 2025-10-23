import numpy as np
import pandas as pd
# You will need to install pyDOE if you don't have it (pip install pyDOE)
from pyDOE3 import lhs 
import os 

Cores = 28
Adhesive = 'DP490'  # 'AF163' or 'DP490'

# Define the number of factors (d) and the number of samples (n)
d = 2  # Number of factors (Overlap, Film_thickness)
# Number of samples
n = 15 * d # n = 30

# --- 1. Generate the Latin Hypercube Design (LHS) ---
# 'm' for maximin (minimax) distance criterion, ensuring optimal space-filling.
design = lhs(d, samples=n, criterion='m', iterations=1000) # Increased iterations for better quality

# --- 2. Convert the normalized design to a DataFrame ---
df = pd.DataFrame(design, columns=['X1', 'X2'])

# --- 3. Define Factor Ranges ---
factor_ranges = [
    (30, 60),    # X1: Overlap (mm)
    (0.1, 0.35)  # X2: Film_thickness (mm)
    ]

# --- 4. Scale the Normalized Design to the Actual Ranges ---
def scale_factors(df, ranges):
    """Scales the normalized (0-1) LHS points to the actual factor ranges."""
    df_scaled = df.copy()
    for i, (min_val, max_val) in enumerate(ranges):
        # Scale: actual = min + (max - min) * normalized
        factor_name = df_scaled.columns[i]
        df_scaled[factor_name] = min_val + (max_val - min_val) * df_scaled[factor_name]
    return df_scaled

df_final = scale_factors(df, factor_ranges)

# Create the final DataFrame with the required columns
output_df = pd.DataFrame({
    'Overlap': df_final['X1'].round(4),
    'Adhesive': [Adhesive] * len(df_final),
    'Film_thickness': df_final['X2'].round(4),
    'Cores': [Cores] * len(df_final)
})

# Export to CSV
output_path = 'abaqus-strapjoint-sim/inputs'
output_filename = os.path.join(output_path, 'sim_params.csv')

output_df.to_csv(output_filename, index=False)
print(f"\nExported to {output_filename} with the following format:")
print(output_df)
