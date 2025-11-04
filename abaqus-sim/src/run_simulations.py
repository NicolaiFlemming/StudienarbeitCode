import csv
import os
import sys
import configparser

# ----------------------------------------------------------------------
# ROBUST PATH DETERMINATION
# ----------------------------------------------------------------------

def find_project_root():
    """Find the project root directory from the current working directory."""
    # Start with the current working directory
    current_dir = os.path.abspath(os.getcwd())
    
    # Try to find 'abaqus-strapjoint-sim' in the path
    while True:
        # Check if we're in the project root
        if os.path.basename(current_dir) == 'abaqus-strapjoint-sim':
            return current_dir
        
        # Check if we've reached the root of the filesystem
        parent = os.path.dirname(current_dir)
        if parent == current_dir:
            # If we haven't found it, return the directory containing run_simulations.py
            return os.path.abspath(os.path.join(os.getcwd(), '..'))
        
        current_dir = parent

# Find project root and set up paths
project_root = find_project_root()
script_dir = os.path.join(project_root, 'src')

if script_dir not in sys.path:
    sys.path.append(script_dir)

# ----------------------------------------------------------------------
# MODULE IMPORTS
# ----------------------------------------------------------------------

try:
    # This import should now work because the 'src' directory is explicitly in sys.path
    from StrapJoint import StrapJoint, DP490, AF163
    from SteppedJoint import SteppedJoint
except ImportError:
    # This fatal exit is a clean way to handle module import failure in Abaqus
    print("FATAL ERROR: Could not import StrapJoint or SteppedJoint. Check file names and directory structure.")
    print(f"Attempted to add directory to sys.path: {script_dir}")
    print(f"Current sys.path entries: {sys.path}")
    sys.exit()

# ----------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------

def get_adhesive_object(name):
    """Maps the adhesive name string from the CSV to the actual AdhesiveMaterial object."""
    if name == 'DP490':
        return DP490
    elif name == 'AF163':
        return AF163
    else:
        raise ValueError(f"Unknown adhesive name in CSV: {name}. Must be 'DP490' or 'AF163'.")

def get_joint_function(joint_type):
    """Maps the joint type string to the corresponding function."""
    if joint_type == 'SAP':
        return StrapJoint
    elif joint_type == 'SEP':
        return SteppedJoint
    else:
        raise ValueError(f"Unknown joint type: {joint_type}. Must be 'SAP' or 'SEP'.")

def read_config():
    """Read configuration from config.ini file."""
    # Navigate up from src to project root to find config.ini
    project_root = find_project_root()
    # Go up one more level to find config.ini in the repo root
    config_path = os.path.join(os.path.dirname(project_root), 'config.ini')
    
    config = configparser.ConfigParser()
    
    # Check if config file exists
    if not os.path.exists(config_path):
        print(f"Warning: config.ini not found at {config_path}. Using defaults.")
        return 'SAP'  # Default to Strap Joint
    
    config.read(config_path)
    
    # Read joint type from config, default to SAP
    joint_type = config.get('simulation', 'joint_type', fallback='SAP').strip()
    
    return joint_type

# ----------------------------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------------------------

