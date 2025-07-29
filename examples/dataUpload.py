import pandas as pd
from pytao import Tao

# Load your CSV data into a pandas DataFrame
csv_file_path = '/sdf/home/a/abbyz/bmad/measurementData.csv'
data = pd.read_csv(csv_file_path)

# Initialize the TAO environment or lattice (example)
INIT = f'-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}'
tao = Tao(INIT)

def tc(cmd):
    [print(l) for l in tao.cmd(cmd)]

# Iterate over columns (devices/parameters)
for col in data.columns:
    # Example: col = 'BPMS:HTR:460:X'
    # Get the element name and parameter from the column name
    if col.endswith(':X'):
        element_name = col[:-2]
        param = 'orbit.x|meas'
    elif col.endswith(':Y'):
        element_name = col[:-2]
        param = 'orbit.y|meas'
    elif col.endswith(':TMIT'):
        element_name = col[:-5]
        param = 'tmit|meas'
    else:
        continue  # Skip columns that don't match

    # Set the value for each row (pulse/measurement)
    for idx, value in enumerate(data[col]):
        try:
            tc(f"set data {param} {element_name} = {value}")
        except Exception as e:
            print(f"Error setting {param} for {element_name}: {e}")

print("All measurements uploaded to Tao.")