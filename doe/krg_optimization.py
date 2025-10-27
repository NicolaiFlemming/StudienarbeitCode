import numpy as np
import pandas as pd
import os
import sys
import time
import subprocess
import tkinter as tk
from tkinter import filedialog
from krg_training import train_and_predict_kriging

# Configuration parameters
ADHESIVE_TYPE = 'DP490'  # Options: 'DP490' or 'AF163'
CPU_CORES = 28
N_ITERATIONS = 5  # Number of optimization iterations

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
    """Convert overlap value to filename format (e.g., 30.0 -> 30p0)."""
    return str(overlap_mm).replace(".", "p")

def get_rf1_from_odb(overlap_mm, thickness_mm):
    """Extract RF1 value and region from an ODB file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abaqus_dir = os.path.abspath(os.path.join(script_dir, '..', 'abaqus-strapjoint-sim', 'src'))
    
    # Format the filename components
    overlap_str = format_overlap_for_filename(overlap_mm)
    thickness_microns = format_thickness_for_filename(thickness_mm)
    
    # Construct the expected ODB filename
    odb_name = f"SAP{overlap_str}_{thickness_microns}mu_{ADHESIVE_TYPE}.odb"
    odb_path = os.path.join(abaqus_dir, odb_name)
    
    if not os.path.exists(odb_path):
        print(f"Error: ODB file not found: {odb_path}")
        return None, None
    
    try:
        from odbAccess import openOdb
        odb = openOdb(odb_path)
        
        rf1_max = None
        region_found = None
        
        try:
            step = odb.steps['Step-1']
            
            # Search all regions for RF1
            for region_name, region in step.historyRegions.items():
                if 'RF1' in region.historyOutputs.keys():
                    rf1_data = region.historyOutputs['RF1'].data
                    rf1_local_max = max(v[1] for v in rf1_data)
                    if rf1_max is None or rf1_local_max > rf1_max:
                        rf1_max = rf1_local_max
                        region_found = region_name
            
            if rf1_max is None:
                print(f" No RF1 found in {odb_name}. Regions:")
                for rn in step.historyRegions.keys():
                    print("   ", rn)
                print("----")
                
        finally:
            odb.close()
            
        return rf1_max, region_found
        
    except Exception as e:
        print(f"Error processing ODB file: {e}")
        return None, None

def update_results_csv(overlap, thickness, rf1_value, region_name, results_file='results.csv'):
    """Update the results CSV file with a new data point."""
    # Create filename as it appears in the ODB
    overlap_str = format_overlap_for_filename(overlap)
    thickness_microns = format_thickness_for_filename(thickness)
    odb_filename = f"SAP{overlap_str}_{thickness_microns}mu_{ADHESIVE_TYPE}.odb"
    
    new_result = pd.DataFrame({
        'ODB_File': [odb_filename],
        'Overlap_mm': [overlap],
        'Adhesive_Thickness_mm': [thickness],
        'Adhesive': [ADHESIVE_TYPE],
        'Max_RF1': [rf1_value],
        'Region': [region_name]
    })
    
    if os.path.exists(results_file):
        if os.path.getsize(results_file) > 0:  # Only try to read if file is not empty
            # Append without header
            new_result.to_csv(results_file, mode='a', header=False, index=False)
        else:
            # Write with header if file is empty
            new_result.to_csv(results_file, index=False)
    else:
        # Create new file with header
        new_result.to_csv(results_file, index=False)

def add_point_to_sim_params(overlap, adhesive_thickness):
    """Add a new point to the simulation parameters CSV file."""
    new_point = pd.DataFrame({
        'Overlap': [overlap],
        'Adhesive': [ADHESIVE_TYPE],
        'Film_thickness': [adhesive_thickness],
        'Cores': [CPU_CORES]
    })
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sim_params_path = os.path.abspath(os.path.join(
        script_dir, '..', 'abaqus-strapjoint-sim', 'inputs', 'sim_params.csv'
    ))
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(sim_params_path), exist_ok=True)
    
    if os.path.exists(sim_params_path):
        new_point.to_csv(sim_params_path, mode='a', header=False, index=False)
    else:
        new_point.to_csv(sim_params_path, index=False)

def run_optimization_loop(n_iterations=5, results_file='results.csv'):
    """Run the iterative optimization loop."""
    print("\nRunning optimization loop with:")
    print(f"Results file: {results_file}")
    print(f"Number of iterations: {n_iterations}")
    print("-" * 50)
    
    for iteration in range(n_iterations):
        print(f"\nStarting iteration {iteration + 1}/{n_iterations}")
        
        # 1. Train Kriging model and get point of highest uncertainty
        max_uncertainty_point = train_and_predict_kriging(results_file, show_plots=False)
        
        if max_uncertainty_point is None:
            print("Error in Kriging model training. Stopping optimization loop.")
            break
            
        overlap, adhesive_thickness, std_dev = max_uncertainty_point
        
        print(f"Point of highest uncertainty found:")
        print(f"Overlap: {overlap:.2f} mm")
        print(f"Adhesive Thickness: {adhesive_thickness:.2f} mm")
        print(f"Standard Deviation: {std_dev:.2f}")
        
        # Get the absolute paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sim_dir = os.path.abspath(os.path.join(script_dir, '..', 'abaqus-strapjoint-sim', 'src'))
        
        # 2. Run the simulation for just this point
        print("\nRunning Abaqus simulation for optimized point...")
        print(f"Simulation directory: {sim_dir}")
        
        # Save current directory
        original_dir = os.getcwd()
        
        try:
            os.chdir(sim_dir)
            print("\nRunning Abaqus simulation...")
            
            # First, construct the job name as it will appear in Abaqus
            overlap_str = format_overlap_for_filename(overlap)
            thickness_microns = format_thickness_for_filename(adhesive_thickness)
            job_name = f"SAP{overlap_str}_{thickness_microns}mu_{ADHESIVE_TYPE}"
            
            # Launch Abaqus simulation and capture output
            cmd = f'abaqus cae noGUI=run_simulations.py -- --single {overlap} {ADHESIVE_TYPE} {adhesive_thickness} {CPU_CORES}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            # Print Abaqus output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
            
            print(f"Exit code: {result.returncode}")
            
            if result.returncode != 0:
                print("Error: Abaqus simulation failed")
                return
                
            # Give a small buffer for file system operations
            time.sleep(2)
            
            # Check if ODB file exists
            odb_name = f"{job_name}.odb"
            if not os.path.exists(odb_name):
                print(f"Error: Expected ODB file {odb_name} not found after simulation")
                return
                
            print("Simulation completed successfully.")
            
            # 3. Extract RF1 from the ODB file
            print("\nExtracting results from ODB file...")
            rf1_value, region_name = get_rf1_from_odb(overlap, adhesive_thickness)
            
            if rf1_value is not None and region_name is not None:
                # 4. Update results.csv with the new point
                os.chdir(original_dir)  # Return to original directory
                update_results_csv(overlap, adhesive_thickness, rf1_value, region_name, results_file)
                print(f"Results updated: RF1 = {rf1_value:.2f}")
                
                # 5. Add point to sim_params.csv for record keeping
                add_point_to_sim_params(overlap, adhesive_thickness)
            else:
                print("Failed to extract results from ODB file. Skipping this iteration.")
                
        finally:
            # Always return to original directory
            os.chdir(original_dir)
        
        print(f"Iteration {iteration + 1} complete.\n")
        print("-" * 50)

if __name__ == '__main__':
    print("Starting Kriging model optimization loop")
    print(f"Configuration:")
    print(f"- Adhesive Type: {ADHESIVE_TYPE}")
    print(f"- CPU Cores: {CPU_CORES}")
    print(f"- Number of iterations: {N_ITERATIONS}")
    print("-" * 50)
    
    # Select the results file using file dialog
    print("Please select the results CSV file...")
    RESULTS_FILE = select_results_file()
    print(f"Selected results file: {RESULTS_FILE}")
    print("-" * 50)
    
    run_optimization_loop(N_ITERATIONS, RESULTS_FILE)