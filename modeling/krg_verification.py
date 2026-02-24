import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import matplotlib.pyplot as plt

# Import functions from krg_training script
from krg_training import initialize_model, load_and_process_data

# --- Function definitions ---

def calculate_rmse(actual: list, predicted: list) -> float:
    """
    Calculates the Root Mean Square Error (RMSE).
    RMSE = sqrt( mean( (actual - predicted)^2 ) )
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    if actual.size == 0 or actual.size != predicted.size:
        raise ValueError("Inputs must be non-empty and of the same size.")

    return np.sqrt(np.mean((actual - predicted)**2))

def calculate_mape(actual: list, predicted: list) -> float:
    """
    Calculates the Mean Absolute Percentage Error (MAPE).
    MAPE = mean( | (actual - predicted) / actual | ) * 100%
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    if actual.size == 0 or actual.size != predicted.size:
        raise ValueError("Inputs must be non-empty and of the same size.")
    
    # Check for division by zero (actual values of 0)
    if np.any(actual == 0):
        print("Warning: Division by zero is a possibility. MAPE is sensitive to actual values close to zero.")

    # Note: MAPE uses the absolute value of (actual - predicted) / actual
    return np.mean(np.abs((actual - predicted) / actual)) * 100

def calculate_mae(actual: list, predicted: list) -> float:
    """
    Calculates the Mean Absolute Error (MAE).
    MAE = mean( |actual - predicted| )
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    if actual.size == 0 or actual.size != predicted.size:
        raise ValueError("Inputs must be non-empty and of the same size.")
        
    return np.mean(np.abs(actual - predicted))

def plot_kriging_model_with_test_points_3d(
    gp,
    x_scaler,
    y_scaler,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    output_dir: str,
) -> str:
    """Create and save a 3D plot of Kriging model surface and test data points."""
    overlap_all = np.concatenate([
        train_df['Overlap_mm'].values,
        test_df['Overlap_mm'].values,
    ])
    thickness_all = np.concatenate([
        train_df['Adhesive_Thickness_mm'].values,
        test_df['Adhesive_Thickness_mm'].values,
    ])

    x1_min, x1_max = overlap_all.min(), overlap_all.max()
    x2_min, x2_max = thickness_all.min(), thickness_all.max()

    x1_margin = max((x1_max - x1_min) * 0.05, 0.5)
    x2_margin = max((x2_max - x2_min) * 0.05, 0.005)

    grid_x1 = np.linspace(x1_min - x1_margin, x1_max + x1_margin, 80)
    grid_x2 = np.linspace(x2_min - x2_margin, x2_max + x2_margin, 80)
    xx1, xx2 = np.meshgrid(grid_x1, grid_x2)
    X_grid = np.column_stack([xx1.ravel(), xx2.ravel()])

    X_grid_scaled = x_scaler.transform(X_grid)
    y_grid_scaled = gp.predict(X_grid_scaled)
    y_grid = y_scaler.inverse_transform(y_grid_scaled.reshape(-1, 1)).ravel()
    zz = y_grid.reshape(xx1.shape)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(xx1, xx2, zz, cmap='viridis', alpha=0.75, linewidth=0)
    fig.colorbar(surf, ax=ax, shrink=0.6, aspect=16, label='Predicted Max RF1 (N)')

    ax.scatter(
        test_df['Overlap_mm'].values,
        test_df['Adhesive_Thickness_mm'].values,
        test_df['Max_RF1'].values,
        c='red',
        marker='s',
        s=55,
        edgecolors='black',
        linewidth=0.6,
        alpha=0.95,
        label='Test Data Points',
    )

    ax.set_xlabel('Overlap_mm ($L_{lap}$)')
    ax.set_ylabel('Adhesive_Thickness_mm ($t_{adh}$)')
    ax.set_zlabel('Max RF1 (N)')
    ax.set_title('Kriging Model Surface with Test Data Points (3D)', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left')

    plt.tight_layout()

    plot_path = os.path.join(output_dir, 'krg_model_with_test_points_3d.svg')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.show()

    return plot_path

def main():
    """Main function to perform Kriging model verification."""
    print("=" * 70)
    print("Kriging Model Verification")
    print("=" * 70)
    
    # Step 1: Select training data (results.csv)
    print("\nStep 1: Select TRAINING data file (e.g., results.csv)")
    root = tk.Tk()
    root.withdraw()
    
    training_file = filedialog.askopenfilename(
        title="Select Training Data CSV (results.csv)",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if not training_file:
        print("No training file selected. Exiting.")
        return
    
    # Step 2: Select test data
    print("\nStep 2: Select TEST data file (extracted from ODB files)")
    test_file = filedialog.askopenfilename(
        title="Select Test Data CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if not test_file:
        print("No test file selected. Exiting.")
        return
    
    # Step 3: Read data
    print(f"\nReading training data from: {os.path.basename(training_file)}")
    train_df = pd.read_csv(training_file)
    print(f"Training set: {len(train_df)} points")
    
    print(f"\nReading test data from: {os.path.basename(test_file)}")
    test_df = pd.read_csv(test_file)
    print(f"Test set: {len(test_df)} points")

    # Prepare output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 4: Load and process training data using krg_training function
    print("\nProcessing training data...")
    X_train, Y_train, X_train_scaled, Y_train_scaled, x_scaler, y_scaler, _ = load_and_process_data(training_file)
    
    if X_train is None:
        print("Error processing training data. Exiting.")
        return
    
    # Step 5: Train Kriging model
    print("\n" + "=" * 70)
    print("Training Kriging Model...")
    print("=" * 70)
    
    gp = initialize_model()
    gp.fit(X_train_scaled, Y_train_scaled.ravel())
    
    # Extract hyperparameters
    optimized_kernel = gp.kernel_
    print("\nOptimized Hyperparameters:")
    # Note: kernel structure is now (ConstantKernel * Matern) + WhiteKernel
    # k1 is the sum, k1.k1 is the product, k1.k2 is WhiteKernel
    print(f"  Constant value: {optimized_kernel.k1.k1.constant_value:.4f}")
    print(f"  Length scale (Overlap): {optimized_kernel.k1.k2.length_scale[0]:.4f}")
    print(f"  Length scale (Thickness): {optimized_kernel.k1.k2.length_scale[1]:.4f}")
    print(f"  Nu (Matern): {optimized_kernel.k1.k2.nu:.2f}")
    print(f"  Noise level (WhiteKernel): {optimized_kernel.k2.noise_level:.4e}")
    print(f"  Log-Marginal-Likelihood: {gp.log_marginal_likelihood_value_:.2f}")
    
    # Step 6: Predict on test data
    print("\n" + "=" * 70)
    print("Testing Kriging Model on Test Data")
    print("=" * 70)
    
    X_test = test_df[['Overlap_mm', 'Adhesive_Thickness_mm']].values
    X_test_scaled = x_scaler.transform(X_test)
    
    # Predict in scaled space
    Y_pred_scaled, Y_pred_std_scaled = gp.predict(X_test_scaled, return_std=True)
    
    # Transform back to original scale
    Y_pred = y_scaler.inverse_transform(Y_pred_scaled.reshape(-1, 1)).ravel()
    Y_pred_std = Y_pred_std_scaled * y_scaler.scale_[0]
    
    actuals = test_df['Max_RF1'].values
    predictions = Y_pred

    # Step 7: Create 3D model surface plot with test points
    print("\n" + "=" * 70)
    print("Generating 3D Plot: Kriging Model + Test Data Points")
    print("=" * 70)
    model_3d_plot_path = plot_kriging_model_with_test_points_3d(
        gp, x_scaler, y_scaler, train_df, test_df, output_dir
    )
    print(f"\n3D model plot saved to: {model_3d_plot_path}")
    
    print(f"\n{'Overlap':>10} | {'Thickness':>10} | {'Actual RF1':>12} | {'Predicted RF1':>14} | {'Std Dev':>10} | {'Error':>10} | {'Error %':>10}")
    print("-" * 100)
    
    for i in range(len(test_df)):
        overlap = test_df.iloc[i]['Overlap_mm']
        thickness = test_df.iloc[i]['Adhesive_Thickness_mm']
        actual_rf1 = actuals[i]
        predicted_rf1 = predictions[i]
        std_dev = Y_pred_std[i]
        
        error = actual_rf1 - predicted_rf1
        error_pct = (abs(error) / actual_rf1) * 100
        
        print(f"{overlap:10.2f} | {thickness:10.4f} | {actual_rf1:12.2f} | {predicted_rf1:14.2f} | {std_dev:10.2f} | {error:10.2f} | {error_pct:9.2f}%")
    
    # Step 8: Calculate error metrics
    rmse = calculate_rmse(actuals, predictions)
    mape = calculate_mape(actuals, predictions)
    mae = calculate_mae(actuals, predictions)
    
    # Calculate Kriging-specific standardized error metrics
    residuals = actuals - predictions
    standardized_residuals = residuals / Y_pred_std
    
    # Mean Standardized Error (should be ~0)
    mse = np.mean(standardized_residuals)
    
    # Root Mean Square Standardized Error (should be ~1)
    rmsse = np.sqrt(np.mean(standardized_residuals**2))
    
    print("\n" + "=" * 70)
    print("Error Metrics")
    print("=" * 70)
    print(f"RMSE (Root Mean Square Error):    {rmse:10.2f} N")
    print(f"MAE  (Mean Absolute Error):       {mae:10.2f} N")
    print(f"MAPE (Mean Absolute % Error):     {mape:10.2f} %")
    print("\n" + "Kriging Confidence Validation:")
    print(f"MSE  (Mean Standardized Error):   {mse:10.4f}  (target: ~0)")
    print(f"RMSSE (Root Mean Sq. Std. Error): {rmsse:10.4f}  (target: ~1)")
    print("=" * 70)
    
    # Step 9: Create actual vs predicted scatter plot
    print("\n" + "=" * 70)
    print("Generating Actual vs Predicted Scatter Plot...")
    print("=" * 70)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Scatter plot
    ax.scatter(actuals, predictions, c='red', s=20, alpha=0.8, marker='s', label='Test Points')
    
    # Perfect prediction line (y = x)
    min_val = min(actuals.min(), predictions.min())
    max_val = max(actuals.max(), predictions.max())
    ax.plot([min_val, max_val], [min_val, max_val], 
            'k--', linewidth=1, label='Perfect Prediction (y = x)')
    
    # Labels and title
    ax.set_xlabel('Actual Max RF1 (N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Predicted Max RF1 (N)', fontsize=12, fontweight='bold')
    ax.set_title('Kriging Model: Actual vs Predicted Values', fontsize=14, fontweight='bold')
    
    # Add error metrics to plot
    textstr = f'RMSE = {rmse:.2f} N\nMAE = {mae:.2f} N\nMAPE = {mape:.2f}%\n\nMSE = {mse:.4f}\nRMSSE = {rmsse:.4f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
    
    ax.legend(fontsize=10, loc='lower right')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    # Save plot
    plot_path = os.path.join(output_dir, 'krg_actual_vs_predicted.svg')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nActual vs Predicted plot saved to: {plot_path}")
    
    plt.show()
    
    # Step 10: Create residual plot
    print("\n" + "=" * 70)
    print("Generating Residual Plot...")
    print("=" * 70)
    
    # Calculate residuals
    residuals = actuals - predictions
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Scatter plot
    ax.scatter(predictions, residuals, c='red', s=20, alpha=0.8, marker='s', label='Residuals')
    
    # Zero line (ideal residual)
    ax.axhline(y=0, color='k', linestyle='--', linewidth=1, label='Zero Residual')
    
    # Labels and title
    ax.set_xlabel('Predicted Max RF1 (N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Residuals (Actual - Predicted) (N)', fontsize=12, fontweight='bold')
    ax.set_title('Kriging Model: Residual Plot', fontsize=14, fontweight='bold')
    
    # Add statistics to plot
    residual_mean = np.mean(residuals)
    residual_std = np.std(residuals)
    textstr = f'Mean = {residual_mean:.2f} N\nStd Dev = {residual_std:.2f} N'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
    
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    # Save plot
    residual_plot_path = os.path.join(output_dir, 'krg_residual_plot.svg')
    plt.savefig(residual_plot_path, dpi=300, bbox_inches='tight')
    print(f"\nResidual plot saved to: {residual_plot_path}")
    
    plt.show()

if __name__ == '__main__':
    main()


##Important metrics to look out for:
#Low Error Metrics (RMSE, MAE, MAPE)
#Low prediction uncertainty (standard deviation)
#MSE (Mean Standardized Error) close to 0 - validates unbiased predictions
#RMSSE (Root Mean Square Standardized Error) close to 1 - validates confidence intervals are properly calibrated
#Good visuals in actual vs predicted and residual plots (actual values closely follow y=x line; residuals randomly scattered around zero)
