from pytao import Tao
from lcls_tools.common.data.bmad_modeling import bmad_modeling as mod
from lcls_tools.common.data.bmad_modeling.outputs import bmad_modeling_outputs as outfn
import matplotlib.pyplot as plt
from pmd_beamphysics import ParticleGroup
import numpy as np
OPTIONS = '-slice BEGL3B:ENDL3B '

INIT = f'-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}'
tao = Tao(INIT)
tao.cmd('set ele BEGINNING:END field_master=True')

def tc(cmd):
    [print(l) for l in tao.cmd(cmd)]

    
tc('set plot_page size = 480 270')
tc('place top beta')
tc('place floor orbit')
tc('place middle eta ')
tc('place bottom layout')
tc('x_scale * 398 652') 
tc('scale *')

tc('set ele XCM16 BL_KICK = 0.0005')
tc('scale *')

# model -> data, remove kick and fit 
tao.var_v1_create('kickFit',1,1)
tao.var_create('kickFit[1]','XCM16', 'BL_KICK', 1, 0, 1E-4, -1E30, 1E30, 'limit', 'F','F',0.01)

tc('set dat orbit.x|meas = orbit.x|model')

tc('set ele XCM16 BL_KICK = 0.000')

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
