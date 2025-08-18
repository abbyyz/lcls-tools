from pytao import Tao
from lcls_tools.common.data.bmad_modeling import bmad_modeling as mod
from lcls_tools.common.data.bmad_modeling.outputs import bmad_modeling_outputs as outfn
import matplotlib.pyplot as plt
from pmd_beamphysics import ParticleGroup
import numpy as np

import h5py
import matplotlib.pyplot as plt
import numpy as np

from orbit_fit_tools import get_orbit, plot_orbits, show_quad_difference, allXto, allYto, plot_orbit_residuals
OPTIONS = ''    
INIT = f'-init $LCLS_LATTICE/bmad/models/sc_diag0/tao_universes.init {OPTIONS}'
#INIT = f'-init $LCLS_LATTICE/bmad/models/sc_sxr/tao.init {OPTIONS}'

tao = Tao(INIT)
tao.cmd('set ele BEGINNING:END field_master=False')

def tc(cmd):
    [print(l) for l in tao.cmd(cmd)]

tao.var_v1_create('kickFitX',1,144)
indx = 0
for u in range(1,37):
    indx = indx+1
    tao.var_create(f'kickFitX[{indx}]','XC01B', 'BL_KICK', u, 0, 1E-4, -0.2, 0.2, 'limit', 'F','F',0.01)
    indx = indx+1
    tao.var_create(f'kickFitX[{indx}]','XC02B', 'BL_KICK', u, 0, 1E-4, -0.2, 0.2, 'limit', 'F','F',0.01)
    indx = indx+1
    tao.var_create(f'kickFitX[{indx}]','YC01B', 'BL_KICK', u, 0, 1E-4, -0.2, 0.2, 'limit', 'F','F',0.01)
    indx = indx+1
    tao.var_create(f'kickFitX[{indx}]','YC02B', 'BL_KICK', u, 0, 1E-4, -0.2, 0.2, 'limit', 'F','F',0.01)

tao.var_v1_create('cavl018',1,36)
for u in range(1,37):
    tao.var_create(f'cavl018[{u}]', 'CAVL018', 'VOLTAGE', u, 0, 1E-4, 0, 19E6, 'limit', 'F','F',0.01)

    
tc('set plot_page size = 480 270')
tc('place top beta')
tc('place floor orbit')
tc('place middle eta ')
tc('place bottom layout')
tc('x_scale * ') 
tc('scale *')
o1 = get_orbit(tao)
bpms = o1['element']
quads = tao.lat_list('Quadrupole::*', 'ele.name')
quads = [q for q in quads if '#2' not in q]
quads = [q.split('#')[0] for q in quads]


tao.var_v1_create('soln2',1,6)
tao.var_create(f'soln2[1]', 'SOL2B', 'X_OFFSET', '*', 0, 1E-4, -0.015, 0.015, 'limit', 'F','F',0.01)
tao.var_create(f'soln2[2]', 'SOL2B', 'Y_OFFSET', '*', 0, 1E-4, -0.015, 0.015, 'limit', 'F','F',0.01)
tao.var_create(f'soln2[3]', 'SOL2B', 'HKICK', '*', 0, 1E-4, -0.015, 0.015, 'limit', 'F','F',0.01)
tao.var_create(f'soln2[4]', 'SOL2B', 'VKICK', '*', 0, 1E-4, -0.015, 0.015, 'limit', 'F','F',0.01)
tao.var_create(f'soln2[5]', 'SOL2B', 'BL_HKICK', '*', 0, 1E-4, -0.015, 0.015, 'limit', 'F','F',0.01)
tao.var_create(f'soln2[6]', 'SOL2B', 'BL_VKICK', '*', 0, 1E-4, -0.015, 0.015, 'limit', 'F','F',0.01)

