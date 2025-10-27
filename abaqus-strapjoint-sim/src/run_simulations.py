import csv
import os
import sys

# ----------------------------------------------------------------------
# ROBUST PATH DETERMINATION (Fixes NameError: name '__file__' is not defined)
# ----------------------------------------------------------------------

# 1. Define the name of your project directory for reliable anchoring.
# Replace 'abaqus-strapjoint-sim' with your actual root folder name if different!
PROJECT_ROOT_NAME = 'abaqus-strapjoint-sim' 

# 2. Search sys.path to find the absolute path to your Project Root
project_root = None
for p in sys.path:
    # Check if the path contains the project root name
    if PROJECT_ROOT_NAME in os.path.basename(os.path.normpath(p)):
        project_root = os.path.abspath(p)
        break

# 3. Fallback logic (Less reliable, but ensures project_root is set)
if project_root is None:
    # If the specific name wasn't found, try the directory containing the executed script (sys.path[0])
    try:
        script_dir = os.path.abspath(sys.path[0])
        project_root = os.path.abspath(os.path.join(script_dir, '..'))
    except IndexError:
        project_root = os.path.abspath(os.getcwd())


# 4. Define the source directory path and add it to sys.path
script_dir = os.path.join(project_root, 'src')

if script_dir not in sys.path:
    sys.path.append(script_dir)

# ----------------------------------------------------------------------
# MODULE IMPORTS
# ----------------------------------------------------------------------

try:
    # This import should now work because the 'src' directory is explicitly in sys.path
    from StrapJoint import StrapJoint, DP490, AF163
except ImportError:
    # This fatal exit is a clean way to handle module import failure in Abaqus
    print("FATAL ERROR: Could not import StrapJoint. Check file names and directory structure.")
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

# ----------------------------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------------------------

def run_single_point(overlap, adhesive_name, film_thickness, cores):
    """Run simulation for a single point with given parameters."""
    try:
        print(f"Processing single point simulation:")
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
            
        print("Starting StrapJoint simulation...")
        
        # Call the StrapJoint function with explicit error handling
        try:
            from StrapJoint import StrapJoint
            StrapJoint(
                overlap=overlap, 
                adhesive=adhesive_object, 
                film_thickness=film_thickness, 
                cores=cores
            )
        except ImportError as e:
            print(f"Error importing StrapJoint module: {e}")
            print(f"Current directory: {os.getcwd()}")
            print(f"Python path: {sys.path}")
            return False
        except Exception as e:
            print(f"Error in StrapJoint execution: {e}")
            return False
        
        print("Job submitted and completed successfully")
        return True
        
    except Exception as e:
        print(f"An error occurred during simulation setup: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # Check if running in single point mode (via command line arguments)
    if len(sys.argv) > 1 and sys.argv[1] == '--single':
        if len(sys.argv) != 6:
            print("Usage for single point: python run_simulations.py --single overlap adhesive film_thickness cores")
            return
        
        try:
            overlap = float(sys.argv[2])
            adhesive_name = sys.argv[3]
            film_thickness = float(sys.argv[4])
            cores = int(sys.argv[5])
            success = run_single_point(overlap, adhesive_name, film_thickness, cores)
            
            if len(sys.argv) > 1:  # If running from command line arguments
                sys.exit(0 if success else 1)  # Exit with status code
            return success  # Otherwise just return the boolean
            
        except ValueError as e:
            print(f"Error in parameter conversion: {e}")
            if len(sys.argv) > 1:  # If running from command line arguments
                sys.exit(1)
            return False
    
    # Regular CSV mode
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
                    
                    # 2. Get the corresponding material object
                    adhesive_object = get_adhesive_object(adhesive_name)
                    
                    print(f"  Overlap: {overlap} mm, Adhesive: {adhesive_name}, Thickness: {film_thickness} mm, Cores: {cores}")
                    
                    # 3. Call the StrapJoint function (The modeling and job run starts here)
                    StrapJoint(
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