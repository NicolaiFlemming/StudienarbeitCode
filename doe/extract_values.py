from odbAccess import openOdb
import csv
import re
import tkinter as tk
from tkinter import filedialog
import os

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

        # --- Open odb ---
        try:
            odb = openOdb(odb_path)
        except Exception as e:
            print(f" Error opening {odb_name}: {e}")
            continue

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

        except Exception as e:
            print(f" Error extracting RF1 from {odb_name}: {e}")
        finally:
            odb.close()

        writer.writerow([odb_name, overlap, thickness, adhesive, rf1_max, region_found])

print(f"\n Done! Results saved to: {csv_path}")
