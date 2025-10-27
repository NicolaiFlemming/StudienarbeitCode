import numpy as np
import pandas as pd
import os
import sys
import tkinter as tk
from tkinter import filedialog
from krg_training import train_and_predict_kriging
from odbAccess import openOdb

def select_results_file():
    """Open a file dialog to select the results CSV file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.lift()      # Bring dialog to front
    root.focus_force()  # Force focus on the dialog
    
    file_path = filedialog.askopenfilename(
        title="Select Results CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if not file_path:
        print("No file selected. Exiting.")
        sys.exit(1)
    
    return file_path

def format_thickness_for_filename(thickness_mm):
    """Convert thickness in mm to microns for filename."""
    return int(thickness_mm * 1000)

def format_overlap_for_filename(overlap_mm):
    """Convert overlap value to filename format (e.g., 45.5 -> 45p50)."""
    whole = int(overlap_mm)
    decimal = int((overlap_mm - whole) * 100)
    return f"{whole}p{decimal:02d}"

def extract_rf1_from_odb(overlap_mm, thickness_mm, adhesive='DP490'):
    """Extract RF1 value from a single ODB file."""
    # Format the filename components
    overlap_str = format_overlap_for_filename(overlap_mm)
    thickness_microns = format_thickness_for_filename(thickness_mm)
    
    # Construct the expected ODB filename
    odb_name = f"SAP{overlap_str}_{thickness_microns}mu_{adhesive}.odb"
    odb_path = os.path.abspath(f"../abaqus-strapjoint-sim/src/{odb_name}")
    
    if not os.path.exists(odb_path):
        print(f"Error: ODB file not found: {odb_path}")
        return None
    
    try:
        odb = openOdb(odb_path)
        rf1_max = None
        
        try:
            step = odb.steps['Step-1']
            
            # Search all regions for RF1
            for region_name, region in step.historyRegions.items():
                if 'RF1' in region.historyOutputs.keys():
                    rf1_data = region.historyOutputs['RF1'].data
                    rf1_local_max = max(v[1] for v in rf1_data)
                    if rf1_max is None or rf1_local_max > rf1_max:
                        rf1_max = rf1_local_max
            
            return rf1_max
            
        finally:
            odb.close()
            
    except Exception as e:
        print(f"Error processing ODB file: {e}")
        return None

def update_results_csv(overlap, thickness, rf1_value, results_file='results.csv'):
    """Update the results CSV file with a new data point."""
    new_result = pd.DataFrame({
        'Overlap_mm': [overlap],
        'Adhesive_Thickness_mm': [thickness],
        'Max_RF1': [rf1_value]
    })
    
    if os.path.exists(results_file):
        # Append without header
        new_result.to_csv(results_file, mode='a', header=False, index=False)
    else:
        # Create new file with header
        new_result.to_csv(results_file, index=False)

def add_point_to_sim_params(overlap, adhesive_thickness, adhesive='DP490', cores=28):
    """Add a new point to the simulation parameters CSV file."""
    new_point = pd.DataFrame({
        'Overlap': [overlap],
        'Adhesive': [adhesive],
        'Film_thickness': [adhesive_thickness],
        'Cores': [cores]
    })
    
    sim_params_path = '../abaqus-strapjoint-sim/inputs/sim_params.csv'
    if os.path.exists(sim_params_path):
        new_point.to_csv(sim_params_path, mode='a', header=False, index=False)
    else:
        new_point.to_csv(sim_params_path, index=False)

def run_optimization_loop(n_iterations=5, results_file='results.csv'):
    """Run the iterative optimization loop."""
    for iteration in range(n_iterations):
        print(f"\nStarting iteration {iteration + 1}/{n_iterations}")
        
        # 1. Train Kriging model and get point of highest uncertainty
        max_uncertainty_point = train_and_predict_kriging(results_file)
        
        if max_uncertainty_point is None:
            print("Error in Kriging model training. Stopping optimization loop.")
            break
            
        overlap, adhesive_thickness, std_dev = max_uncertainty_point
        
        print(f"Point of highest uncertainty found:")
        print(f"Overlap: {overlap:.2f} mm")
        print(f"Adhesive Thickness: {adhesive_thickness:.2f} mm")
        print(f"Standard Deviation: {std_dev:.2f}")
        
        # 2. Run the simulation for just this point
        print("\nRunning Abaqus simulation for optimized point...")
        os.chdir('../abaqus-strapjoint-sim/src')
        cmd = f'abaqus cae noGUI=run_simulations.py -- --single {overlap} DP490 {adhesive_thickness} 28'
        os.system(cmd)
        
        # 3. Extract RF1 from the ODB file
        print("\nExtracting results from ODB file...")
        rf1_value = extract_rf1_from_odb(overlap, adhesive_thickness)
        
        if rf1_value is not None:
            # 4. Update results.csv with the new point
            os.chdir('../../doe')  # Return to original directory
            update_results_csv(overlap, adhesive_thickness, rf1_value, results_file)
            print(f"Results updated: RF1 = {rf1_value:.2f}")
            
            # 5. Add point to sim_params.csv for record keeping
            add_point_to_sim_params(overlap, adhesive_thickness)
        else:
            print("Failed to extract results from ODB file. Skipping this iteration.")
            os.chdir('../../doe')  # Return to original directory
            continue
        
        print(f"Iteration {iteration + 1} complete.\n")
        print("-" * 50)

if __name__ == '__main__':
    # Number of optimization iterations
    N_ITERATIONS = 5
    
    print("Starting Kriging model optimization loop")
    print(f"Number of iterations: {N_ITERATIONS}")
    print("-" * 50)
    
    # Select the results file using file dialog
    print("Please select the results CSV file...")
    RESULTS_FILE = select_results_file()
    print(f"Selected results file: {RESULTS_FILE}")
    print("-" * 50)
    
    run_optimization_loop(N_ITERATIONS, RESULTS_FILE)