tao.var_v1_create('tcxdg0',1,6)
tao.var_create(f'tcxdg0[1]', 'TCXDG0', 'X_OFFSET', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'tcxdg0[2]', 'TCXDG0', 'Y_OFFSET', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'tcxdg0[3]', 'TCXDG0', 'HKICK', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'tcxdg0[4]', 'TCXDG0', 'VKICK', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'tcxdg0[5]', 'TCXDG0', 'BL_HKICK', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'tcxdg0[6]', 'TCXDG0', 'BL_VKICK', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)

tao.var_v1_create('blrdg0',1,6)
tao.var_create(f'blrdg0[1]', 'BLRDG0', 'X_OFFSET', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'blrdg0[2]', 'BLRDG0', 'Y_OFFSET', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'blrdg0[3]', 'BLRDG0', 'HKICK', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'blrdg0[4]', 'BLRDG0', 'VKICK', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'blrdg0[5]', 'BLRDG0', 'BL_HKICK', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)
tao.var_create(f'blrdg0[6]', 'BLRDG0', 'BL_VKICK', '*', 0, 1E-4, -500, 500, 'limit', 'F','F',0.01)


tao.var_v1_create('umhtr',1,5)
tao.var_create(f'umhtr[1]', 'UMHTR', 'X_OFFSET', '*', 0, 1E-4, -0.005, 0.005, 'limit', 'F','F',0.01)
tao.var_create(f'umhtr[2]', 'UMHTR', 'Y_OFFSET', '*', 0, 1E-4, -0.005, 0.005, 'limit', 'F','F',0.01)
tao.var_create(f'umhtr[3]', 'UMHTR', 'X_PITCH', '*', 0, 1E-4, -1, 1, 'limit', 'F','F',0.01)
tao.var_create(f'umhtr[4]', 'UMHTR', 'Y_PITCH', '*', 0, 1E-4, -1, 1, 'limit', 'F','F',0.01)
tao.var_create(f'umhtr[5]', 'UMHTR', 'TILT', '*', 0, 1E-4, -1, 1, 'limit', 'F','F',0.01)

bends = ['BCXH1', 'BCXH2', 'BCXH3', 'BCXH4']
tao.var_v1_create('bcxh2',1,8)
indx = 0
for b in bends:
    indx = indx+1
    tao.var_create(f'bcxh2[{indx}]', b, 'ROLL', '*', 0, 1E-4, -100, 100, 'limit', 'F','F',0.01)
    indx = indx+1
    tao.var_create(f'bcxh2[{indx}]', b, 'B_FIELD', '*', 0, 1E-4, -0.05, 0.05, 'limit', 'F','F',0.01)



tao.var_v1_create('quad',1,len(quads))
for indx, quad in enumerate(quads):
    tao.var_create(f'quad[{indx+1}]',quad, 'B1_GRADIENT', '*', 0, 1E-4, -1E30, 1E30, 'limit', 'F','F',0.01)

tao.var_v1_create('quad_tilt',1,len(quads))
for indx, quad in enumerate(quads):
    tao.var_create(f'quad_tilt[{indx+1}]',quad, 'TILT', '*', 0, 1E-4, -1E30, 1E30, 'limit', 'F','F',0.01)

tao.var_v1_create('quadx_offset',1, len(quads))
for indx, quad in enumerate(quads):
    tao.var_create(f'quadx_offset[{indx+1}]', quad, 'X_OFFSET', '*', 0, 1E-4, -0.015, 0.015, 'limit', 'F','F',0.01)

tao.var_v1_create('quady_offset',1, len(quads))
for indx, quad in enumerate(quads):
    tao.var_create(f'quady_offset[{indx+1}]', quad, 'Y_OFFSET', '*', 0, 1E-4, -0.015, 0.015, 'limit', 'F','F',0.01)

tao.var_v1_create('bpmx_offset',1, len(bpms))
for indx, bpm in enumerate(bpms):
    tao.var_create(f'bpmx_offset[{indx+1}]',bpm, 'X_OFFSET', '*', 0, 1E-4, -0.015, 0.015, 'limit', 'F','F',0.01)

