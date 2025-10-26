import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern , RBF
import tkinter as tk
from tkinter import filedialog

# --- Step 1: Data Structure and Preprocessing ---

print("Step 1: Loading and Preprocessing Data")

# Define the file path
# Use a file dialog to select the CSV file
root = tk.Tk()
root.withdraw()  # hide the main window
root.lift()  # Bring the dialog to front
root.focus_force()  # Force focus on the dialog
FILE_PATH = filedialog.askopenfilename(
    title="Select CSV file",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)

if not FILE_PATH:
    print("No file selected. Exiting.")
    exit()

# Load the data using pandas
try:
    data = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print(f"Error: The file '{FILE_PATH}' was not found.")
    print("Please make sure the CSV file is in the same directory as the script.")
    exit()

# Extract Input Matrix (Xtrain) and Output Vector (Ytrain)
# Xtrain: [Overlap_mm, Adhesive_Thickness_mm]
X_train = data[['Overlap_mm', 'Adhesive_Thickness_mm']].values
# Ytrain: Max_RF1
Y_train = data['Max_RF1'].values

print(f"Loaded {X_train.shape[0]} training samples.")
print(f"Input shape (X_train): {X_train.shape}")
print(f"Output shape (Y_train): {Y_train.shape}")

# Crucial preprocessing: Standardizing to zero mean and unit variance
# This scaler will be used to transform both the training and test data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

print("\nData preprocessing complete (StandardScaler).")


# --- Step 2: Selecting and Configuring the GaussianProcessRegressor ---

print("\nStep 2: Configuring the Kernel and Noise Term")

# Kernel Definition: Anisotropic Matérn 5/2 kernel
# Define initial length scales for the two dimensions [Overlap_mm, Adhesive_Thickness_mm]
initial_length_scales = [1.0, 1.0] 
bounds_ls = (1e-2, 1e5) # Define bounds for optimization

# Matern Kernel
kernel = ConstantKernel(constant_value=1.0, constant_value_bounds=(1e-2, 1e5)) \
         * Matern(length_scale=initial_length_scales, 
                  length_scale_bounds=bounds_ls, 
                  nu=2.5) # nu=2.5 corresponds to Matern 5/2

# RBF Kernel as alternative (significantly worse performance)
# kernel = ConstantKernel(constant_value=1.0, constant_value_bounds=(1e-2, 1e5)) \
#          * RBF(length_scale=initial_length_scales, 
#                length_scale_bounds=bounds_ls)

# Noise Term (alpha) for deterministic FEM data (Kriging normally assumes alpha=0)
alpha_noise = 1e-10 

print(f"Kernel: {kernel}")
print(f"Alpha (noise): {alpha_noise}")


# --- Step 3: Step-by-Step Model Training and Optimization ---

print("\nStep 3: Initializing and Training the GPR Model")

# Initialize GPR with defined kernel and numerical noise term
# Use a high number of restarts to find the global maximum of the LML
gp = GaussianProcessRegressor(kernel=kernel, 
                              alpha=alpha_noise, 
                              n_restarts_optimizer=100, # Increased restarts for better optimization
                              random_state=42)

print(f"GaussianProcessRegressor initialized with {gp.n_restarts_optimizer} optimizer restarts.")
print("Fitting model to the (scaled) training data...")

# Fitting (Optimization): Maximize the LML
gp.fit(X_train_scaled, Y_train)

print("Model fitting complete.")
print(f"Optimized Kernel Parameters: {gp.kernel_}")
print(f"Log-Marginal-Likelihood (LML): {gp.log_marginal_likelihood(gp.kernel_.theta):.3f}")


# --- Step 4: Prediction and Uncertainty Quantification ---

print("\nStep 4: Prediction on a Dense Grid and Visualization")

# 1. Generate a dense grid X_test covering the 2D design space
# We use the parameter ranges
x1_min, x1_max = 30, 60 #Overlap range
x2_min, x2_max = 0.1, 0.35 #Adhesive thickness range

# Add a small padding to the grid to see beyond the training points
x1_pad = (x1_max - x1_min) * 0.1
x2_pad = (x2_max - x2_min) * 0.1

# Create 100 points for each dimension
grid_x1 = np.linspace(x1_min, x1_max, 100)
grid_x2 = np.linspace(x2_min, x2_max, 100)

# Create the meshgrid
xx1, xx2 = np.meshgrid(grid_x1, grid_x2)

# Flatten the grid into an (N_test, 2) array for prediction
X_test = np.vstack([xx1.ravel(), xx2.ravel()]).T

