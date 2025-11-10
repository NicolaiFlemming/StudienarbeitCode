import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import tkinter as tk
from tkinter import filedialog
import os
import matplotlib.pyplot as plt

# --- Function definitions ---

def to_coded(x, x_center, x_half_range):
    """Convert real value to coded variable."""
    return (x - x_center) / x_half_range


def fit_rsm_model(df, x1_center, x1_half, x2_center, x2_half):
    """Fit RSM model to training data and return the fitted model."""
    # Calculate coded variables
    df['X1'] = (df['Overlap_mm'] - x1_center) / x1_half
    df['X2'] = (df['Adhesive_Thickness_mm'] - x2_center) / x2_half
    
    # Fit the second-order model
    rsm_formula = 'Max_RF1 ~ X1 + X2 + I(X1**2) + I(X2**2) + X1:X2'
    model = smf.ols(formula=rsm_formula, data=df)
    rsm_fit = model.fit()
    
    return rsm_fit

def predict_from_rsm(rsm_fit, x1_real, x2_real, x1_center, x1_half, x2_center, x2_half):
    """Predict Max_RF1 using the fitted RSM model."""
    X1 = to_coded(x1_real, x1_center, x1_half)
    X2 = to_coded(x2_real, x2_center, x2_half)
    
    pred_df = pd.DataFrame({'X1': [X1], 'X2': [X2]})
    prediction = rsm_fit.predict(pred_df).values[0]
    
    return prediction

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

def main():
    """Main function to perform RSM verification."""
    print("=" * 70)
    print("RSM Model Verification")
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
    
    # Step 4: Use standard DOE factor ranges (not from data, since CCD extends beyond ±1)
    # These should match the ranges used in ccdplan.py and lhsplan.py
    x1_low = 30.0   # Overlap minimum
    x1_high = 60.0  # Overlap maximum
    x2_low = 0.1    # Film_thickness minimum
    x2_high = 0.35  # Film_thickness maximum
    
    print(f"\nFactor ranges (DOE design space):")
    print(f"  Overlap: {x1_low:.2f} - {x1_high:.2f} mm")
    print(f"  Adhesive Thickness: {x2_low:.4f} - {x2_high:.4f} mm")
    print(f"\nNote: Training data may extend beyond these ranges due to CCD axial points.")
    
    # Compute center and half-ranges
    x1_center = (x1_high + x1_low) / 2.0
    x2_center = (x2_high + x2_low) / 2.0
    x1_half = (x1_high - x1_low) / 2.0
    x2_half = (x2_high - x2_low) / 2.0
    
    # Step 5: Fit RSM model
    print("\n" + "=" * 70)
    print("Fitting RSM Model...")
    print("=" * 70)
    
    rsm_fit = fit_rsm_model(train_df, x1_center, x1_half, x2_center, x2_half)
    
    print("\nRSM Model Summary:")
    print(rsm_fit.summary())
    
    # Display model equation
    params = rsm_fit.params
    equation = (
        f"Max_RF1 = {params.get('Intercept', 0):.2f} "
        f"+ ({params.get('X1', 0):.2f} * X1) "
        f"+ ({params.get('X2', 0):.2f} * X2) "
        f"+ ({params.get('I(X1 ** 2)', 0):.2f} * X1²) "
        f"+ ({params.get('I(X2 ** 2)', 0):.2f} * X2²) "
        f"+ ({params.get('X1:X2', 0):.2f} * X1*X2)"
    )
    print("\n" + "=" * 70)
    print("RSM Equation (Coded Variables):")
    print(equation)
    print("=" * 70)
    
    # Step 6: Predict on test data
    print("\n" + "=" * 70)
    print("Testing RSM Model on Test Data")
    print("=" * 70)
    
    predictions = []
    actuals = []
    
    print(f"\n{'Overlap':>10} | {'Thickness':>10} | {'Actual RF1':>12} | {'Predicted RF1':>14} | {'Error':>10} | {'Error %':>10}")
    print("-" * 80)
    
    for idx, row in test_df.iterrows():
        overlap = row['Overlap_mm']
        thickness = row['Adhesive_Thickness_mm']
        actual_rf1 = row['Max_RF1']
        
        predicted_rf1 = predict_from_rsm(rsm_fit, overlap, thickness, 
                                         x1_center, x1_half, x2_center, x2_half)
        
        error = actual_rf1 - predicted_rf1
        error_pct = (abs(error) / actual_rf1) * 100
        
        predictions.append(predicted_rf1)
        actuals.append(actual_rf1)
        
        print(f"{overlap:10.2f} | {thickness:10.4f} | {actual_rf1:12.2f} | {predicted_rf1:14.2f} | {error:10.2f} | {error_pct:9.2f}%")
    
    # Step 7: Calculate error metrics
    predictions = np.array(predictions)
    actuals = np.array(actuals)
    
    rmse = calculate_rmse(actuals, predictions)
    mape = calculate_mape(actuals, predictions)
    mae = calculate_mae(actuals, predictions)
    
    print("\n" + "=" * 70)
    print("Error Metrics")
    print("=" * 70)
    print(f"RMSE (Root Mean Square Error):    {rmse:10.2f} N")
    print(f"MAE  (Mean Absolute Error):       {mae:10.2f} N")
    print(f"MAPE (Mean Absolute % Error):     {mape:10.2f} %")
    print("=" * 70)
    
    # Step 8: Create actual vs predicted scatter plot
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
    ax.set_title('RSM Model: Actual vs Predicted Values', fontsize=14, fontweight='bold')
    
    # Add error metrics to plot
    textstr = f'RMSE = {rmse:.2f} N\nMAE = {mae:.2f} N\nMAPE = {mape:.2f}%'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
    
    ax.legend(fontsize=10, loc='lower right')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    # Save plot
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    plot_path = os.path.join(output_dir, 'rsm_actual_vs_predicted.svg')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nActual vs Predicted plot saved to: {plot_path}")
    
    plt.show()
    
    # Step 9: Create residual plot
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
    ax.set_title('RSM Model: Residual Plot', fontsize=14, fontweight='bold')
    
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
    residual_plot_path = os.path.join(output_dir, 'rsm_residual_plot.svg')
    plt.savefig(residual_plot_path, dpi=300, bbox_inches='tight')
    print(f"\nResidual plot saved to: {residual_plot_path}")
    
    plt.show()
    
    print("\nInterpretation:")
    print("- Points scattered around y=0 = Good model fit")
    print("- Pattern or trend = Systematic error in model")
    print("- Increasing spread = Heteroscedasticity (non-constant variance)")

if __name__ == '__main__':
    main()


##Important metrics to look out for:
#Low Error Metrics (RMSE, MAE, MAPE)
#High R-squared and Adjusted R-squared values (goodness of fir)
#Good visuals in actual vs predicted and residual plots (actual values closely follow y=x line; residuals randomly scattered around zero)
