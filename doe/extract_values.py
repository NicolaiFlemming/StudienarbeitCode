from odbAccess import openOdb
import csv
import re
import tkinter as tk
from tkinter import filedialog
import os

# === Step 1: Ask user to select ODB files ===
root = tk.Tk()
root.withdraw()  # Hide main tkinter window
file_paths = filedialog.askopenfilenames(
    title="Select Abaqus ODB files",
    filetypes=[("Abaqus ODB files", "*.odb")]
)

if not file_paths:
    print("No files selected. Exiting.")
    exit()

# === Step 2: Ask where to save CSV ===
csv_path = filedialog.asksaveasfilename(
    title="Save results CSV as...",
    defaultextension=".csv",
    filetypes=[("CSV files", "*.csv")]
)
if not csv_path:
    print("No save location selected. Exiting.")
    exit()

# === Step 3: Define filename regex ===
# Matches: SAP30p0_100mu_DP490.odb
# Groups:
#   1 = overlap (30p0 → 30.0)
#   2 = adhesive thickness in micrometers (100 → 0.1 mm)
#   3 = adhesive name (DP490)
pattern = re.compile(r"SAP(\d+)p(\d+)_([0-9]+)mu_([A-Za-z0-9]+)\.odb", re.IGNORECASE)

# === Step 4: Process and extract data ===
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ODB_File', 'Overlap_mm', 'Adhesive_Thickness_mm', 'Adhesive', 'Max_RF1'])

    for odb_path in file_paths:
        odb_name = os.path.basename(odb_path)
        print(f"Processing {odb_name}...")

        # --- Parse info from filename ---
        match = pattern.match(odb_name)
        if match:
            overlap = float(match.group(1)) + float(match.group(2)) / 10.0  # e.g. 30p0 → 30.0
            thickness = float(match.group(3)) / 1000.0                      # e.g. 100µm → 0.1 mm
            adhesive = match.group(4)
        else:
            overlap = None
            thickness = None
            adhesive = None
            print(f"⚠️ Could not parse data from filename: {odb_name}")

        # --- Open ODB ---
        try:
            odb = openOdb(odb_path)
        except Exception as e:
            print(f"❌ Error opening {odb_name}: {e}")
            continue

        # --- Find RF1 in H-Output-2 ---
        rf1_max = None
        try:
            step = odb.steps['Step-1']

            # Loop through all history regions to find H-Output-2
            for region_name, region in step.historyRegions.items():
                if 'H-Output-2' in region_name or 'ZugMesspunkt' in region_name:
                    if 'RF1' in region.historyOutputs.keys():
                        rf1_data = region.historyOutputs['RF1'].data
                        rf1_max = max([v[1] for v in rf1_data])
                        break

            # Fallback: try global assembly
            if rf1_max is None:
                assembly_hist = step.historyRegions.get('Assembly ZUGMESSPUNKT')
                if assembly_hist and 'RF1' in assembly_hist.historyOutputs:
                    rf1_data = assembly_hist.historyOutputs['RF1'].data
                    rf1_max = max([v[1] for v in rf1_data])

        except Exception as e:
            print(f"⚠️ Error extracting RF1 from {odb_name}: {e}")
            rf1_max = None
        finally:
            odb.close()

        # --- Write to CSV ---
        writer.writerow([odb_name, overlap, thickness, adhesive, rf1_max])

print(f"\n✅ Done! Results saved to: {csv_path}")