def run_single_point(overlap, adhesive_name, film_thickness, cores, joint_type='SAP'):
    """Run simulation for a single point with given parameters."""
    try:
        print(f"Processing single point simulation:")
        print(f"  Joint Type: {joint_type}")
        print(f"  Overlap: {overlap} mm")
        print(f"  Adhesive: {adhesive_name}")
        print(f"  Thickness: {film_thickness} mm")
        print(f"  Cores: {cores}")
        
        # Get the corresponding material object
        print("Getting adhesive object...")
        adhesive_object = get_adhesive_object(adhesive_name)
        if adhesive_object is None:
            print(f"Error: Could not get adhesive object for {adhesive_name}")
            return False
        
        # Get the joint function
        print("Getting joint function...")
        joint_function = get_joint_function(joint_type)
        
        print(f"Starting {joint_type} simulation...")
        
        # Call the joint function with explicit error handling
        try:
            joint_function(
                overlap=overlap, 
                adhesive=adhesive_object, 
                film_thickness=film_thickness, 
                cores=cores
            )
        except ImportError as e:
            print(f"Error importing joint module: {e}")
            print(f"Current directory: {os.getcwd()}")
            print(f"Python path: {sys.path}")
            return False
        except Exception as e:
            print(f"Error in joint execution: {e}")
            return False
        
        print("Job submitted and completed successfully")
        return True
        
    except Exception as e:
        print(f"An error occurred during simulation setup: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # Get the project root using our robust function
    project_root = find_project_root()
    
    # Read joint type from config
    joint_type_from_config = read_config()
    print(f"Joint type from config: {joint_type_from_config}")
    
    # Extract the --single argument position
    try:
        single_index = sys.argv.index('--single')
    except ValueError:
        single_index = -1

    # Check if running in single point mode
    if single_index != -1:
        if len(sys.argv) < single_index + 5:
            print("Usage for single point: abaqus cae noGUI=run_simulations.py -- --single overlap adhesive film_thickness cores [joint_type]")
            print("  joint_type is optional, defaults to SAP (Strap Joint). Use SEP for Stepped Joint.")
            return
        
        try:
            # Arguments come after --single
            overlap = float(sys.argv[single_index + 1])
            adhesive_name = sys.argv[single_index + 2]
            film_thickness = float(sys.argv[single_index + 3])
            cores = int(sys.argv[single_index + 4])
            joint_type = sys.argv[single_index + 5] if len(sys.argv) > single_index + 5 else 'SAP'
            
            print(f"Running single point simulation with parameters:")
            print(f"  Joint Type: {joint_type}")
            print(f"  Overlap: {overlap}")
            print(f"  Adhesive: {adhesive_name}")
            print(f"  Film thickness: {film_thickness}")
            print(f"  Cores: {cores}")
            
            success = run_single_point(overlap, adhesive_name, film_thickness, cores, joint_type)
            sys.exit(0 if success else 1)
            
        except ValueError as e:
            print(f"Error in parameter conversion: {e}")
            sys.exit(1)
    params_file = os.path.join(project_root, 'inputs', 'sim_params.csv')
    
    if not os.path.exists(params_file):
        print(f"Error: Input file '{params_file}' not found.")
        print(f"Looked for CSV at: {params_file}")
        return

    print(f"Starting Abaqus simulations using parameters from {params_file}...")
    
    try:
        with open(params_file, mode='r') as file:
            reader = csv.DictReader(file)
            
            for i, params in enumerate(reader):
                print("-" * 40)
                print(f"Processing Scenario {i + 1}:")
                
                try:
                    # 1. Parameter extraction and type conversion
                    overlap = float(params['Overlap'])
                    adhesive_name = params['Adhesive'].strip()
                    film_thickness = float(params['Film_thickness'])
                    cores = int(params['Cores'])
                    
                    # 2. Get the corresponding material object and joint function from config
                    adhesive_object = get_adhesive_object(adhesive_name)
                    joint_function = get_joint_function(joint_type_from_config)
                    
                    print(f"  Joint Type: {joint_type_from_config}, Overlap: {overlap} mm, Adhesive: {adhesive_name}, Thickness: {film_thickness} mm, Cores: {cores}")
                    
                    # 3. Call the appropriate joint function (The modeling and job run starts here)
                    joint_function(
                        overlap=overlap, 
                        adhesive=adhesive_object, 
                        film_thickness=film_thickness, 
                        cores=cores
                    )
                    
                    print(f"  Job finished successfully for Scenario {i + 1}. CAE saved to: {project_root}")
                    
                except KeyError as e:
                    print(f"Error in CSV format: Missing column {e}. Check headers.")
                    break
                except ValueError as e:
                    print(f"Error in data conversion or adhesive lookup: {e}")
                    break
                except Exception as e:
                    print(f"An Abaqus error occurred during Scenario {i + 1}: {e}")
                    # You might want to remove 'break' here to continue to the next job, but for debugging, 'break' is safer.
                    break 

    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")

if __name__ == '__main__':
    print("Starting run_simulations.py")
    print(f"Current directory: {os.getcwd()}")
    print(f"Command line arguments: {sys.argv}")
    main()
    print("Finished run_simulations.py")