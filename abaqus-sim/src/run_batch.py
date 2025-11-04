"""
Wrapper script to run Abaqus simulations from regular Python.
This script reads config.ini and sim_params.csv, then calls Abaqus
for each simulation using the single-point mode.

Usage:
    python run_batch.py
"""

import csv
import os
import sys
import subprocess
import configparser
from pathlib import Path


def find_project_root():
    """Find the project root directory (abaqus-sim)."""
    current_dir = Path(__file__).parent.resolve()
    
    # Go up from src to abaqus-sim
    project_root = current_dir.parent
    
    if project_root.name == 'abaqus-sim':
        return project_root
    
    # Fallback: search upward
    while current_dir.name != 'abaqus-sim' and current_dir.parent != current_dir:
        current_dir = current_dir.parent
    
    return current_dir if current_dir.name == 'abaqus-sim' else project_root


def read_config(project_root):
    """Read configuration from config.ini file."""
    # Go up one more level to repo root where config.ini is
    config_path = project_root.parent / 'config.ini'
    
    config = configparser.ConfigParser()
    
    if not config_path.exists():
        print(f"Warning: config.ini not found at {config_path}. Using defaults.")
        return 'SAP', 28  # Default values
    
    config.read(config_path)
    
    joint_type = config.get('simulation', 'joint_type', fallback='SAP').strip()
    cpu_cores = config.getint('simulation', 'cpu_cores', fallback=28)
    
    return joint_type, cpu_cores


def run_abaqus_simulation(overlap, adhesive, film_thickness, cores, joint_type, project_root):
    """Run a single Abaqus simulation using subprocess."""
    
    # Construct the Abaqus command
    cmd = [
        'abaqus',
        'cae',
        'noGUI=src/run_simulations.py',
        '--',
        '--single',
        str(overlap),
        adhesive,
        str(film_thickness),
        str(cores),
        joint_type
    ]
    
    print(f"\nRunning: {' '.join(cmd)}")
    print(f"Working directory: {project_root}")
    
    try:
        # Run the command from the project root directory
        result = subprocess.run(
            cmd,
            cwd=str(project_root),
            capture_output=True,
            text=True,
            timeout=7200  # 2 hour timeout per simulation
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode != 0:
            print(f"ERROR: Simulation failed with return code {result.returncode}")
            if result.stderr:
                print(f"Error output: {result.stderr}")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print("ERROR: Simulation timed out after 2 hours")
        return False
    except FileNotFoundError:
        print("ERROR: 'abaqus' command not found. Make sure Abaqus is installed and in PATH")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error running simulation: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 60)
    print("Abaqus Batch Simulation Runner (Python Wrapper)")
    print("=" * 60)
    
    # Find project root
    project_root = find_project_root()
    print(f"\nProject root: {project_root}")
    
    # Read configuration
    joint_type, default_cores = read_config(project_root)
    print(f"Configuration:")
    print(f"  Joint type: {joint_type}")
    print(f"  Default CPU cores: {default_cores}")
    
    # Find and read sim_params.csv
    params_file = project_root / 'inputs' / 'sim_params.csv'
    
    if not params_file.exists():
        print(f"\nERROR: Input file not found: {params_file}")
        print("Please generate sim_params.csv using one of the DOE scripts:")
        print("  python doe/lhsplan.py")
        print("  python doe/ccdplan.py")
        return 1
    
    print(f"\nReading parameters from: {params_file}")
    
    # Read and process simulations
    successful = 0
    failed = 0
    
    try:
        with open(params_file, 'r') as f:
            reader = csv.DictReader(f)
            
            simulations = list(reader)
            total = len(simulations)
            
            print(f"\nFound {total} simulation(s) to run")
            print("=" * 60)
            
            for i, params in enumerate(simulations, 1):
                print(f"\n[{i}/{total}] Processing simulation {i}:")
                
                try:
                    # Extract parameters
                    overlap = float(params['Overlap'])
                    adhesive = params['Adhesive'].strip()
                    film_thickness = float(params['Film_thickness'])
                    cores = int(params.get('Cores', default_cores))
                    
                    print(f"  Overlap: {overlap} mm")
                    print(f"  Adhesive: {adhesive}")
                    print(f"  Film thickness: {film_thickness} mm")
                    print(f"  Cores: {cores}")
                    print(f"  Joint type: {joint_type}")
                    
                    # Run the simulation
                    success = run_abaqus_simulation(
                        overlap, adhesive, film_thickness, 
                        cores, joint_type, project_root
                    )
                    
                    if success:
                        successful += 1
                        print(f"✓ Simulation {i} completed successfully")
                    else:
                        failed += 1
                        print(f"✗ Simulation {i} failed")
                        
                except KeyError as e:
                    print(f"ERROR: Missing column in CSV: {e}")
                    failed += 1
                except ValueError as e:
                    print(f"ERROR: Invalid value in CSV: {e}")
                    failed += 1
                except Exception as e:
                    print(f"ERROR: Unexpected error: {e}")
                    failed += 1
    
    except Exception as e:
        print(f"\nERROR: Failed to read CSV file: {e}")
        return 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total simulations: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
