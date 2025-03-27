#!/usr/bin/env python3
"""
main script plotting all plots for fastqc report
use: python .\website\scrips\plotting.py .\website\static\fastqc_data.txt
"""

__author__ = "Maartje van der Hulst"
__date__ = 2025.3
__version__ = 2.0

import sys
import pandas as pd
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from IPython.core.pylabtools import figsize

from website.scrips.plotting_v1 import make_base_sequence_quality_data


# user uploads file and settings (dict?!) app.py -> main.py
# change limits.txt with settings and save (limits class?)
# take uploaded file and execute fastqc from terminal
# unzip output (terminal)
# use data.txt for rest of this (or html inbedded for easy version)
# loop through data (file handling class?) and use different part for their corresponding plotting method
#       -> check via module titles which data is following
#       -> collect data until module ends
#       -> send collected data to correct plotting method (plotting class)
#           -> make plot, format plot, add labels, legend, background etc
#           -> save plots as png's, tables as html-strings
#       -> reset collected data for next module
# finish main.py -> app.py
# enbed results in fastqc results html via app.py



class MakePlots:
    def __init__(self, rows_list):
        self.rows_list = rows_list
        self.meanplot_list = []
        self.boxplot_data_list = []
#     different types of plots possibly in child classes

    def make_base_sequence_quality_data(self):
        """

        :param meanplot_list:
        :param base_quality_list:
        :param line:
        :return:
        """

        for line in self.rows_list:
            if not line.startswith(">>") and not line.startswith("#"): #skipping module title and column names
                line = line.rstrip().split("\t")
                for i, num in enumerate(line): #looping through list of strings

                    if i == 0: #putting each float in its corresponding variable
                        if num.find("-"):
                            num = num.split("-")[0]
                            # num = str(num)
                            label = num
                        else:
                            # num = str(num)
                            label = num
                    elif i == 1:
                        num = float(num)
                        mean = num
                    elif i == 2:
                        num = float(num)
                        median = num

                    elif i == 3:
                        num = float(num)
                        q1 = num

                    elif i == 4:
                        num = float(num)
                        q3 = num

                    elif i == 5:
                        num = float(num)
                        whislo = num

                    elif i == 6:
                        num = float(num)
                        whishi = num
                        # adding dict with the base quality statistics to list
                        self.boxplot_data_list.append({'label':label, 'mean':mean, 'med':median, 'q1':q1, 'q3':q3, 'whislo':whislo,
                                                  'whishi':whishi})
                        self.meanplot_list.append(mean) #adding mean to separate list for separate line plot

        return self.boxplot_data_list, self.meanplot_list

    def make_boxplot(self, plotname=str):
        """

        :param boxplot_data_list:
        :param meanplot_list:
        :return:
        """
        self.make_base_sequence_quality_data() # calling previous function to have the data in a usable format and datatype
        fig, ax = plt.subplots(layout='constrained') #making the figure and axis with as little whitespace surrounding as possible

        label_list = []
        for box_data_dict in self.boxplot_data_list:
            label = box_data_dict['label']
            label_list.append(label)
        #only drawing the boxplots using the already calculated statistics from data file
        boxplot = ax.bxp(bxpstats=self.boxplot_data_list, zorder=3, widths=0.8, label=label_list, capwidths=0.8, showfliers=False, manage_ticks=False, patch_artist=True)
        # making line plot also start at 1 instead of 0
        xticks = np.arange(1, len(self.meanplot_list) + 1).tolist()
        # creating line plot of mean overlapping the boxplots
        ax.plot(xticks, self.meanplot_list, zorder=3, color='xkcd:true blue', linewidth=1)

        #styling
        #coloring the boxplots
        for patch in boxplot['boxes']:
            patch.set_facecolor('yellow')
        for patch in boxplot['medians']:
            patch.set_color('red')
        #getting the highest number for the y-axis from the 90th percentile numbers
        numlist = []
        for box_data_dict in self.boxplot_data_list:
            num = box_data_dict['whishi']
            num = float(num) #str -> float
            numlist.append(num)
        ymax = max(numlist)
       #setting lengths of x-axis and y-axis
        plt.xlim(left=0.5, right=len(self.meanplot_list)+1)
        plt.ylim(bottom=1, top=ymax+1)
        #coloring background vertically in darker and lighter strips per boxplot
        for i in range(1, max(xticks)+1):
            if i % 2 == 0:
                plt.axvspan(i-0.5, i + 0.5, facecolor='white', alpha=0.3, zorder=2)
        #coloring background horizontally
        plt.axhspan(1, 20, facecolor='xkcd:salmon pink', alpha=0.5)
        plt.axhspan(20, 28, facecolor='xkcd:light yellow', alpha=0.5)
        plt.axhspan(28, 40, facecolor='xkcd:soft green', alpha=0.5)


        #saving with custom name in png format
        plt.savefig(f"static/images/boxplot_{plotname}.png")
        plt.close()
        # plt.show()
        return "boxplot made"

    def make_per_tile(self):
        """

        :param line:
        :return:
        """
        tile_list = []
        for line in self.rows_list:
            if not line.startswith(">>") and not line.startswith("#"):  # skipping module title and column names
                line = line.rstrip().split("\t")
                for i, num in enumerate(line):
                    if i == 0:
                        num = int(num)
                        y = num
                    elif i == 1:
                        if num.find("-"):
                            num = num.split("-")[0]
                            num = int(num)
                            x = num
                        else:
                            num = int(num)
                            x = num
                    elif i == 2:
                        num = float(num)
                        z = num
                tile_list.append({'x':x, 'y':y, 'z':z})

        return tile_list

    def make_heatplot(self, plotname):
        """

        :param df_tile:
        :param data:
        :return:
        """
        tile_list = self.make_per_tile()
        # Pivot the dataframe
        df_tile = pd.DataFrame(tile_list)
        df_pivot = df_tile.pivot(index='y', columns='x', values='z')

        fig, ax = plt.subplots(layout='constrained')
        fig.set_size_inches(8, 6, forward=True)

        cmap = colors.LinearSegmentedColormap.from_list('custom blue',
                                                        ['#F9000D', '#00bbb8', '#000BC9', '#00bbb8', '#F9000D'])


        if df_pivot.index.size < 1/4 * df_pivot.columns.size :
            ratio = df_pivot.columns.size/2
            heatmap = ax.matshow(df_pivot, cmap=cmap, origin='lower', norm=colors.CenteredNorm(), aspect=ratio)
            plt.colorbar(heatmap, ax=ax)
        else:
            heatmap = ax.matshow(df_pivot, cmap=cmap, origin='lower', norm=colors.CenteredNorm())
            plt.colorbar(heatmap, ax=ax)

        # plt.show()
        plt.savefig(f"static/images/heatmap{plotname}.png")
        plt.close()

    def make_sequence_quality(self):
        """
        Extracts phred scores and their corresponding count from line and returns those seperately

        :param line: one line from uploaded file
        :return: x variable holding 1 float number, y variable holding 1 float number
        """
        x_list = []
        y_list = []
        for line in self.rows_list:
            if not line.startswith(">>") and not line.startswith("#"):  # skipping module title and column names
                line = line.rstrip().split("\t")
                for i, num in enumerate(line):
                    if i == 0:
                        num = int(num)
                        x_list.append(num)
                    elif i == 1:
                        num = float(num)
                        y_list.append(num)

        return x_list, y_list

    def make_lineplot(self, plot_name=str):
        """

        :param plot_name:
        :param x_list:
        :param data:
        :return:
        """
        x_list, y_lists = self.make_sequence_quality()

        fig, ax = plt.subplots(layout='constrained')
        ax.set_prop_cycle(color=['purple', 'blue', 'green', 'yellow', 'teal', 'pink'])

        line_plot = ax.plot(x_list, y_lists, label="Average quality per read")

        for i in range(min(x_list), max(x_list)+1):
            if i % 2 == 0:
                plt.axvspan(i-0.5, i + 0.5, facecolor='xkcd:lilac', alpha=0.3)
        #coloring background horizontally
        # plt.axhspan(1, 20, facecolor='xkcd:lilac', alpha=0.1)
        ax.legend(handles=line_plot, loc='upper right')
        # plt.savefig(f"../static/images/lineplot_{plot_name}.png")
        # plt.close()
        plt.show()
        return 0



class MakeTables:
    def __init__(self, rows_list):
        self.rows_list = rows_list
        self.df = self.make_dataframe()
        self.html_string = self.make_html_table(self.df)

    def make_dataframe(self):
        keys = self.rows_list[1]
        values = self.rows_list[2:]
        new_values = []
        keys = keys.strip("#\n").split("\t") #list of strings
        for value in values:
            value = value.strip().split("\t")
            new_values.append(value)
        rows_dict = {}
        for num, key in enumerate(keys):
            rows_dict[key] = []
            for value in new_values:
                rows_dict[key].append(value[num])
        df_rows = pd.DataFrame(rows_dict)
        return df_rows

    def make_html_table(self,data):

        html_string = data.to_html(index=False, justify='center')

        return f'{html_string}'

