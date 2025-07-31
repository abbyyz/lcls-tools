from pytao import Tao
from lcls_tools.common.data.bmad_modeling import bmad_modeling as mod
from lcls_tools.common.data.bmad_modeling.outputs import bmad_modeling_outputs as outfn
import matplotlib.pyplot as plt
from pmd_beamphysics import ParticleGroup
import numpy as np
OPTIONS = '-slice BEGL3B:ENDL3B '
INIT = f'-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}'
#INIT = f'-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}'

tao = Tao(INIT)
#tao.cmd('set ele BEGINNING:END field_master=True')

def tc(cmd):
    [print(l) for l in tao.cmd(cmd)]

    
tc('set plot_page size = 480 270')
tc('place top beta')
tc('place floor orbit')
tc('place middle eta ')
tc('place bottom layout')
tc('x_scale * ') 
tc('scale *')

tc('set ele XCM16 BL_KICK = 0.0005')
tc('scale *')

# model -> data, remove kick and fit 
tao.var_v1_create('kickFit2',1,2)
tao.var_create('kickFit2[1]','XCM16', 'BL_KICK', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F','F',0.01)
tao.var_create('kickFit2[2]','QCM18', 'B1_GRADIENT', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F','F',0.01)

tc('set dat orbit.x|meas = orbit.x|model')

tc('set ele XCM16 BL_KICK = 0.000')

def get_orbit():
    orbit_data = {}
    meas, model, design = {},{},{}
    for plane in ['x','y']:
        val = tao.data_d_array('orbit', plane)
        meas[plane] = [item['meas_value'] for item in val]
        model[plane] = [item['model_value'] for item in val]
        design[plane] = [item['design_value'] for item in val]
    orbit_data['meas'] = meas
    orbit_data['model'] = model
    orbit_data['design'] = design
    orbit_data['element'] =  [item['ele_name'] for item in val]
    return orbit_data


tc('show alias')
tc('vv')
tc('vd')
tc('use var kickFit')
tc('use data orbit.x')
tc('show merit')

#These above will use the optimizer (default settings) to find a kick at
# the variable elements.  The kick will be the best fit of the model to the
#orbit we previously generated.

tc('run')

#checkes that optimizer set the corrector XCM16 BL_KICK to the value
#we set it manualy before to generate the data
tc('show lat  XCM16 -attr BL_KICK')

#Now look at  quad kicks

#1.5575E+00
tc('show lat QCM18 -attr B1_GRADIENT')


tc('set ele QCM18  B1_GRADIENT = 1.3')


tc('set dat orbit.x|meas = orbit.x|model')
tao.var_v1_create('kickFit2',1,2)
tao.var_create('kickFit2[1]','XCM16', 'BL_KICK', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F','F',0.01)
tao.var_create('kickFit2[2]','QCM18', 'B1_GRADIENT', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F','F',0.01)
tc('show alias')
tc('vv')
tc('vd')
tc('use var kickFit2')
tc('use data orbit.x')
tc('show merit')


tc('set ele XCM16 BL_KICK = 0.000') #back to desing
tc('set ele QCM18  B1_GRADIENT = 1.5575E+00') #Back to design

#Did the fit find 1.3 for quad and  0.0005 for corrector?
tc('show lat QCM18 -attr B1_GRADIENT')
tc('show lat  XCM16 -attr BL_KICK')

