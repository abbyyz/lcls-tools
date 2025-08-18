import numpy as np
import matplotlib.pyplot as plt

def get_orbit(tao):
    orbit_data = {}
    meas, model, design, useit = {},{},{},{}
    for plane in ['x','y']:
        val = tao.data_d_array('orbit', plane)
        meas[plane] = [1000* item['meas_value'] for item in val]
        model[plane] = [1000*item['model_value'] for item in val]
        design[plane] = [1000*item['design_value'] for item in val]
        useit[plane] = [item['useit_opt'] for item in val]
    orbit_data['meas'] = meas
    orbit_data['model'] = model
    orbit_data['design'] = design
    orbit_data['element'] =  [item['ele_name'] for item in val]
    orbit_data['s'] = [tao.ele_head(ele)['s'] for ele in orbit_data['element']]
    orbit_data['ixd1'] = [item['ix_d1'] for item in val]
    orbit_data['useit'] = useit
    return orbit_data

def plot_orbits(o1, type1, o2,type2, title_v='',figN = 1):
    indx = np.where(o1['useit']['x'])[0].astype(int)
    plt.figure(figN)
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    ax1.stem(o1['s'], o1[type1]['x'])
    ax1.plot(o2['s'], o2[type2]['x'])
    ax1.plot(o2['s'][indx[0]:indx[-1]],
             o2[type2]['x'][indx[0]:indx[-1]], color = 'cyan')
    ax1.set_title(title_v)
    ax1.set_ylabel('X (mm)')
    ax2.stem(o1['s'], o1[type1]['y'])
    ax2.plot(o2['s'], o2[type2]['y'])
    ax2.plot(o2['s'][indx[0]:indx[-1]],
             o2[type2]['y'][indx[0]:indx[-1]], color = 'cyan')
    ax2.set_ylabel('Y (mm)')
    ax2.set_xlabel('Z (m)')
    plt.show(block=False)

def plot_orbit_residuals(tao):
    for u in range(1,37):
        plt.figure
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)
        tao.cmd(f'set default universe = {u}')
        o = get_orbit(tao)
        res_x, res_y = [], []
        for indx in range(0, len(o['meas']['x'])):
            res_x.append(o['meas']['x'][indx] -
                         o['model']['x'][indx])
            res_y.append(o['meas']['y'][indx] -
                         o['model']['y'][indx])
        ax1.plot(o['s'], res_x)
        ax2.plot(o['s'], res_y)
    ax1.set_title('Residuals')
    ax1.set_ylabel(' X (mm)')
    ax1.grid(True)
    ax2.set_ylabel(' Y (mm)')
    ax2.set_xlabel(' z (m)')
    ax2.grid(True)
    plt.show(block=False)
    

    
    
def show_quad_difference(tao):
    print('B1_GRADIENT:')
    print(f'QUAD Model Desing %')
    val = tao.var_v_array('quad')
    for indx, v in enumerate(val):
        name = v['var_attrib_name']
        model = v['model_value']
        design = v['design_value']
        percent = 100 * (model-design)/design if design != 0 else 0
        print(f'{name:12} {model:8.2f} {design:8.2f} {percent:8.1f}')


    
def allXto(xlim):
    fig_numbers = plt.get_fignums()
    for fig_num in fig_numbers:
        fig = plt.figure(fig_num)
        axes = fig.get_axes()
        for ax in axes:
            ax.set_xlim(xlim)
        plt.draw()
    
def allYto(ylim):
    fig_numbers = plt.get_fignums()
    for fig_num in fig_numbers:
        fig = plt.figure(fig_num)
        axes = fig.get_axes()
        for ax in axes:
            ax.set_ylim(ylim)
        plt.draw()
    
    
