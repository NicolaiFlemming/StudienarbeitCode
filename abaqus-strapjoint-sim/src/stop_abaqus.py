import subprocess
import sys
import os

def stop_abaqus_simulations():
    """Stop all running Abaqus simulations."""
    print("Attempting to stop all running Abaqus simulations...")
    
    try:
        # On Windows, taskkill will terminate all Abaqus processes
        # /F forces termination
        # /IM specifies the image name to search for
        # /T terminates the specified processes and any child processes
        abaqus_processes = [
            "ABQcaeK.exe",    # CAE kernel process
            "ABQAMSolver.exe", # Analysis process
            "ABQSMAMicro.exe", # Microsolver process
            "ABQSMAFront.exe", # Frontend process
            "standard.exe"     # Standard solver
        ]
        
        processes_found = False
        for process in abaqus_processes:
            try:
                result = subprocess.run(
                    f'taskkill /F /IM "{process}" /T',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if "SUCCESS" in result.stdout:
                    processes_found = True
                    print(f"Successfully terminated {process}")
            except subprocess.CalledProcessError:
                continue
        
        if processes_found:
            print("\nAll Abaqus processes have been terminated.")
        else:
            print("\nNo running Abaqus processes were found.")
            
    except Exception as e:
        print(f"An error occurred while trying to stop Abaqus processes: {e}")
        return False
    
    return True

if __name__ == '__main__':
    stop_abaqus_simulations()