tao.var_v1_create('bpmy_offset',1, len(bpms))
for indx, bpm in enumerate(bpms):
    tao.var_create(f'bpmy_offset[{indx+1}]',bpm, 'Y_OFFSET', '*', 0, 1E-4, -0.015, .015, 'limit', 'F','F',0.01)

tao.var_v1_create('engy', 1, 1)
tao.var_create(f'engy[1]', 'CAVL018', 'VOLTAGE', '*', 0, 1E-4, 0, 17, 'limit', 'F','F',0.01)
   

#TODO how to get bpmList from .mat file ???
bpmList =['BPM1B', 'BPM2B', 'CMB01', 'BPM0H01', 'BPM0H04', 'BPM0H05', 'BPM0H08','BPMH1', 'BPMH2', 'BPMHD01', 'BPMHD02', 'BPMHD03', 'BPMHD04', 'BPMDG001', 'BPMDG002', 'BPMDG003', 'BPMDG004', 'BPMDG005', 'BPMDG0RF', 'BPMDG008', 'BPMDG009', 'BPMDG011', 'BPMDG012', 'BPMDG000']
quadList =[    'CQ01B',     'SQ01B' ,    'CQ02B' ,    'SQ02B' ,    'QDG001',    'QDG002',    'QDG003',    'QDG004',    'QDG005',    'QDG006',    'QDG007',    'QDG008',    'QDG009',    'QDG010',    'QDG011',    'QCM01' ,    'Q0H01' ,    'Q0H02' ,    'Q0H03' ,    'Q0H04' ,    'Q0H05' ,    'Q0H06' ,    'Q0H07' ,    'Q0H08' ,    'QHD01' ,    'QHD02' ,    'QHD03' ,'QHD04' ]


#Use RF and QUAD values from time data was taken:
#Need RF AMPL and PHAS
pvdata_rf = {'ACCL:L0B:0110:ADES':6.5, 'ACCL:L0B:0120:ADES':12, 'ACCL:L0B:0130:ADES':9.7, 'ACCL:L0B:0140:ADES':5, 'ACCL:L0B:0150:ADES':13, 'ACCL:L0B:0160:ADES':16.6, 'ACCL:L0B:0170:ADES':16.6, 'ACCL:L0B:0180:ADES':16.6, 'ACCL:L0B:0110:ADES':16.6, 'ACCL:L0B:0110:PDES':-11.5, 'ACCL:L0B:0120:PDES':-94.5, 'ACCL:L0B:0130:PDES':0, 'ACCL:L0B:0140:PDES':0, 'ACCL:L0B:0150:PDES':0, 'ACCL:L0B:0160:PDES':60.8, 'ACCL:L0B:0170:PDES':-19.1, 'ACCL:L0B:0180:PDES':19.1}


filename = 'OrbitGrid--2025-07-17-061821.mat'

with h5py.File(filename, 'r') as mat_file:
    # Explore the file structure
    for key in mat_file.keys():
        print(key)
    posxy = mat_file['data']['procOrbits']['posxy'][:]
    data = np.nanmean(mat_file['data']['xMeas'][:], axis=0)
    #bpmList = mat_file['data']['static']['bpmList'][:]
    z = mat_file['data']['static']['zBPM'][:]
    xc = mat_file['data']['xc'][:]
    yc = mat_file['data']['yc'][:]
    quadBact =  mat_file['data']['quadBACT'][:]
    quadBdes = mat_file['data']['quadBDES'][:]
    #quadList = mat_file['data']['static']['quadList'][:]

pvdata_quad = {}
for indx, quad in enumerate(quadList):
    pvdata_quad[tao.ele_head(quad)["alias"]+':BDES'] = quadBdes[0][indx].item()


