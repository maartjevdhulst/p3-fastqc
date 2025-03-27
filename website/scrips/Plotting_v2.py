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
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import dataframe_image as dfi

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
        self.make_base_sequence_quality_data()
        fig, ax = plt.subplots() #making the figure and axis
        # plt.style.use('dark_background')
        #only drawing the boxplots using the already calculated statistics from data file
        boxplot = ax.bxp(bxpstats=self.boxplot_data_list, showfliers=False,  manage_ticks=False, patch_artist=True)
        for patch in boxplot['boxes']:
            patch.set_facecolor('yellow')
        for patch in boxplot['medians']:
            patch.set_color('red')
        xticks = np.arange(1, len(self.meanplot_list) + 1).tolist() #making line plot also start at 1 instead of 0

        ax.plot(xticks, self.meanplot_list) #creating line plot of mean overlapping the boxplots
        #  mooimaken en zorgen dat het plaatje naar een bruikbare plek gaat
        plt.savefig(f"../static/images/boxplot_{plotname}.png")
        plt.close()

        return "boxplot made"




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

