import os
import sys

# ----------------------------------------------------------------------
# ROBUST PATH DETERMINATION
# ----------------------------------------------------------------------

def find_project_root():
    """Find the project root directory from the current working directory."""
    # Start with the current working directory
    current_dir = os.path.abspath(os.getcwd())
    
    # Try to find 'abaqus-sim' in the path
    while True:
        # Check if we're in the project root
        if os.path.basename(current_dir) == 'abaqus-sim':
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
    """Main entry point - expects 5 positional arguments."""
    # Abaqus may or may not preserve the -- separator, so we need to handle both cases
    
    # Check if we have the -- separator
    if '--' in sys.argv:
        # Find the -- separator and get args after it
        separator_index = sys.argv.index('--')
        args = sys.argv[separator_index + 1:]
    else:
        # No -- separator, try to find args at the end of sys.argv
        # Look for numeric values that could be our parameters
        # Skip Abaqus-specific arguments that start with '-'
        potential_args = []
        for i in range(len(sys.argv) - 1, -1, -1):
            arg = sys.argv[i]
            # Stop if we hit a flag or the script name
            if arg.startswith('-') or arg.endswith('.py'):
                break
            potential_args.insert(0, arg)
        
        # We expect exactly 5 arguments
        if len(potential_args) >= 5:
            args = potential_args[-5:]  # Take the last 5
        else:
            args = []
    
    # Check we have all required arguments
    if len(args) < 5:
        print("ERROR: Missing arguments.")
        print("Usage: abaqus cae noGUI=run_simulations.py -- overlap adhesive film_thickness cores joint_type")
        print("  overlap: Overlap length in mm (e.g., 30.0)")
        print("  adhesive: Adhesive type (DP490 or AF163)")
        print("  film_thickness: Film thickness in mm (e.g., 0.1)")
        print("  cores: Number of CPU cores (e.g., 28)")
        print("  joint_type: Joint type (SAP or SEP)")
        print(f"\nReceived sys.argv: {sys.argv}")
        sys.exit(1)
    
    try:
        # Parse arguments
        overlap = float(args[0])
        adhesive_name = args[1]
        film_thickness = float(args[2])
        cores = int(args[3])
        joint_type = args[4]
        
        print(f"Running simulation with parameters:")
        print(f"  Joint Type: {joint_type}")
        print(f"  Overlap: {overlap}")
        print(f"  Adhesive: {adhesive_name}")
        print(f"  Film thickness: {film_thickness}")
        print(f"  Cores: {cores}")
        
        success = run_single_point(overlap, adhesive_name, film_thickness, cores, joint_type)
        sys.exit(0 if success else 1)
        
    except ValueError as e:
        print(f"Error in parameter conversion: {e}")
        print(f"Args received: {args}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    print("Starting run_simulations.py")
    print(f"Current directory: {os.getcwd()}")
    print(f"Command line arguments: {sys.argv}")
    main()
    print("Finished run_simulations.py")