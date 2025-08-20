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

def plot_orbits(o1, type1, o2, type2):
    plt.style.use('ggplot')
    indx = np.where(o1['useit']['x'])[0].astype(int)
    _, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    # Scale factor for model data
    # model_scale = 1e10 if type2 == 'model' else 1
    
    # Multiply y values by 1000 for mm
    ax[0].stem(o1['s'], np.array(o1[type1]['x']) * 1000, linefmt='#FF6F61', markerfmt='o', basefmt=" ", label=type1 + ' x orbit')
    ax[0].plot(o2['s'], np.array(o2[type1]['x']) * 1000, label=type1 + ' x region')
    ax[0].plot(o2['s'][indx[0]:indx[-1]], np.array(o2[type2]['x'])[indx[0]:indx[-1]] * 1000 * model_scale, color='#007B7F', label='fitted x region')
    ax[0].set_ylabel('x orbit [mm]')
    ax[0].set_xlabel('s [m]')
    ax[0].legend()
    
    ax[1].stem(o1['s'], np.array(o1[type1]['y']) * 1000, linefmt='#FF6F61', markerfmt='o', basefmt=" ", label=type1 + ' y orbit')
    ax[1].plot(o2['s'], np.array(o2[type1]['y']) * 1000, label=type1 + ' y region')
    ax[1].plot(o2['s'][indx[0]:indx[-1]], np.array(o2[type2]['y'])[indx[0]:indx[-1]] * 1000 * model_scale, color='#007B7F', label='fitted y region')
    ax[1].set_ylabel('y orbit [mm]')
    ax[1].set_xlabel('s [m]')
    ax[1].legend()
    plt.show(block=False)
               

#=================================================================================

# Set up plotting (optional)
tc('set plot_page size = 480 270')
tc('place top beta')
tc('place floor orbit')
tc('place middle eta ')
tc('place bottom layout')
tc('x_scale * ')
tc('scale *')

# --- Step 1: Add both a corrector kick and a quad k value kick ---
tc('set ele XCM16 BL_KICK = 0.05')      # X Corrector kick
# tc('set ele YCM22 BL_KICK = 0.0005')     # Y Corrector kick
tc('set ele QCM18 B1_GRADIENT = 1.3')     # Quad k value kick
# tc('set ele CAVL258 GRADIENT = 9000000')  # Cavity kick (optional)

# --- Step 2: Store this as the "measured" orbit ---
tc('set dat orbit.x|meas = orbit.x|model')
tc('set dat orbit.y|meas = orbit.y|model')  # Optional: Store y orbit as well

# --- Step 3: Remove the corrector kick, leave only the quad kick in the model ---
tc('set ele XCM16 BL_KICK = 0.000')       # Remove X corrector kick
# tc('set ele YCM22 BL_KICK = 0.000')       # Remove Y corrector kick
# tc('set ele QCM18 B1_GRADIENT = 1.5575E+00')       # back to design
# tc('set ele CAVL258 GRADIENT = 1.50567+07')       # Remove CAVL258 cavity kick

# --- Step 4: Fit with only a quad kick variable ---
# tao.var_create('kickFit[1]', 'XCM16', 'BL_KICK', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F', 'F', 0.01) # Optional: Add more correctors if needed
# tao.var_create('kickFit[2]', 'YCM22', 'BL_KICK', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F', 'F', 0.01) # Optional: Add more correctors if needed
tao.var_v1_create('kickFit', 1, 1) #BEAM FITTING
tao.var_create('kickFit[1]', 'QCM18', 'B1_GRADIENT', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F', 'F', 0.01)
# tao.var_create('kickFit[4]', 'CAVL258', 'GRADIENT', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F', 'F', 0.01) # Optional: Add more correctors if needed

tc('show alias')
tc('vv')
tc('vd')
tc('use var kickFit')
tc('use data orbit.x')
tc('show merit')
tc('run')

# --- Step 5: Check results ---
tc('show lat XCM16 -attr BL_KICK')
# tc('show lat YCM22 -attr BL_KICK')
tc('show lat QCM18 -attr B1_GRADIENT')
# tc('show lat CAVL258 -attr GRADIENT')

o = get_orbit(tao)
plot_orbits(o, 'meas', o, 'model')
