import numpy as np
# --- Function definitions ---

def to_coded(x, x_center, x_half_range):
    """Convert real value to coded variable."""
    return (x - x_center) / x_half_range


def calculate_max_rf1(X1, X2):
    """RSM equation for predicted Max_RF1 (coded variables)."""
    Max_RF1 = (
        15340.24
        + (3298.00 * X1)
        + (519.46 * X2)
        - (986.47 * X1**2)
        - (642.55 * X2**2)
        + (411.23 * X1 * X2)
    )
    return Max_RF1

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

# --- Real factor ranges (from DOE) ---
# Overlap (X1)
x1_low, x1_high = 30.0, 60.0
# Adhesive Thickness (X2)
x2_low, x2_high = 0.10, 0.35

# --- Compute center and half-ranges ---
x1_center = (x1_high + x1_low) / 2.0
x2_center = (x2_high + x2_low) / 2.0
x1_half = (x1_high - x1_low) / 2.0
x2_half = (x2_high - x2_low) / 2.0

# --- Test points (real values) ---
test_values = [
    (37.5, 0.16),
    (37.5, 0.285),
    (52.5, 0.285),
    (52.5, 0.16)
]

# --- Perform calculations ---
print("DOE RSM Verification Results")
print("--------------------------------------------------------------")
print(f"{'Overlap (mm)':>12} | {'Adh.Thk (mm)':>12} | {'X1_coded':>9} | {'X2_coded':>9} | {'Predicted Max_RF1 (N)':>22}")
print("--------------------------------------------------------------")

expected = np.array([])

for x1_real, x2_real in test_values:
    X1 = to_coded(x1_real, x1_center, x1_half)
    X2 = to_coded(x2_real, x2_center, x2_half)
    max_rf1 = calculate_max_rf1(X1, X2)
    print(f"{x1_real:12.2f} | {x2_real:12.3f} | {X1:9.2f} | {X2:9.2f} | {max_rf1:22.2f}")
    expected = np.append(expected, max_rf1)

actual = np.array([13432.20, 13245.73, 16179.85, 16812.63])

rmse = calculate_rmse(actual, expected)
mape = calculate_mape(actual, expected)
mae = calculate_mae(actual, expected)
print("DOE RSM Verification Error Metrics")
print("--------------------------------------------------------------")
print(f"RMSE: {rmse:.2f} N")
print(f"MAPE: {mape:.2f} %")
print(f"MAE: {mae:.2f} N")
