import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

factor_ranges = [
    (30, 60), #Overlap
    (0.1, 0.35) # Film_thickness
    ]



root = tk.Tk()
root.withdraw()  # Hide the main window

file_name = filedialog.askopenfilename(
    title="Select results .csv file",
    filetypes=[("CSV files", "*.csv")]
)
df = pd.read_csv(file_name)

# Uncoding parameters for Overlap (X1)
min_X1, max_X1 = factor_ranges[0]
center_X1 = (max_X1 + min_X1) / 2
step_X1 = (max_X1 - min_X1) / 2

# Uncoding parameters for Film_thickness (X2)
min_X2, max_X2 = factor_ranges[1]
center_X2 = (max_X2 + min_X2) / 2
step_X2 = (max_X2 - min_X2) / 2

# =====================================================================
# 2. Calculate Coded Variables (X_c = (X_u - Center) / Step)
# =====================================================================
df['X1'] = (df['Overlap_mm'] - center_X1) / step_X1
df['X2'] = (df['Adhesive_Thickness_mm'] - center_X2) / step_X2

# 3. Fit the Second-Order Model using Coded Variables
# Formula: Y = B0 + B1*X1 + B2*X2 + B11*X1^2 + B22*X2^2 + B12*X1*X2
rsm_formula_coded = (
    'Max_RF1 ~ X1 + X2 + I(X1**2) + I(X2**2) + X1:X2'
)

# Fit the model
model_coded = smf.ols(formula=rsm_formula_coded, data=df)
rsm_fit_coded = model_coded.fit()

# 4. Analyze the Results
print("\n--- RSM Model Summary (Using Coded Variables) ---")
print(rsm_fit_coded.summary())

# Generate the Coded Response Surface Equation for clarity
params_coded = rsm_fit_coded.params
equation_coded = (
    f"Max_RF1 = {params_coded.get('Intercept', 0):.2f} "
    f"+ ({params_coded.get('X1', 0):.2f} * X1) "
    f"+ ({params_coded.get('X2', 0):.2f} * X2) "
    f"+ ({params_coded.get('I(X1 ** 2)', 0):.2f} * X1^2) "
    f"+ ({params_coded.get('I(X2 ** 2)', 0):.2f} * X2^2) "
    f"+ ({params_coded.get('X1:X2', 0):.2f} * X1*X2)"
)
print("\n--- Final Regression Equation (Coded RSM) ---")
print(equation_coded)

# =====================================================================
# 4. Create Prediction Grid
# =====================================================================
# Create a grid for prediction using UNCODED (actual) values for plotting axes
X1_range_u = np.linspace(df['Overlap_mm'].min(), df['Overlap_mm'].max(), 50)
X2_range_u = np.linspace(df['Adhesive_Thickness_mm'].min(), df['Adhesive_Thickness_mm'].max(), 50)
X1_grid_u, X2_grid_u = np.meshgrid(X1_range_u, X2_range_u)

# Convert the UNCODED grid points to CODED values for prediction input
X1_grid_c = (X1_grid_u - center_X1) / step_X1
X2_grid_c = (X2_grid_u - center_X2) / step_X2

pred_df_coded = pd.DataFrame({
    'X1': X1_grid_c.ravel(),
    'X2': X2_grid_c.ravel()
})

# Predict the response (Max_RF1)
Y_pred = rsm_fit_coded.predict(pred_df_coded).values.reshape(X1_grid_u.shape)

# =====================================================================
# 5. Generate 2D Contour Plot
# =====================================================================
plt.figure(figsize=(10, 8))
contour = plt.contourf(X1_grid_u, X2_grid_u, Y_pred, levels=20, cmap='viridis')
plt.colorbar(contour, label='Predicted Max_RF1 (N)')
plt.scatter(df['Overlap_mm'], df['Adhesive_Thickness_mm'], c='red', edgecolors='k', s=50, label='Actual Data Points')
plt.xlabel('Overlap (mm)')
plt.ylabel('Adhesive Thickness (mm)')
plt.title('2D Response Surface Contour Plot (Coded Model)')
plt.legend()
plt.savefig('rsm_2d_contour_plot.png')
plt.close() # Close plot figure

# =====================================================================
# 6. Generate 3D Response Surface Plot
# =====================================================================
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
ax.plot_surface(X1_grid_u, X2_grid_u, Y_pred, cmap='viridis', alpha=0.8)

# Plot the actual data points
ax.scatter(df['Overlap_mm'], df['Adhesive_Thickness_mm'], df['Max_RF1'],
           c='red', marker='o', s=50, label='Actual Data')

ax.set_xlabel('Overlap (mm)')
ax.set_ylabel('Adhesive Thickness (mm)')
ax.set_zlabel('Predicted Max_RF1 (N)')
ax.set_title('3D Response Surface Plot (Coded Model)')
ax.legend()
plt.savefig('rsm_3d_surface_plot.png')
plt.show()