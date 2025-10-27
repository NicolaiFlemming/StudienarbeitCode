from odbAccess import openOdb
import sys
import os

def extract_rf1_from_odb(odb_path):
    """Extract RF1 value from a single ODB file."""
    try:
        odb = openOdb(odb_path)
        rf1_max = None
        
        try:
            step = odb.steps['Step-1']
            
            # Search all regions for RF1
            for region_name, region in step.historyRegions.items():
                if 'RF1' in region.historyOutputs.keys():
                    rf1_data = region.historyOutputs['RF1'].data
                    rf1_local_max = max(v[1] for v in rf1_data)
                    if rf1_max is None or rf1_local_max > rf1_max:
                        rf1_max = rf1_local_max
            
            # Write result to a temporary file
            with open('rf1_result.txt', 'w') as f:
                f.write(str(rf1_max))
            
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