#Use magnets from time data was taken
bm = mod.BmadModeling('sc_diag0', 'ARCHIVE')
#bm.date_time = '2025-07-17T08:18:00.000000-07:00' #This fails, use data from code above
output_design = mod.get_output(tao)
#rf_quads_pv_list = mod.get_rf_quads_pvlist(tao, bm.all_data_maps)
#energy_gain_pv_list = mod.get_energy_gain_pvlist(bm.beam_path);
#pvdata = mod.get_machine_values(bm.data_source,rf_quads_pv_list + energy_gain_pv_list)
pvdata = {'REFS:GUNB:950:EDES':0.0008, 'REFS:COL0:950:EDES':0.075}
pvdata.update(pvdata_quad)
#pvdata.update(pvdata_rf)

tao_cmds = mod.get_tao(pvdata, bm);

output = mod.evaluate_tao(tao, tao_cmds)

#mod.update_energy_gain_sc(tao, pvdata, 'L0', bm)

#Populate each universe with it's orbit from grid
#data.shape (74, 24, 2) 24 BPMS, 0 = x, 1 = y
#1st orbit is reference,  last orbit is reference also

refOrbitI = 0;
nGridOrbits = int(xc.size/2);
gridXindx = range(1,nGridOrbits+1)
gridYindx = range(gridXindx[-1] +1, 2*nGridOrbits+1);
reforbitLastI = refOrbitI + 2 * nGridOrbits + 1;

gridI = range(0,74)
   
o1 = get_orbit(tao)
tao.cmd("set global lattice_calc_on = F")
for universe_indx, grid_indx in enumerate(gridYindx):
    print(universe_indx)
    for orbit_indx, bpmElement in enumerate(o1['element']):
        bpm_indx = np.nonzero(np.isin(bpmList, bpmElement))[0]
        x_value = posxy[grid_indx, bpm_indx, 0]
        y_value = posxy[grid_indx, bpm_indx, 1]
        #x_value = data[grid_indx, bpm_indx, 0] - data[0, bpm_indx, 0] #subtract reference orbit
        #y_value = data[grid_indx, bpm_indx, 1] - data[0, bpm_indx, 1]
        #x_value = x_value * 1000
        #y_value = y_value * 1000
        #x_value = data[grid_indx, bpm_indx, 0] 
        #y_value = data[grid_indx, bpm_indx, 1] 
        tc(f'set dat {universe_indx+1}@orbit.x[{orbit_indx+1}]|meas = {x_value[0]}')
        tc(f'set dat {universe_indx+1}@orbit.y[{orbit_indx+1}]|meas = {y_value[0]}')

tao.cmd("set global lattice_calc_on = T")
tc('scale *')
tc('set global%n_opti_cycles =  2412')
STOP
#Fit each universe with 1st 2 X,Y CORS (what was used in grid)
for u in range(1,37):
    tc(f'set default universe = {u}')
    tc('vv')
    tc('vd')
    tc(f'use var kickFitX[{4*u-3}:{4*u}]') #x and y
    #tc(f'use var kickFitX[{4*u-3}:{4*u-2}]') #x only
    tc(f'use data {u}@orbit.x[1:5]')
    tc(f'use data {u}@orbit.y[1:5]')
    tc('run')
    tc('scale *')

plot_orbit_residuals(tao)

for u in range(1,37,4):
    tc(f'set default universe = {u}')
    tc(f'use data {u}@orbit.x[1:5]')
    tc(f'use data {u}@orbit.y[1:5]')
    o = get_orbit(tao)
    plot_orbits(o, 'meas', o, 'model', f'Universe: {u}', figN = u)

# Fit ################################
tc('vv')
tc('vd') 
tc('use data *@orbit.x[10:24]')
tc('use data *@orbit.y[10:24]')
tc('use var bpmx_offset[10:24]')
tc('use var bpmy_offset[10:24]')
tc('use var quadx_offset[11:25]')
tc('use var quady_offset[11:25]')
#tc('use var quad_tilt[11:25]')
tc('use var quad[11:25]')
tc('use var  blrdg0')
tc('use var  tcxdg0')
tc('use var xcor[11:18]')
tc('use var ycor[11:18]')
show_quad_difference(tao)

tc('use var bcxh2')

