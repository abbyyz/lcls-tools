from pytao import Tao
from lcls_tools.common.data.bmad_modeling import bmad_modeling as mod
from lcls_tools.common.data.bmad_modeling.outputs import bmad_modeling_outputs as outfn
import matplotlib.pyplot as plt
from pmd_beamphysics import ParticleGroup
import numpy as np

OPTIONS = ''
INIT = f'-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}'
tao = Tao(INIT)

def tc(cmd):
    [print(l) for l in tao.cmd(cmd)]

# Set up plotting (optional)
tc('set plot_page size = 480 270')
tc('place top beta')
tc('place floor orbit')
tc('place middle eta ')
tc('place bottom layout')
tc('x_scale * ')
tc('scale *')

# --- Step 1: Add both a corrector kick and a quad k value kick ---
tc('set ele XCM16 BL_KICK = 0.0005')      # Corrector kick
tc('set ele QCM18 B1_GRADIENT = 1.3')     # Quad k value kick

# --- Step 2: Store this as the "measured" orbit ---
tc('set dat orbit.x|meas = orbit.x|model')

# --- Step 3: Remove the corrector kick, leave only the quad kick in the model ---
tc('set ele XCM16 BL_KICK = 0.000')       # Remove corrector kick
# QCM18 B1_GRADIENT remains at 1.3

# --- Step 4: Fit with only a quad kick variable ---
tao.var_v1_create('kickFit', 1, 1)
tao.var_create('kickFit[1]', 'QCM18', 'B1_GRADIENT', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F', 'F', 0.01)

tc('show alias')
tc('vv')
tc('vd')
tc('use var kickFit')
tc('use data orbit.x')
tc('show merit')

tc('run')

# --- Step 5: Check results ---
tc('show lat QCM18 -attr B1_GRADIENT')
tc('show lat XCM16 -attr BL_KICK')

# --- Step 6: Compare meas and model orbits ---
def get_orbit(tao):
    orbit_data = {}
    meas, model, design, useit = {},{},{},{}
    for plane in ['x','y']:
        val = tao.data_d_array('orbit', plane)
        meas[plane] = [item['meas_value'] for item in val]
        model[plane] = [item['model_value'] for item in val]
        design[plane] = [item['design_value'] for item in val]
        useit[plane] = [item['useit_opt'] for item in val]
    orbit_data['meas'] = meas
    orbit_data['model'] = model
    orbit_data['design'] = design
    orbit_data['element'] =  [item['ele_name'] for item in val]
    orbit_data['s'] = [tao.ele_head(ele)['s'] for ele in orbit_data['element']]
    orbit_data['ixd1'] = [item['ix_d1'] for item in val]
    orbit_data['useit'] = useit
    return orbit_data

plt.style.use('ggplot')

def plot_orbits(o1, type1, o2, type2):
    indx = np.where(o1['useit']['x'])[0].astype(int)
    _, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].stem(o1['s'], o1[type1]['x'], linefmt='#FF6F61', markerfmt='o', basefmt=" ", label=type1 + ' x orbit')
    ax[0].plot(o2['s'], o2[type1]['x'])
    ax[0].plot(o2['s'][indx[0]:indx[-1]], o2[type1]['x'][indx[0]:indx[-1]], color='#007B7F', label='fitted x region')
    ax[0].set_ylabel('x orbit')
    ax[0].set_xlabel('s [m]')
    ax[0].legend()
    ax[1].stem(o1['s'], o1[type1]['y'], linefmt='#FF6F61', markerfmt='o', basefmt=" ", label=type1 + ' y orbit')
    ax[1].plot(o2['s'], o2[type1]['y'])
    ax[1].plot(o2['s'][indx[0]:indx[-1]], o2[type1]['y'][indx[0]:indx[-1]], color='#007B7F', label='fitted y region')
    ax[1].set_ylabel('y orbit')
    ax[1].set_xlabel('s [m]')
    ax[1].legend()
    plt.show(block=False)

o = get_orbit(tao)
plot_orbits(o, 'meas', o, 'model')
