import csv
import re
import tkinter as tk
from tkinter import filedialog
import os
import subprocess

# === Step 1: Select ODB files ===
root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(
    title="Select Abaqus ODB files",
    filetypes=[("Abaqus ODB files", "*.odb")]
)

if not file_paths:
    print("No files selected. Exiting.")
    exit()

# === Step 2: Choose output CSV ===
csv_path = filedialog.asksaveasfilename(
    title="Save results CSV as...",
    defaultextension=".csv",
    filetypes=[("CSV files", "*.csv")]
)
if not csv_path:
    print("No save location selected. Exiting.")
    exit()

# === Step 3: Filename pattern ===
# Example: SAP66p21_220mu_DP490.odb
pattern = re.compile(r"SAP(\d+p\d+)_([0-9]+)mu_([A-Za-z0-9]+)\.odb", re.IGNORECASE)

# Get path to extract_rf1_single.py script
script_dir = os.path.dirname(os.path.abspath(__file__))
extract_script = os.path.join(script_dir, 'extract_rf1_single.py')

if not os.path.exists(extract_script):
    print(f"Error: extract_rf1_single.py not found at {extract_script}")
    exit()

# === Step 4: Process each ODB ===
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ODB_File', 'Overlap_mm', 'Adhesive_Thickness_mm', 'Adhesive', 'Max_RF1', 'Region'])

    for odb_path in file_paths:
        odb_name = os.path.basename(odb_path)
        print(f"Processing {odb_name}...")

        # --- Parse file name ---
        match = pattern.match(odb_name)
        if match:
            overlap_str = match.group(1).replace('p', '.')   # e.g. "66p21" → "66.21"
            overlap = float(overlap_str)
            thickness = float(match.group(2)) / 1000.0       # e.g. 220µm → 0.22 mm
            adhesive = match.group(3)
        else:
            overlap, thickness, adhesive = None, None, None
            print(f" Could not parse info from {odb_name}")

        # --- Extract RF1 using extract_rf1_single.py ---
        rf1_max = None
        region_found = None
        
        try:
            # Call extract_rf1_single.py with abaqus python
            cmd = f'abaqus python "{extract_script}" "{odb_path}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f" Error running extraction: {result.stderr}")
            else:
                # Read the result file
                result_file = 'rf1_result.txt'
                if os.path.exists(result_file):
                    with open(result_file, 'r') as f:
                        lines = f.readlines()
                        if len(lines) >= 2 and lines[0].strip():
                            try:
                                rf1_max = float(lines[0].strip())
                                region_found = lines[1].strip()
                                print(f" Found RF1: {rf1_max:.2f} in region {region_found}")
                            except ValueError:
                                print(f" Could not parse RF1 value from result file")
                        else:
                            print(f" No RF1 found in {odb_name}")
                    
                    # Clean up result file
                    try:
                        os.remove(result_file)
                    except Exception:
                        pass
                else:
                    print(f" Result file not created")
                    
        except subprocess.TimeoutExpired:
            print(f" Timeout processing {odb_name}")
        except Exception as e:
            print(f" Error processing {odb_name}: {e}")

        writer.writerow([odb_name, overlap, thickness, adhesive, rf1_max, region_found])

print(f"\nDone! Results saved to: {csv_path}")