tc('use var bpmx_offset[5:13]')
tc('use var bpmy_offset[5:13]')
tc('use var quadx_offset[3:10]')
tc('use var quady_offset[3:10]')

tc('use var quad_tilt[3:10]')

tc('use var quad[3:10]')

for u in range(1,37,3):
    tc(f'set default universe = {u}')
    tc(f'use data {u}@orbit.x[10:19]')
    tc(f'use data {u}@orbit.y[10:19]')
    o = get_orbit(tao)
    plot_orbits(o, 'meas', o, 'model', f'Universe: {u}', figN = u)


for u in range(1,37):
    tc(f'set default universe = {u}')
    tc('vv')
    tc('vd')
    tc(f'use data {u}@orbit.x[6:24]')
    tc(f'use data {u}@orbit.y[6:24]')
    tc('use var bpmx_offset[6:24]')
    tc('use var bpmy_offset[6:24]')
    tc('run')
    tc('scale *')

tc('show var cavl018')
tc('show var  bpmx_offset')
    
for u in range(1,37,6):
    tc(f'set default universe = {u}')
    tc(f'use data {u}@orbit.x[8:17]')
    tc(f'use data {u}@orbit.y[8:17]')
    o = get_orbit(tao)
    plot_orbits(o, 'meas', o, 'model', f'Universe: {u}')

#Now fit with many parameters
tc('set var soln2|model = soln2|design')
#tc('set var kickFitX|model = kickFitX|design')
tc('set var quad|model  =  quad|design')
tc('set var quad_tilt|model = quad_tilt|design')
tc('set var quadx_offset|model = quadx_offset|design')
tc('set var quady_offset|model = quady_offset|design')
tc('set var bpmx_offset|model = bpmx_offset|design')
tc('set var bpmy_offset|model = bpmy_offset|design')
tc('set var engy|model = engy|design')
tc('set var xcor|model = xcor|design')
tc('set var ycor|model = ycor|design')
tc('set var umhtr|model= umhtr|design')
tc('set var  blrdg0|model = blrdg0|design')
tc('set var  tcxdg0|model = tcxdg0|design')
tc('scale *')
## Now start looking for errors 
tc('vv')
tc('vd')
#tc('use var quad[9:25]')
tc('use var bpmx_offset[5:14]')
tc('use var bpmy_offset[5:14]')
tc('use var quadx_offset[7:25]')
tc('use var quady_offset[7:25]')
tc('use var quad_tilt[7:25]')
#tc('use var xcor[9:18]')
#tc('use var ycor[9:18]')
tc(f'use data *@orbit.x[5:14]')
tc(f'use data *@orbit.y[5:14]')
tc(f'use var engy')

tc('run')

tc('show var quad_tilt')
tc('show var quadx_offset')
tc('show var quady_offset')
tc('show var soln2')

    
for u in range(1,36,4):
    tc(f'set default universe = {u}')
    tc(f'use data {u}@orbit.x[6:14]')
    tc(f'use data {u}@orbit.y[6:14]')
    o = get_orbit(tao)
    plot_orbits(o, 'meas', o, 'model', f'Universe: {u}')


#SOLN2 kicks show as y orbit?
tc('vv')
tc('vd')
tc('use var soln2')
tc('use var ycor[1:4]')
tc(f'use data *@orbit.x[1:5]')
tc(f'use data *@orbit.y[1:5]')
tc('use var bpmx_offset[1:5]')
tc('use var bpmy_offset[1:5]')
tc('run')
tc('scale *')

    
    
tc('show var bpmx_offset')
tc('show var bpmy_offset')
tc('show var quadx_offset')
tc('show var quady_offset')
tc('show var quad_tilt')
tc('show var quad')

tc('show var kickFitX')
tc('show var soln2')
tc('show var engy')
show_quad_difference(tao)

import importlib
importlib.reload(orbit_fit_tools)

for indx, quad in enumerate(quadList[4:-1]):
    print(f'{quad} {quadBdes[0][indx+4]:7.2} {mod.get_bmad_bdes(tao,quad):7.2}')




    
