# -*- coding: utf-8 -*-
"""
@author: Michalis Palaiokostas
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
import numpy as np


class GridPlot:
    def __init__(self, font_name='', font_dirs='', x_label=''):
        self.fig = plt.figure(figsize=(8.27, 11.69), dpi=100)  # A4 Size
        # self.fig = plt.figure(figsize=(11.69, 16.53), dpi=100)  # A3 Size
        self.axG = self.fig.add_subplot(111)

        # Change fonts if other is provided
        if font_name != '':
            '''
            Solution found at: https://stackoverflow.com/questions/35668219/\
            how-to-set-up-a-custom-font-with-custom-path-to-matplotlib-global-font
            '''
            self.font = font_name
            font_files = fm.findSystemFonts(fontpaths=font_dirs)
            font_list = fm.createFontList(font_files)
            fm.fontManager.ttflist.extend(font_list)
            plt.rcParams['font.family'] = self.font
        self.title_font_sz = 8
        self.ticks_font_size = 7
        plt.rcParams.update({'font.size': self.ticks_font_size})

        # Turn off axis lines and ticks of the big subplot
        self.axG.spines['top'].set_color('none')
        self.axG.spines['bottom'].set_color('none')
        self.axG.spines['left'].set_color('none')
        self.axG.spines['right'].set_color('none')
        self.axG.tick_params(labelcolor='w', top='off',
                             bottom='off', left='off', right='off')
        self.axG.set_xticklabels([])
        self.axG.set_yticklabels([])
        self.axG.set_xlabel(x_label, labelpad=15, fontsize=self.title_font_sz)
        plt.subplots_adjust(wspace=0.3, hspace=0.3)

        self.colours = ['#1b9e77', '#d95f02', '#7770b3']
        '''
        '#1b9e77'  # Green
        '#d95f02'  # Red
        '#7770b3'  # Purple
        '''

        self.linestyles = ['-', '--', ':']
        self.position_calls = [[0, 0]]

        self.first_row_axes = []
        self.first_column_axes = []
        return

    def add_case(self, n_rows, n_cols, position, dataframe, logarithmic=False):
        """
        Adds a subplot to the current figure. Axes scale are normal unless
        specified otherwise by the logarithmic boolean.
        Input:  The number or rows and columns of the figure.
                The position of the subplot
                A dataframe where the 1st column is common for all included
                datasets and each dataset consists of 2 columns (the average
                and the standard error).
                (Optional) a boolean to enable logarithmic scales.
        Output: A subplot with a number of lines equal to the number of
                datasets. (N-1)/2
        """

        # Identify if this position has been called before and if yes
        # plot in a different linestyle.
        if self.position_calls[-1][0] != int(position + 1):
            self.position_calls.append([position + 1, 1])
        else:
            self.position_calls[-1][1] += 1
        line_style = self.linestyles[self.position_calls[-1][1] - 1]

        # Set subplot properties    
        df = dataframe
        self.ax = self.fig.add_subplot(n_rows, n_cols, position + 1)
        if logarithmic is True:
            self.ax.set_yscale('log')

        # Load datasets
        number_sets = int((len(df.columns) - 1) / 2)
        for s in range(number_sets):
            # Plot mean values
            plt.plot(df.ix[:, 0], df.ix[:, (s * 2) + 1],
                     color=self.colours[s], linewidth=3, linestyle=line_style)

            # Plot standard errors
            plt.fill_between(df.ix[:, 0],
                             df.ix[:, (s * 2) + 1] - df.ix[:, (s * 2) + 2],
                             df.ix[:, (s * 2) + 1] + df.ix[:, (s * 2) + 2],
                             alpha=0.4, linewidth=0,
                             edgecolor=self.colours[s],
                             facecolor=self.colours[s])

        # Obtain handles of lines to be able to connect them to labels
        self.handles, self.labels = self.ax.get_legend_handles_labels()

        # Save axes of subplot that are in the first row for future use
        if position + 1 in [i + 1 for i in range(n_cols)]:
            self.first_row_axes.append(self.ax)

        # Save axes of subplot that are in the first column for future use
        if position + 1 in [(i * n_cols) + 1 for i in range(n_rows)]:
            self.first_column_axes.append(self.ax)

        # Remove ticklabels for all but the bottom subplots
        if position + 1 not in [(n_rows * n_cols) - i for i in range(n_cols)]:
            self.ax.set_xticklabels([])
        return

    def add_legend(self, labels):
        """
        Solution taken from here: https://stackoverflow.com/questions/\
        25812255/row-and-column-headers-in-matplotlibs-subplots
        """
        self.ax.legend(self.handles, labels,
                       bbox_to_anchor=(2.7, 0.5),
                       loc='center right',
                       borderaxespad=0., prop={'size': 20})
        return

    def add_titles(self, row_titles, column_titles):
        for ax, col in zip(self.first_row_axes, column_titles):
            ax.set_title(col, fontsize=self.title_font_sz)

        for ax, row in zip(self.first_column_axes, row_titles):
            ax.set_ylabel(row, rotation=45, fontsize=self.title_font_sz,
                          verticalalignment='center',
                          horizontalalignment='center')
            ax.get_yaxis().set_label_coords(-0.4, 0.5)
        return

    def add_grid_limits_ticks(self, xaxis_limits=(), yaxis_limits=(),
                              ymajor_spacing=None, xmajor_spacing=None,
                              yminor_spacing=None, xminor_spacing=None):
        # Set x-axis limit
        if xaxis_limits != ():
            plt.xlim(xaxis_limits)

            # Set x-axis limit
        if yaxis_limits != ():
            plt.ylim(yaxis_limits)

        if ymajor_spacing is not None:
            self.ax.yaxis.set_major_locator(
                ticker.MultipleLocator(ymajor_spacing))

        if xmajor_spacing is not None:
            self.ax.xaxis.set_major_locator(
                ticker.MultipleLocator(xmajor_spacing))

        if yminor_spacing is not None:
            self.ax.yaxis.set_minor_locator(
                ticker.MultipleLocator(yminor_spacing))

        if xminor_spacing is not None:
            self.ax.xaxis.set_minor_locator(
                ticker.MultipleLocator(xminor_spacing))

        # Set grid
        # self.ax.grid(which='both')
        # self.ax.grid(which='minor', alpha=0.2)
        self.ax.grid(which='major', alpha=0.5)
        return

    def save_figure(self, name, formats=['png']):
        # self.fig.tight_layout()
        # plt.show()
        for f in formats:
            plt.savefig(f'{name}.{f}', bbox_inches='tight', format=f, dpi=100)
        # plt.close()
        return


class LogPlot:
    def __init__(self, font_name='', font_dirs='', x_label='', y_label=''):

        self.fig = plt.figure(figsize=(3.3, 3.3))
        self.ax = self.fig.add_subplot(111)

        # Change font properties or add custom fonts
        if font_name != '':
            '''
            Solution found at: https://stackoverflow.com/questions/35668219/\
            how-to-set-up-a-custom-font-with-custom-path-to-matplotlib-global-font
            '''
            self.font = font_name
            font_files = fm.findSystemFonts(fontpaths=font_dirs)
            font_list = fm.createFontList(font_files)
            fm.fontManager.ttflist.extend(font_list)
            plt.rcParams['font.family'] = self.font
        self.title_font_sz = 8
        self.ticks_font_size = 7
        plt.rcParams.update({'font.size': self.ticks_font_size})

        # Define axes labels
        self.ax.set_xlabel(x_label, labelpad=5, fontsize=self.title_font_sz)
        self.ax.set_ylabel(y_label, labelpad=5, fontsize=self.title_font_sz)

        # Define markers and colours
        self.markers = ['8', '>', 'D', '^', 'H', '*', 'd', 'h',
                        'v', 's', '<', 'o', 'p']

        colormap = plt.cm.get_cmap('brg')
        self.colours = [colormap(i) for i in
                        np.linspace(0, 0.9, len(self.ax.collections))]
        return

    def plot_data(self, dataframe, labels_col):
        df = dataframe
        '''
        for x, y, lab, mar in zip(df.iloc[:, 1], df.iloc[:, 3],
                                  df.loc[:, labels_col], self.markers):
            self.ax.scatter(x, y, label=lab, marker=mar, s=50, alpha=1)
        '''
        for x, y, lab, xerr, yerr, mar in zip(df.iloc[:, 1], df.iloc[:, 3],
                                              df.loc[:, labels_col], df.iloc[:, 2],
                                              df.iloc[:, 4], self.markers):
            (_, caps, _) = self.ax.errorbar(x, y, xerr=xerr, yerr=yerr, label=lab,
                                            marker=mar, markersize='6',
                                            capsize=0, capthick=0,
                                            elinewidth=1, alpha=0.5,
                                            linestyle="None")
            for cap in caps:
                cap.set_markeredgewidth(0)

        return

    def add_grid_limits(self, x_limits, y_limits,
                        ymajor_spacing=None, xmajor_spacing=None,
                        yminor_spacing=None, xminor_spacing=None):

        plt.plot(x_limits, y_limits, '--', color='black', linewidth=1, alpha=0.3)
        plt.plot(x_limits, [0, 0], ':', color='black', linewidth=1, alpha=0.3)
        plt.plot([0, 0], y_limits, ':', color='black', linewidth=1, alpha=0.3)

        # Set x-axis limit
        if x_limits != ():
            plt.xlim(x_limits)

            # Set x-axis limit
        if y_limits != ():
            plt.ylim(y_limits)

        if ymajor_spacing is not None:
            self.ax.yaxis.set_major_locator(
                ticker.MultipleLocator(ymajor_spacing))

        if xmajor_spacing is not None:
            self.ax.xaxis.set_major_locator(
                ticker.MultipleLocator(xmajor_spacing))

        if yminor_spacing is not None:
            self.ax.yaxis.set_minor_locator(
                ticker.MultipleLocator(yminor_spacing))

        if xminor_spacing is not None:
            self.ax.xaxis.set_minor_locator(
                ticker.MultipleLocator(xminor_spacing))
        return

    def add_legend(self):
        handles, labels = self.ax.get_legend_handles_labels()
        handles = [h[0] for h in handles]
        self.ax.legend(handles, labels,
                       fontsize=self.title_font_sz, scatterpoints=1,
                       bbox_to_anchor=(0.5, 1.25),
                       loc='center', borderaxespad=0.,
                       ncol=2, frameon=False, numpoints=1)
        '''
        self.ax.legend(fontsize=self.title_font_sz, scatterpoints=1,
                       bbox_to_anchor=(0.5, 1.35),
                       loc='center', borderaxespad=0.,
                       ncol=2, frameon=False)
        '''
    def save_figure(self, name, formats=['png']):
        # self.fig.tight_layout()
        for f in formats:
            plt.savefig(f'{name}.{f}', bbox_inches='tight', format=f, dpi=100)
        # plt.show()
        # plt.close()
        return
