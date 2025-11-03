import numpy as np
import pandas as pd
import os
import sys
import time
import subprocess
import tkinter as tk
from tkinter import filedialog
import configparser
import matplotlib.pyplot as plt
from krg_training import train_and_predict_kriging

# Read configuration
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.ini')

if not os.path.exists(config_path):
    print(f"Error: Configuration file not found at {config_path}")
    sys.exit(1)

config.read(config_path)

# Configuration parameters
ADHESIVE_TYPE = config.get('simulation', 'adhesive_type')
CPU_CORES = config.getint('simulation', 'cpu_cores')
N_ITERATIONS = config.getint('optimization', 'n_iterations')

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
    """Convert overlap value to filename format with 4 decimal places."""
    # Round to 4 decimal places and keep all 4 decimals in filename
    rounded = round(float(overlap_mm), 4)
    return f"{rounded:.4f}".replace(".", "p")

def get_rf1_from_odb(overlap_mm, thickness_mm):
    """Extract RF1 value and region from an ODB file using abaqus python."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abaqus_dir = os.path.abspath(os.path.join(script_dir, '..', 'abaqus-sim', 'src'))
    
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
        # Save current directory to return to it later
        original_dir = os.getcwd()
        try:
            # Change to the abaqus directory
            os.chdir(abaqus_dir)
            
            # Run the extraction script in Abaqus Python
            extract_script = os.path.join(script_dir, 'extract_rf1_single.py')
            cmd = f'abaqus python "{extract_script}" "{odb_path}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print("Error running extraction script:")
                print(result.stderr)
                return None, None
            
            # Read results from the text file
            result_file = 'rf1_result.txt'
            if os.path.exists(result_file):
                with open(result_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        rf1_value = float(lines[0].strip())
                        region_name = lines[1].strip()
                        return rf1_value, region_name
            
            return None, None
            
        finally:
            os.chdir(original_dir)
            # Clean up result file
            if os.path.exists(os.path.join(abaqus_dir, 'rf1_result.txt')):
                try:
                    os.remove(os.path.join(abaqus_dir, 'rf1_result.txt'))
                except Exception:
                    pass
            
    except Exception as e:
        print(f"Error in get_rf1_from_odb: {e}")
        return None, None

def update_results_csv(overlap, thickness, rf1_value, region_name, results_file='results.csv'):
    """Update the results CSV file with a new data point."""
    # Create filename as it appears in the ODB
    overlap_str = format_overlap_for_filename(overlap)
    thickness_microns = format_thickness_for_filename(thickness)
    odb_filename = f"SAP{overlap_str}_{thickness_microns}mu_{ADHESIVE_TYPE}.odb"
    
    new_result = pd.DataFrame({
        'ODB_File': [odb_filename],
        'Overlap_mm': [round(float(overlap), 4)],
        'Adhesive_Thickness_mm': [round(float(thickness), 4)],
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
        'Overlap': [round(float(overlap), 4)],
        'Adhesive': [ADHESIVE_TYPE],
        'Film_thickness': [round(float(adhesive_thickness), 4)],
        'Cores': [CPU_CORES]
    })
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sim_params_path = os.path.abspath(os.path.join(
        script_dir, '..', 'abaqus-sim', 'inputs', 'sim_params.csv'
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
    
    # Track optimization history
    iteration_history = []
    
    for iteration in range(n_iterations):
        print(f"\nStarting iteration {iteration + 1}/{n_iterations}")
        
        # 1. Train Kriging model and get point of highest uncertainty
        result = train_and_predict_kriging(results_file, show_plots=False)
        
        if result is None:
            print("Error in Kriging model training. Stopping optimization loop.")
            break
            
        overlap, adhesive_thickness, std_dev, hyperparameters = result
        
        # Store iteration data including hyperparameters
        iteration_data = {
            'iteration': iteration + 1,
            'overlap': overlap,
            'adhesive_thickness': adhesive_thickness,
            'std_dev': std_dev,
            'kernel_constant': hyperparameters['constant_value'],
            'length_scale_overlap': hyperparameters['length_scale_overlap'],
            'length_scale_thickness': hyperparameters['length_scale_thickness'],
            'nu': hyperparameters['nu'],
            'alpha': hyperparameters['alpha'],
            'log_marginal_likelihood': hyperparameters['log_marginal_likelihood']
        }
        
        print(f"Point of highest uncertainty found:")
        print(f"Overlap: {overlap:.4f} mm")
        print(f"Adhesive Thickness: {adhesive_thickness:.3f} mm")
        print(f"Standard Deviation: {std_dev:.2f}")
        print(f"\nOptimized Hyperparameters:")
        print(f"  Kernel Constant: {hyperparameters['constant_value']:.4f}")
        print(f"  Length Scale (Overlap): {hyperparameters['length_scale_overlap']:.4f}")
        print(f"  Length Scale (Thickness): {hyperparameters['length_scale_thickness']:.4f}")
        print(f"  Log Marginal Likelihood: {hyperparameters['log_marginal_likelihood']:.2f}")
        
        # Get the absolute paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sim_dir = os.path.abspath(os.path.join(script_dir, '..', 'abaqus-sim', 'src'))
        
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
                return iteration_history
                
            # Give a small buffer for file system operations
            time.sleep(2)
            
            # Check if ODB file exists
            odb_name = f"{job_name}.odb"
            if not os.path.exists(odb_name):
                print(f"Error: Expected ODB file {odb_name} not found after simulation")
                return iteration_history
                
            print("Simulation completed successfully.")
            
            # 3. Extract RF1 from the ODB file
            print("\nExtracting results from ODB file...")
            rf1_value, region_name = get_rf1_from_odb(overlap, adhesive_thickness)
            
            if rf1_value is not None and region_name is not None:
                # 4. Update results.csv with the new point
                os.chdir(original_dir)  # Return to original directory
                update_results_csv(overlap, adhesive_thickness, rf1_value, region_name, results_file)
                print(f"Results updated: RF1 = {rf1_value:.2f}")
                
                # Store RF1 in iteration data
                iteration_data['rf1_value'] = rf1_value
                
                # 5. Add point to sim_params.csv for record keeping
                add_point_to_sim_params(overlap, adhesive_thickness)
            else:
                print("Failed to extract results from ODB file. Skipping this iteration.")
                iteration_data['rf1_value'] = None
                
        finally:
            # Always return to original directory
            os.chdir(original_dir)
        
        # Add to history
        iteration_history.append(iteration_data)
        
        print(f"Iteration {iteration + 1} complete.\n")
        print("-" * 50)
    
    return iteration_history

def plot_optimization_history(iteration_history):
    """Plot the optimization history showing uncertainty reduction."""
    if not iteration_history:
        print("No optimization history to plot.")
        return
    
    # Convert to DataFrame for easier plotting
    df = pd.DataFrame(iteration_history)
    
    # Get script directory and create output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save iteration history to CSV in output directory
    csv_filename = os.path.join(output_dir, 'krg_optimization_history.csv')
    df.to_csv(csv_filename, index=False)
    print(f"\nOptimization history data saved to: {csv_filename}")
    
    # Create single plot for standard deviation
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(df['iteration'], df['std_dev'], 'o-', linewidth=2.5, markersize=10, 
            color='#e74c3c', markeredgecolor='black', markeredgewidth=1.5)
    ax.set_xlabel('Iteration', fontsize=13, fontweight='bold')
    ax.set_ylabel('Standard Deviation (Uncertainty)', fontsize=13, fontweight='bold')
    ax.set_title('Kriging Optimization: Maximum Uncertainty per Iteration', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xticks(df['iteration'])
    
    # Add value labels on points
    for idx, row in df.iterrows():
        ax.annotate(f'{row["std_dev"]:.1f}', 
                   (row['iteration'], row['std_dev']),
                   textcoords="offset points", 
                   xytext=(0, 10), 
                   ha='center',
                   fontsize=9,
                   fontweight='bold')
    
    plt.tight_layout()
    
    # Save plot in output directory
    plot_filename = os.path.join(output_dir, 'krg_optimization_history.png')
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    print(f"Optimization history plot saved to: {plot_filename}")
    
    # Show plot
    plt.show()
    
    # Print summary statistics
    print("\n" + "=" * 50)
    print("OPTIMIZATION SUMMARY")
    print("=" * 50)
    print(f"Total iterations completed: {len(df)}")
    print(f"Initial max uncertainty: {df['std_dev'].iloc[0]:.2f}")
    print(f"Final max uncertainty: {df['std_dev'].iloc[-1]:.2f}")
    print(f"Uncertainty reduction: {((df['std_dev'].iloc[0] - df['std_dev'].iloc[-1]) / df['std_dev'].iloc[0] * 100):.1f}%")
    print("=" * 50)

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
    
    # Run optimization
    history = run_optimization_loop(N_ITERATIONS, RESULTS_FILE)
    
    # Save results immediately after optimization
    if history:
        # Create output directory if it doesn't exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Save to CSV in the output directory
        df_history = pd.DataFrame(history)
        csv_filename = os.path.join(output_dir, 'krg_optimization_history.csv')
        df_history.to_csv(csv_filename, index=False)
        print(f"\n{'='*50}")
        print(f"Optimization history saved to: {csv_filename}")
        print(f"{'='*50}")
        
        # Plot results
        plot_optimization_history(history)
    else:
        print("\nNo optimization history to save.")