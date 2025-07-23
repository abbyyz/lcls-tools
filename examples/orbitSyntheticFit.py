from pytao import Tao
from lcls_tools.common.data.bmad_modeling import bmad_modeling as mod
from lcls_tools.common.data.bmad_modeling.outputs import (
    bmad_modeling_outputs as outfn,
)
OPTIONS = "-slice BEGINNING:ENDL3B -noplot "
INIT = f"-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}"

section = "BEGL3B:ENDL3B"
init_cmd = f"-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init -slice {section} -noplot"

tao = Tao(INIT)  # Create Tao instance first
def tc(cmd):
    [print(line) for line in tao.cmd(cmd)]

# Apply settings in Tao
element_settings = {
    "XC01B": 0.01,         # Horizontal kicker near start
    "CQ01B": 1.2,          # Example quadrupole gradient
    "BUN1B": 0.0,          # Example cavity setting
    "XC02B": 0.0,          # Another kicker
    "CQ02B": 1.0,          # Another quadrupole
    # Add more elements as needed, using names from your lattice
    # "element_name": value,
}

for ele, val in element_settings.items():
    if val is not None:
        if ":ADES" in ele or ":PDES" in ele:
            tao.cmd(f"set ele {ele} DESIGN_ENERGY = {val}")
        elif ":BDES" in ele:
            tao.cmd(f"set ele {ele} BDES = {val}")
        # Add more attribute mappings if needed
tao.cmd("set ele BEGINNING:ENDCOL0 field_master=True")

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