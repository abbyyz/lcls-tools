import pandas as pd
from pytao import Tao

# Load your CSV data into a pandas DataFrame
csv_file_path = '/sdf/home/a/abbyz/bmad/measurementData.csv'
data = pd.read_csv(csv_file_path)

# Initialize the TAO environment or lattice (example)
OPTIONS = "-slice BEGINNING:END -noplot "
INIT = f'-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}'
tao = Tao(INIT)

def tc(cmd):
    [print(l) for l in tao.cmd(cmd)]

# Get the number of valid orbit.x data points from Tao
num_orbit_x = len(tao.data_d_array('orbit', 'x'))

# Iterate over columns (devices/parameters)
for col in data.columns:
    if col.endswith(':X'):
        param = 'orbit.x'
    elif col.endswith(':Y'):
        param = 'orbit.y'
    elif col.endswith(':TMIT'):
        param = 'charge'
    else:
        continue

    # Set each value using the correct index
    for idx, value in enumerate(data[col]):
        if idx+1 > num_orbit_x:
            continue  # Skip out-of-bounds indices
        try:
            tc(f'set dat {param}[{idx+1}]|meas = {value}')
        except Exception as e:
            print(f'Error setting {param}[{idx+1}]|meas: {e}')

print("All measurements uploaded to Tao.")