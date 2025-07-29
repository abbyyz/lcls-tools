pv_list = bm.all_data_maps["bpms"].pvlist
result = mod.get_machine_values(tao, bm.all_data_maps, bm.data_source, pv_list)

rf_quads_pv_list = mod.get_rf_quads_pvlist(tao, bm.all_data_maps)
energy_gain_pv_list = mod.get_energy_gain_pvlist(bm.beam_path)
pvdata = mod.get_machine_values(tao, bm.all_data_maps, bm.data_source, rf_quads_pv_list + energy_gain_pv_list, bm.date_time)

tao_cmds = mod.get_tao(pvdata, bm)
output = mod.evaluate_tao(tao, tao_cmds)



# Iterate through pvdata to update lattice elements
for element_key, value in pvdata.items():
    if element_key in measurement_to_element_map:
        lattice_element = measurement_to_element_map[element_key]
        tao.set_value(lattice_element, value)  # Modify this based on your PyTAO interface