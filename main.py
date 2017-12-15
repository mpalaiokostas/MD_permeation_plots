# -*- coding: utf-8 -*-
"""
@author: Michalis Palaiokostas
"""

import os
import pandas as pd
from classes.data_munging import SummaryFile, MoleculesFile
from classes.plotting_matplotlib import GridPlot, LogPlot

# USER INPUT ##################################################################


# FUNCTIONS ###################################################################
def plot_grid_figure():
    # Load molecular properties
    file_location = directory_source_data
    file_name = 'molecules.csv'
    molecules = MoleculesFile(os.path.join(file_location, file_name))
    molecules_data = molecules.raw_data()

    # Define information of results to be plotted
    results_dict = {'result': ['pmf', 'diffusion', 'resistance', 'hbonds'],
                    'yaxis': [
                        'Free-energy\n$\Delta G$ $[ kcal \, mol^{-1} ]$',
                        'Local diffusion\n$[\cdot 10^{-5} \, cm^2 \, s^{-1}]$',
                        'Local resistance\n$[\cdot 10^{6} \, s^{-1} \, cm^2 ]$',
                        'Hydrogen bonds\nper frame']}
    results_info = pd.DataFrame(data=results_dict)

    # Create figure object to be populated
    fig_object = GridPlot(font_name='Droid Sans',
                          font_dirs=os.path.join(directory_work, 'fonts'),
                          x_label='Distance from bilayer centre [$nm$]')

    # Load each case in the figure
    for col, res in enumerate(results_info['result']):
        print('Plotting:', res)
        file_location = os.path.join(directory_source_data, res)

        for row, mol in enumerate(molecules_data['Type']):
            print('    Molecule:', mol)

            if res == 'resistance':
                # continue
                file_name = f'ba-Summary--{res}--{mol}.dat'
                file_object = SummaryFile(os.path.join(file_location, file_name))
                filtered_data = file_object.filter_positions_columns(
                    ['position', 'DOPC_mean', 'DOPC_se', 'MIX_mean', 'MIX_se'])
                fig_object.add_case(13, 4, row * 4 + col,
                                    filtered_data, logarithmic=True)
                y_limits = (
                    ('molecule', 'ymin_lim', 'ymax_lim', 'ymajor_sp', 'yminor_sp'),
                    ('nh3', 1e-6, 1e6),
                    ('h2o', 1e-6, 1e6),
                    ('ch3f', 1e-2, 1e2),
                    ('co2', 1e-2, 1e2),
                    ('c3h8', 1e-4, 1e4),
                    ('c2h6o', 1e-4, 1e4),
                    ('ch4n2o', 1e-12, 1e12),
                    ('c3h8o', 1e-3, 1e3),
                    ('c2h5no2', 1e-6, 1e6),
                    ('c6h6o', 1e-3, 1e3),
                    ('c7h6o2', 1e-3, 1e3),
                    ('c9h6o2', 1e-2, 1e2),
                    ('c8h9no2', 1e-6, 1e6))

                for i, line in enumerate(y_limits):
                    if mol == line[0]:
                        ymin_lim = line[1]
                        ymax_lim = line[2]

                fig_object.add_grid_limits_ticks(xaxis_limits=(0, 2.7),
                                                 xmajor_spacing=0.5,
                                                 xminor_spacing=0.1,
                                                 yaxis_limits=(ymin_lim, ymax_lim))

            elif res == 'hbonds':
                # continue
                for hbond in ['totals', 'lipids', 'waters']:
                    hbond_location = os.path.join(file_location, hbond)
                    file_name = f'ba-Summary--{res}--{hbond}--vmd--{mol}.dat'
                    file_object = SummaryFile(os.path.join(hbond_location,
                                                           file_name))
                    filtered_data = file_object.filter_positions_columns(
                        ['position', 'DOPC_mean', 'DOPC_se',
                         'MIX_mean', 'MIX_se'])
                    fig_object.add_case(13, 4, row * 4 + col,
                                        filtered_data, logarithmic=False)
                    fig_object.add_grid_limits_ticks(xaxis_limits=(0, 2.7),
                                                     yaxis_limits=(0, 1.6),
                                                     ymajor_spacing=0.4,
                                                     xmajor_spacing=0.5,
                                                     yminor_spacing=0.2,
                                                     xminor_spacing=0.1)

            elif res == 'diffusion':
                # continue
                file_name = f'ba-Summary--{res}--{mol}.dat'
                file_object = SummaryFile(os.path.join(file_location, file_name))
                filtered_data = file_object.filter_positions_columns(
                    ['position', 'DOPC_mean', 'DOPC_se', 'MIX_mean', 'MIX_se'])
                fig_object.add_case(13, 4, row * 4 + col,
                                    filtered_data, logarithmic=False)
                fig_object.add_grid_limits_ticks(xaxis_limits=(0, 2.7),
                                                 xmajor_spacing=0.5,
                                                 xminor_spacing=0.1,
                                                 yaxis_limits=(0, 3),
                                                 ymajor_spacing=1.0,
                                                 yminor_spacing=0.5)
            else:
                # continue
                file_name = f'ba-Summary--{res}--{mol}.dat'
                file_object = SummaryFile(os.path.join(file_location, file_name))
                filtered_data = file_object.filter_positions_columns(
                    ['position', 'DOPC_mean', 'DOPC_se', 'MIX_mean', 'MIX_se'])
                fig_object.add_case(13, 4, row * 4 + col,
                                    filtered_data, logarithmic=False)
                y_limits = (
                    ('molecule', 'ymin_lim', 'ymax_lim', 'ymajor_sp', 'yminor_sp'),
                    ('nh3', 0.0, 6.0, 2.0, 1.0),
                    ('h2o', 0.0, 9.0, 3.0, 1.5),
                    ('ch3f', -0.8, 0.8, 0.8, 0.4),
                    ('co2', -1.2, 0.6, 0.6, 0.4),
                    ('c3h8', -4, 2, 2, 1),
                    ('c2h6o', -2, 4, 2, 1),
                    ('ch4n2o', 0, 12, 4, 2),
                    ('c3h8o', -2, 4, 2, 1),
                    ('c2h5no2', 0.0, 9.0, 3.0, 1.5),
                    ('c6h6o', -4, 2, 2, 1),
                    ('c7h6o2', -4, 2, 2, 1),
                    ('c9h6o2', -4, 2, 2, 1),
                    ('c8h9no2', -3, 6, 3, 1.5))

                for line in y_limits:
                    if mol == line[0]:
                        ymin_lim = line[1]
                        ymax_lim = line[2]
                        ymajor_sp = line[3]
                        yminor_sp = line[4]

                fig_object.add_grid_limits_ticks(xaxis_limits=(0, 2.7),
                                                 xmajor_spacing=0.5,
                                                 xminor_spacing=0.1,
                                                 yaxis_limits=[ymin_lim, ymax_lim],
                                                 ymajor_spacing=ymajor_sp,
                                                 yminor_spacing=yminor_sp)

    # Add legend
    # fig_object.add_legend(['DOPC','MIX'])

    # Add titles
    new_mol_nam = [l.replace('\\n', '\n') for l in molecules_data['Name'].tolist()]
    fig_object.add_titles(new_mol_nam, results_info['yaxis'])

    # Save figure in output directory
    # Note: file_name should not have format as this is given as keyword
    file_location = directory_figures
    file_name = 'all_results'
    fig_object.save_figure(os.path.join(file_location, file_name),
                           ['pdf', 'png'])
    return


