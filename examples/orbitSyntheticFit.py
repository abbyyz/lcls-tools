from pytao import Tao

section = "BEGL3B:ENDL3B"
init_cmd = f"-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init -slice {section} -noplot"
tao = Tao(init_cmd)

elements = tao.lat_list("*", "ele.name")
z_positions = tao.lat_list("*", "ele.z")
x_orbit = tao.lat_list("*", "ele.x")

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