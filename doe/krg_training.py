import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, RBF
import tkinter as tk
from tkinter import filedialog

def initialize_model():
    """Initialize the Gaussian Process model with default parameters."""
    # Kernel Definition: Anisotropic Matérn 5/2 kernel
    initial_length_scales = [1.0, 1.0]
    bounds_ls = (1e-2, 1e8)
    
    kernel = ConstantKernel(constant_value=1.0, constant_value_bounds=(1e-2, 1e5)) \
            * Matern(length_scale=initial_length_scales,
                    length_scale_bounds=bounds_ls,
                    nu=2.5)
    
    alpha_noise = 1e-10
    
    return GaussianProcessRegressor(
        kernel=kernel,
        alpha=alpha_noise,
        n_restarts_optimizer=100,
        random_state=42
    )

def load_and_process_data(file_path=None):
    """Load and preprocess the data from CSV file."""
    if file_path is None:
        # Use a file dialog to select the CSV file
        root = tk.Tk()
        root.withdraw()
        root.lift()
        root.focus_force()
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            print("No file selected. Exiting.")
            return None, None, None, None
    
    print(f"Loading data from: {file_path}")
    
    try:
        data = pd.read_csv(file_path)
        X_train = data[['Overlap_mm', 'Adhesive_Thickness_mm']].values
        Y_train = data['Max_RF1'].values
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        return X_train, Y_train, X_train_scaled, scaler
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None, None

def create_prediction_grid():
    """Create the prediction grid for the design space."""
    x1_min, x1_max = 30, 60  # Overlap range
    x2_min, x2_max = 0.1, 0.35  # Adhesive thickness range
    
    # Create grid points
    grid_x1 = np.linspace(x1_min, x1_max, 100)
    grid_x2 = np.linspace(x2_min, x2_max, 100)
    xx1, xx2 = np.meshgrid(grid_x1, grid_x2)
    
    # Flatten for prediction
    X_test = np.vstack([xx1.ravel(), xx2.ravel()]).T
    
    return X_test, xx1, xx2

def create_plots(xx1, xx2, X_train, Y_train, Y_pred_mean_grid, Y_pred_std_grid):
    """Create and save all visualization plots."""
    # Plot 1: Mean Prediction
    fig1 = plt.figure(figsize=(10, 8))
    ax1 = fig1.add_subplot(111)
    contour1 = ax1.contourf(xx1, xx2, Y_pred_mean_grid, levels=30, cmap='viridis')
    fig1.colorbar(contour1, ax=ax1, label='Predicted Max_RF1')
    ax1.scatter(X_train[:, 0], X_train[:, 1], c='red', edgecolors='k', s=40, label='Training Points')
    ax1.set_title('Kriging Mean Prediction (2D View)', fontsize=14)
    ax1.set_xlabel('Overlap_mm ($L_{lap}$)')
    ax1.set_ylabel('Adhesive_Thickness_mm ($t_{adh}$)')
    ax1.legend(loc='upper left')
    ax1.axis('tight')
    plt.tight_layout()
    plt.savefig('kriging_2d_prediction.svg')
    plt.close()
    
    # Plot 2: Uncertainty
    fig2 = plt.figure(figsize=(10, 8))
    ax2 = fig2.add_subplot(111)
    contour2 = ax2.contourf(xx1, xx2, Y_pred_std_grid, levels=30, cmap='plasma')
    fig2.colorbar(contour2, ax=ax2, label='Standard Deviation (σ)')
    ax2.scatter(X_train[:, 0], X_train[:, 1], c='red', edgecolors='k', s=40, label='Training Points')
    ax2.set_title('Kriging Prediction Uncertainty', fontsize=14)
    ax2.set_xlabel('Overlap_mm ($L_{lap}$)')
    ax2.set_ylabel('Adhesive_Thickness_mm ($t_{adh}$)')
    ax2.legend(loc='upper left')
    ax2.axis('tight')
    plt.tight_layout()
    plt.savefig('kriging_uncertainty.svg')
    plt.close()
    
    # Plot 3: 3D Surface
    fig3 = plt.figure(figsize=(12, 10))
    ax3 = fig3.add_subplot(111, projection='3d')
    surf = ax3.plot_surface(xx1, xx2, Y_pred_mean_grid, cmap='viridis', alpha=0.8)
    
    zmin = Y_pred_mean_grid.min()
    offset = zmin - (Y_pred_mean_grid.max() - zmin) * 0.1
    ax3.contourf(xx1, xx2, Y_pred_mean_grid, zdir='z', offset=offset, levels=20, cmap='viridis')
    ax3.scatter(X_train[:, 0], X_train[:, 1], Y_train, c='red', marker='o', s=40, edgecolors='k', label='Training Points')
    
    ax3.set_zlim(offset, Y_pred_mean_grid.max())
    ax3.set_xlabel('Overlap_mm ($L_{lap}$)')
    ax3.set_ylabel('Adhesive_Thickness_mm ($t_{adh}$)')
    ax3.set_zlabel('Predicted Max_RF1')
    ax3.set_title('Kriging 3D Response Surface', fontsize=14)
    
    fig3.colorbar(surf, shrink=0.5, aspect=5, label='Predicted Max_RF1')
    plt.tight_layout()
    plt.savefig('kriging_3d_surface.svg')
    if plt.get_fignums():
        plt.show()
    plt.close()

def train_and_predict_kriging(file_path=None, show_plots=False):
    """Train the Kriging model and return the point of highest uncertainty."""
    # Load and process data
    X_train, Y_train, X_train_scaled, scaler = load_and_process_data(file_path)
    if X_train is None:
        return None
    
    # Initialize and train model
    gp = initialize_model()
    gp.fit(X_train_scaled, Y_train)
    
    # Create prediction grid
    X_test, xx1, xx2 = create_prediction_grid()
    X_test_scaled = scaler.transform(X_test)
    
    # Make predictions
    Y_pred_mean, Y_pred_std = gp.predict(X_test_scaled, return_std=True)
    Y_pred_mean_grid = Y_pred_mean.reshape(xx1.shape)
    Y_pred_std_grid = Y_pred_std.reshape(xx1.shape)
    
    # Find point of maximum uncertainty
    max_std_idx = np.argmax(Y_pred_std_grid)
    max_std_x1 = xx1.ravel()[max_std_idx]
    max_std_x2 = xx2.ravel()[max_std_idx]
    max_std_value = Y_pred_std_grid.ravel()[max_std_idx]
    
    print(f"\nMaximum Uncertainty Point:")
    print(f"Overlap = {max_std_x1:.2f} mm")
    print(f"Adhesive Thickness = {max_std_x2:.2f} mm")
    print(f"Standard Deviation = {max_std_value:.2f}")
    
    if show_plots:
        create_plots(xx1, xx2, X_train, Y_train, Y_pred_mean_grid, Y_pred_std_grid)
    
    return max_std_x1, max_std_x2, max_std_value

if __name__ == '__main__':
    train_and_predict_kriging(show_plots=True)