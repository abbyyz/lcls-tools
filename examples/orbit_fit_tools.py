#gets orbit
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

#plots the orbits, given two orbit data dictionaries
#o1 is the orbit data from the model, o2 is the orbit data from the
#data, type1 and type2 are the keys in the orbit data dictionaries
#that contain the x and y values to plot
#e.g. type1 = 'meas', type2 = 'model'
import matplotlib.pyplot as plt
import numpy as np
def plot_orbits(o1, type1, o2,type2):
    indx = np.where(o1['useit']['x'])[0].astype(int)
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].stem(o1['s'], o1[type1]['x'])
    ax[0].plot(o2['s'], o2[type1]['x'])
    ax[0].plot(o2['s'][indx[0]:indx[-1]], o2[type1]['x'][indx[0]:indx[-1]], color = 'cyan')
    ax[1].stem(o1['s'], o1[type1]['y'])
    ax[1].plot(o2['s'], o2[type1]['y'])
    ax[1].plot(o2['s'][indx[0]:indx[-1]], o2[type1]['y'][indx[0]:indx[-1]], color = 'cyan')
    plt.show(block=False)
