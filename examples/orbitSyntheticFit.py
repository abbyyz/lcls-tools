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