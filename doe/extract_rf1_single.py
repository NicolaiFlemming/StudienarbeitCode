from odbAccess import openOdb
import sys
import os

def extract_rf1_from_odb(odb_path):
    """Extract RF1 value and region from a single ODB file."""
    try:
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
                print(f" No RF1 found in {odb_path}. Regions:")
                for rn in step.historyRegions.keys():
                    print("   ", rn)
                print("----")
            
            # Write results to a temporary file
            with open('rf1_result.txt', 'w') as f:
                f.write(f"{rf1_max}\n{region_found}" if rf1_max is not None else "")
            
        finally:
            odb.close()
            
    except Exception as e:
        print(f"Error processing ODB file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: abaqus cae noGUI=extract_rf1_single.py -- odb_path")
        sys.exit(1)
    
    odb_path = sys.argv[1]
    extract_rf1_from_odb(odb_path)