# 2. Preprocess the test grid *using the same scaler*
X_test_scaled = scaler.transform(X_test)
print(f"Created prediction grid with {X_test.shape[0]} test points.")

# 3. Use the predict method
Y_pred_mean, Y_pred_std = gp.predict(X_test_scaled, return_std=True)

# 4. Reshape predictions back to grid shape for plotting
Y_pred_mean_grid = Y_pred_mean.reshape(xx1.shape)
Y_pred_std_grid = Y_pred_std.reshape(xx1.shape)

print("Prediction complete.")

# Find the point of maximum uncertainty
max_std_idx = np.argmax(Y_pred_std_grid)
max_std_x1 = xx1.ravel()[max_std_idx]
max_std_x2 = xx2.ravel()[max_std_idx]
max_std_value = Y_pred_std_grid.ravel()[max_std_idx]

print(f"\nMaximum Uncertainty Point:")
print(f"Overlap = {max_std_x1:.2f} mm")
print(f"Adhesive Thickness = {max_std_x2:.2f} mm")
print(f"Standard Deviation = {max_std_value:.2f}")

print("\nPlotting results...")

# Plot 1: Mean Prediction (BLUP) - 2D Contour
fig1 = plt.figure(figsize=(10, 8))
ax1 = fig1.add_subplot(111)
contour1 = ax1.contourf(xx1, xx2, Y_pred_mean_grid, levels=30, cmap='viridis')
fig1.colorbar(contour1, ax=ax1, label='Predicted Max_RF1')
# Overlay the original training points
ax1.scatter(X_train[:, 0], X_train[:, 1], c='red', edgecolors='k', s=40, label='Training Points')
ax1.set_title('Kriging Mean Prediction (2D View)', fontsize=14)
ax1.set_xlabel('Overlap_mm ($L_{lap}$)')
ax1.set_ylabel('Adhesive_Thickness_mm ($t_{adh}$)')
ax1.legend(loc='upper left')
ax1.axis('tight')
plt.tight_layout()
plt.savefig('kriging_2d_prediction.svg')
plt.close()

# Plot 2: Standard Deviation (Uncertainty)
fig2 = plt.figure(figsize=(10, 8))
ax2 = fig2.add_subplot(111)
contour2 = ax2.contourf(xx1, xx2, Y_pred_std_grid, levels=30, cmap='plasma')
fig2.colorbar(contour2, ax=ax2, label='Standard Deviation (σ)')
# Overlay the original training points
ax2.scatter(X_train[:, 0], X_train[:, 1], c='red', edgecolors='k', s=40, label='Training Points')
ax2.set_title('Kriging Prediction Uncertainty', fontsize=14)
ax2.set_xlabel('Overlap_mm ($L_{lap}$)')
ax2.set_ylabel('Adhesive_Thickness_mm ($t_{adh}$)')
ax2.legend(loc='upper left')
ax2.axis('tight')
plt.tight_layout()
plt.savefig('kriging_uncertainty.svg')
plt.close()

# Plot 3: 3D Surface Plot with base contour
fig3 = plt.figure(figsize=(12, 10))
ax3 = fig3.add_subplot(111, projection='3d')

# Plot the surface
surf = ax3.plot_surface(xx1, xx2, Y_pred_mean_grid, cmap='viridis', alpha=0.8)

# Add filled contour plot at the base
zmin = Y_pred_mean_grid.min()
offset = zmin - (Y_pred_mean_grid.max() - zmin) * 0.1
contour3 = ax3.contourf(xx1, xx2, Y_pred_mean_grid,
                       zdir='z', offset=offset, levels=20, cmap='viridis')

# Plot the actual data points in 3D
scatter = ax3.scatter(X_train[:, 0], X_train[:, 1], Y_train,
                     c='red', marker='o', s=40, edgecolors='k', label='Training Points')

# Adjust the z-axis limits to accommodate the contour plot
ax3.set_zlim(offset, Y_pred_mean_grid.max())

# Add labels
ax3.set_xlabel('Overlap_mm ($L_{lap}$)')
ax3.set_ylabel('Adhesive_Thickness_mm ($t_{adh}$)')
ax3.set_zlabel('Predicted Max_RF1')
ax3.set_title('Kriging 3D Response Surface', fontsize=14)

# Add colorbar for the 3D plot
fig3.colorbar(surf, shrink=0.5, aspect=5, label='Predicted Max_RF1')

plt.tight_layout()
plt.savefig('kriging_3d_surface.svg')
plt.show()

print("\nScript finished.")