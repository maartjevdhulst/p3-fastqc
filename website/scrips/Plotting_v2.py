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



class MakePlots(object):
    def __init__(self, **kwargs):
        pass
#     different types of plots possibly in child classes

class MakeTables():
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

