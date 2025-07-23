from pytao import Tao
from lcls_tools.common.data.bmad_modeling import bmad_modeling as mod
from lcls_tools.common.data.bmad_modeling.outputs import (
    bmad_modeling_outputs as outfn,
)
OPTIONS = -"slice BEGINNING:ENDL3B -noplot "
INIT = f"-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}"

section = "BEGL3B:ENDL3B"
init_cmd = f"-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init -slice {section} -noplot"

# Set element values for this section   
element_settings = {
    'ACCL:L3B:2680:ADES': 0.0,
    'ACCL:L3B:1670:ADES': 18.68,
    'ACCL:L3B:1950:PDES': 0.0,
    'QUAD:L3B:1885:BDES': -3.7177067,
    'ACCL:L3B:2970:PDES': -18.59487075086617,
    'ACCL:L3B:3120:ADES': 16.6,
    'ACCL:L3B:3210:PDES': 24.17171409887307,
    'ACCL:L3B:1740:ADES': 16.0,
    'ACCL:L3B:1880:ADES': 16.59,
    'ACCL:L3B:2240:ADES': 18.68,
    'ACCL:L3B:2130:ADES': 16.59,
    'ACCL:L3B:3140:ADES': 16.6,
    'ACCL:L3B:2620:ADES': 18.68,
    'ACCL:L3B:2340:ADES': 16.59,
    'ACCL:L3B:2320:ADES': 16.59,
    'ACCL:L3B:2530:ADES': 14.59,
    'ACCL:L3B:1810:ADES': 15.99,
    'ACCL:L3B:1820:ADES': 12.5,
    'ACCL:L3B:3260:ADES': 16.6,
    'ACCL:L3B:3080:ADES': 16.6,
    'ACCL:L3B:2930:ADES': 18.68,
    'ACCL:L3B:2740:ADES': 16.6,
    'ACCL:L3B:1630:ADES': 16.2,
    'ACCL:L3B:2920:ADES': 12.09,
    # Add more as needed for your section
}

# Apply settings in Tao
for ele, val in element_settings.items():
    if val is not None:
        if ":ADES" in ele or ":PDES" in ele:
            tao.cmd(f"set ele {ele} DESIGN_ENERGY = {val}")
        elif ":BDES" in ele:
            tao.cmd(f"set ele {ele} BDES = {val}")
        # Add more attribute mappings if needed
tao = Tao(INIT)
tao.cmd("set ele BEGINNING:ENDCOL0 field_master=True")
def tc(cmd):
    [print(line) for line in tao.cmd(cmd)]

elements = tao.lat_list("*", "ele.name")
z_positions = tao.lat_list("*", "ele.z")
x_orbit = tao.lat_list("*", "ele.x")

print("z_positions:", z_positions)
print("x_orbit:", x_orbit)
print("Length z_positions:", len(z_positions))
print("Length x_orbit:", len(x_orbit))

import matplotlib.pyplot as plt
plt.plot(z_positions, x_orbit, label="X Orbit")
plt.xlabel("Z [m]")
plt.ylabel("X [mm]")
plt.title("X vs. Z orbit")
plt.legend()
plt.show()

corrector = "XCxxxx"  # Replace with actual corrector name near BEGL3B
# Get current BDES
bdes_orig = tao.ele_gen_attribs(corrector)["BL_GRADIENT"]
# Change BDES
tao.cmd(f"set ele {corrector} BL_GRADIENT = {bdes_orig + 0.01}")  # Small kick
# Recalculate lattice
tao.cmd("run")
# Plot new orbit
x_orbit_new = tao.lat_list("*", "orbit.x")
plt.plot(z_positions, x_orbit_new, label="X Orbit (after kick)")
plt.legend()
plt.show()

quad = "QUADxxxx"  # Replace with actual quad name after corrector
# Change gradient
quad_grad_orig = tao.ele_gen_attribs(quad)["B1_GRADIENT"]
tao.cmd(f"set ele {quad} B1_GRADIENT = {quad_grad_orig * 1.05}")
tao.cmd("run")
x_orbit_quad = tao.lat_list("*", "orbit.x")
plt.plot(z_positions, x_orbit_quad, label="X Orbit (quad changed)")
plt.legend()
plt.show()

# Change X_OFFSET
tao.cmd(f"set ele {quad} X_OFFSET = 0.001")
tao.cmd("run")
x_orbit_offset = tao.lat_list("*", "orbit.x")
plt.plot(z_positions, x_orbit_offset, label="X Orbit (quad X_OFFSET)")
plt.legend()
plt.show()

# Change X_PITCH
tao.cmd(f"set ele {quad} X_PITCH = 0.001")
tao.cmd("run")
x_orbit_pitch = tao.lat_list("*", "orbit.x")
plt.plot(z_positions, x_orbit_pitch, label="X Orbit (quad X_PITCH)")
plt.legend()
plt.show()

# Change corrector again
tao.cmd(f"set ele {corrector} BL_GRADIENT = {bdes_orig + 0.02}")
tao.cmd("run")
x_orbit = tao.lat_list("*", "orbit.x")
y_orbit = tao.lat_list("*", "orbit.y")
plt.plot(z_positions, x_orbit, label="X Orbit")
plt.plot(z_positions, y_orbit, label="Y Orbit")
plt.legend()
plt.show()

# Rotate quad about z axis (theta in radians)
tao.cmd(f"set ele {quad} TILT = 0.05")  # ~2.9 degrees
tao.cmd("run")
x_orbit_coupled = tao.lat_list("*", "orbit.x")
y_orbit_coupled = tao.lat_list("*", "orbit.y")
plt.plot(z_positions, x_orbit_coupled, label="X Orbit (coupled)")
plt.plot(z_positions, y_orbit_coupled, label="Y Orbit (coupled)")
plt.legend()
plt.show()

plt.plot(z_positions, x_orbit_coupled - x_orbit, label="ΔX Orbit (coupling)")
plt.plot(z_positions, y_orbit_coupled - y_orbit, label="ΔY Orbit (coupling)")
plt.xlabel("Z [m]")
plt.ylabel("Δ Orbit [mm]")
plt.title("Difference Orbits After Quad Rotation")
plt.legend()
plt.show()

import numpy as np
print("Any NaNs in x_orbit?", np.any(np.isnan(x_orbit)))
print("Any NaNs in z_positions?", np.any(np.isnan(z_positions)))