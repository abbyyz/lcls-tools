import h5py
import numpy as np
from scipy.io import loadmat
from pytao import Tao
from lcls_tools.common.data.bmad_modeling import bmad_modeling as mod

# Step 1: Load the MATLAB Data
file_path = '/mccfs2/u1/lcls/matlab/data/2025/2025-07/2025-07-08/OnlineMonitor-orbitSearchSynch-BSA-2025-07-08--16-59-05-765.mat'
f = h5py.File(file_path, 'r')

# Scalars: shape [num_devices, num_pulses] in HDF5, so you may need to transpose
scalars = np.array(f['Data']['Scalars']).T  # Now [num_pulses, num_devices]
scalars_list = [b''.join(f['Data']['ScalarsList'][i][0]).decode() for i in range(f['Data']['ScalarsList'].shape[0])]

# Find indices for X and Y BPMs
x_indices = [i for i, name in enumerate(scalars_list) if ':X' in name]
y_indices = [i for i, name in enumerate(scalars_list) if ':Y' in name]

# Example: Use the first X and Y BPMs (or loop over all)
x_data = scalars[:, x_indices[0]]  # First BPM X column
y_data = scalars[:, y_indices[0]]  # First BPM Y column

# If you want all BPMs, you can build arrays:
all_x_data = scalars[:, x_indices]  # shape: [num_pulses, num_bpms]
all_y_data = scalars[:, y_indices]

# Step 2: Setup TAO
OPTIONS = "-slice BEGINNING:END -noplot"
INIT = f"-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}"
tao = Tao(INIT)
tao.cmd("set ele BEGINNING:ENDCOL0 field_master=True")

def tc(cmd):
    [print(l) for l in tao.cmd(cmd)]

# from pytao import Tao
# from lcls_tools.common.data.bmad_modeling import bmad_modeling as mod
# from lcls_tools.common.data.bmad_modeling.outputs import bmad_modeling_outputs as outfn
# import matplotlib.pyplot as plt
# from pmd_beamphysics import ParticleGroup
# import numpy as np
# OPTIONS = '-slice BEGL3B:ENDL3B '

# INIT = f'-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}'
# tao = Tao(INIT)
# tao.cmd('set ele BEGL3B:ENDL3B field_master=True')

# def tc(cmd):
#     [print(l) for l in tao.cmd(cmd)]



# Get BPM PV List 
bm = mod.BmadModeling("sc_sxr", "DES")
pv_list = bm.all_data_maps["bpms"].pvlist

# Step 3: Set Data in TAO
for i, pv in enumerate(pv_list):
    if i < num_pulses:
        # Set the measured x and y data for each BPM
        tc(f'set data {i + 1}@orbit.x|meas = {x_data[i]:.6e} ')
        tc(f'set data {i + 1}@orbit.y|meas = {y_data[i]:.6e} ')

# Step 4: Verify the Data
tc('show data orbit.x[1:5]')  # Adjust the range as needed to see your data
tc('show data orbit.y[1:5]')