def plot_log_figure():
    # Load molecular properties
    file_location = directory_source_data
    file_name = 'molecules.csv'
    molecules = MoleculesFile(os.path.join(file_location, file_name))
    molecules_data = molecules.raw_data()

    # Load data
    file_location = directory_source_data
    file_name = f'ba-Summary--logP--Hummer_Method.dat'
    file_object = SummaryFile(os.path.join(file_location, file_name))
    filtered_data = file_object.filter_columns(
        ['molecule', 'DOPC_mean', 'DOPC_se', 'MIX_mean', 'MIX_se'])

    # Merge datasets to allow better plotting
    df = filtered_data
    merged_data = df.merge(molecules_data, left_on='molecule', right_on='Type')
    merged_data = merged_data.sort_values('MolWeight')
    merged_data['Name'] = merged_data['Name'].replace(regex=True,
                                                      to_replace=r'\\n',
                                                      value=r' ')
    merged_data['Name'] = merged_data['Name'].replace(regex=True,
                                                      to_replace=r'- ',
                                                      value=r'')
    # Create plot
    fig_object = LogPlot(font_name='Droid Sans',
                         font_dirs=os.path.join(directory_work, 'fonts'),
                         x_label='logP DOPC',
                         y_label='logP DOPC:DOPE(1:3)')
    fig_object.add_grid_limits((-7, 2), (-7, 2), 1, 1, 0.5, 0.5)
    fig_object.plot_data(merged_data, 'Name')
    fig_object.add_legend()
    file_location = directory_figures
    file_name = 'logP'
    fig_object.save_figure(os.path.join(file_location, file_name),
                           ['pdf', 'png'])

    return


# EXECUTE SCRIPT ##############################################################
if __name__ == '__main__':

    # User input
    """TODO: Add arguments"""
    dir_source_name = 'source_data'
    dir_figures_name = 'figures'

    # The directory from which main.py is called
    directory_work = os.getcwd()
    # The directory of main.py
    directory_module = os.path.dirname(os.path.realpath(__file__))
    # Other directories
    directory_source_data = os.path.join(directory_work, dir_source_name)
    directory_figures = os.path.join(directory_work, dir_figures_name)
    if not os.path.exists(directory_figures):
        os.makedirs(directory_figures)

    # Plotting results
    plot_grid_figure()
    plot_log_figure()


