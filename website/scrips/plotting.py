#!/usr/bin/env python3
"""
two plotting classes using inheritance to make all plots for the fastqc report. PrepPlotData has
a function for each module, which calls their corresponding MakePlots function for the correct plot.

This class gets imported in the main.py script of this project. To use this class in other projects
import the class like you would any other selfmade class.
"""

__author__ = "Maartje van der Hulst"
__date__ = 2025.3
__version__ = 3.2


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors



class MakePlots:
    """
    Parent class for making plots. all functions of this class are only used through direct
    calling and none are executed through initializing the MakePlots class object.
    """
    def __init__(self):
        """
        pass, making all functions only available through direct calling and none are executed by
        initializing the MakePlots class object.
        """


    def __repr__(self):
        """
        An unambiguous string representation of an object, primarily for developers and debugging.
        :return: string
        """
        return "MakePlots()"

    def make_boxplot(self, boxplot_data_list, meanplot_list, x_labels=None, plotname=str):
        """
        makes a graph with boxplots from a list of dictionaries and a overlapping lineplot from a
        list of means

        :param plotname: string with the name of the plot
        :param x_labels: optional list of labels for the x-axis
        :param meanplot_list: list of floats of the means
        :type boxplot_data_list: list of dictionaries containing the boxplot data
        :return: string
        """


        # making the figure and axis with as little whitespace surrounding as possible and
        # setting the figure size
        fig, ax = plt.subplots(layout='constrained')
        fig.set_size_inches(8, 6, forward=True)
        # extracting labels from the data list containing dictionairies
        label_list = [box_data_dict['label'] for box_data_dict in boxplot_data_list]

        #only drawing the boxplots using the already calculated statistics from data file
        boxplot = ax.bxp(bxpstats=boxplot_data_list, zorder=3, widths=0.8, label=label_list,
                         capwidths=0.8, showfliers=False, manage_ticks=False, patch_artist=True)
        # making line plot also start at 1 instead of 0
        xticks = np.arange(1, len(meanplot_list) + 1).tolist()
        # creating line plot of mean overlapping the boxplots
        ax.plot(xticks, meanplot_list, zorder=3, color='xkcd:true blue', linewidth=1)

        #styling
        #coloring the boxplots
        for patch in boxplot['boxes']:
            patch.set_facecolor('yellow')
        for patch in boxplot['medians']:
            patch.set_color('red')
        #getting the highest number for the y-axis from the 90th percentile numbers
        numlist = []
        for box_data_dict in boxplot_data_list:
            num = box_data_dict['whishi']
            num = float(num) #str -> float
            numlist.append(num)
        ymax = max(numlist)
       #setting lengths of x-axis and y-axis
        plt.xlim(left=0.5, right=len(meanplot_list)+1)
        plt.ylim(bottom=1, top=ymax+1)
        plt.xlabel("Position in read (bp)", fontsize=8)
        #coloring background vertically in darker and lighter strips per boxplot
        for i in range(1, max(xticks)+1):
            if i % 2 == 0:
                plt.axvspan(i-0.5, i + 0.5, facecolor='white', alpha=0.3, zorder=2)
        #coloring background horizontally
        plt.axhspan(1, 20, facecolor='xkcd:salmon pink', alpha=0.5)
        plt.axhspan(20, 28, facecolor='xkcd:light yellow', alpha=0.5)
        plt.axhspan(28, 45, facecolor='xkcd:soft green', alpha=0.5)

        #if there are labels for the x-ticks use them
        if x_labels:
            ax.set_xticks(x_labels[0], x_labels[1], fontsize=7)

        #saving with custom name in png format
        plt.savefig(f"static/images/boxplot_{plotname}.png")
        plt.close()
        # plt.show()
        return "boxplot made"

    def make_heatplot(self, tile_list, plotname=str):
        """
        makes a graph containing a heatmap of the tile list
        :param plotname: string with the name of the plot
        :param tile_list: list of dictionaries containing the value (z) of each tile (x, y)

        """

        # make a dataframe from the list and pivot the dataframe so each tile (x,y) has a value (z)
        df_tile = pd.DataFrame(tile_list)
        df_pivot = df_tile.pivot(index='y', columns='x', values='z')

        # making the figure and axis with as little whitespace surrounding as possible and
        # setting the figure size
        fig, ax = plt.subplots(layout='constrained')
        fig.set_size_inches(8, 6, forward=True)


        # if the tile quality is equal everywhere resize plot and normalize color around 0
        if df_pivot.index.size < 1/4 * df_pivot.columns.size :
            ratio = df_pivot.columns.size/2
            heatmap = ax.matshow(df_pivot, cmap="jet", origin='lower',
                                 norm=colors.CenteredNorm(), aspect=ratio)
        # when the tile quality varies
        else:
            heatmap = ax.matshow(df_pivot, cmap='jet_r' , origin='lower')
            fig.colorbar(heatmap, ax=ax)

        # plt.show()
        plt.savefig(f"static/images/heatmap{plotname}.png")
        plt.close()

    def make_lineplot(self, x_list, *y_lists, x_labels=None, title=None,
                      labels=None, plot_name=str):
        """
        create a graph with line plots from an x-list and y-list(s)
        :type y_lists: list of lists of floats of the x-values
        :param labels: optional list of label(s) for the line(s) for the legend
        :param title: optional title for the graph
        :param x_labels: optional list of labels for the x-axis
        :param plot_name: string with the name of the plot
        :param x_list: list of floats of the x-values

        """
        # making the figure and axis with as little whitespace surrounding as possible and
        # setting the figure size
        fig, ax = plt.subplots(layout='constrained')
        fig.set_size_inches(8,6)
        #setting line colors to cycle through
        ax.set_prop_cycle(color=['purple', 'blue', 'green', 'yellow', 'teal', 'pink'])
        #plotting each line individually
        for i, y in enumerate(y_lists):
            line_plot = ax.plot(x_list, y, label=labels[i])

        #checking whether x are integers or floats
        if isinstance(x_list[0], int):
            for i in range(min(x_list), max(x_list)+1):
                if i % 2 == 0:
                    plt.axvspan(i - 0.5, i + 0.5, facecolor='xkcd:lilac', alpha=0.3)

        # when x_labels are given to the function, use them
        if x_labels:
            ax.set_xticks(x_labels[0], x_labels[1])
        # adding legend and title
        ax.legend(loc='upper right')
        plt.title(title)
        plt.savefig(f"static/images/lineplot_{plot_name}.png")
        plt.close()
        #
        # plt.show()

    def make_html_table(self,dataframe):
        """
        turning dataframe into html table
        :param dataframe: dataframe containing the data for the html table
        :return: string containing the html table
        """
        html_string = dataframe.to_html(index=False, justify='center')
        # returning it in string format
        return f'{html_string}'



class PrepPlotData(MakePlots):
    """
    class which preps the data from the ReadingDataTextFile class from main.py to be plotted
    using the MakePlots class
    """
    def __init__(self, rows_list):
        """
        initializes global variables and executes super().__init__() to give access to the functions
        of the parent class MakePlots

        :param rows_list: list of strings containing the rows of the text file of one module
        """
        self.rows_list = rows_list
        self.df_basics = ""
        super().__init__()

    def __repr__(self):
        """
        An unambiguous string representation of an object, primarily for developers and debugging.
        :return: string
        """
        return f"PrepPlotData({self.rows_list})"

    def make_basics_dataframe(self):
        """
        Takes data from basic  statistics module turns it into a dataframe, which is passed into
        the super function to make a html table
        :return: string of html table, dataframe
        """
        # Skipping the module name, taking the columnnames as keys for the following data
        keys = self.rows_list[1]
        values = self.rows_list[2:]
        #
        keys = keys.strip("#\n").split("\t") #list of strings
        new_values = [value.strip().split("\t") for value in values] #list of lists with strings
        # equal in length to the keys list of strings

        # making dictionary using above keys and values
        rows_dict = {}
        lc = [rows_dict[key].append(value[i])
              if key in rows_dict.keys()
              else
                rows_dict.update({key:[value[i]]} )
                for i, key in enumerate(keys)
                    for value in new_values]

        # turning dict into database
        self.df_basics = pd.DataFrame(rows_dict)
        # using parent class to turn the database into string containing the html table
        html_string = super().make_html_table(self.df_basics)

        return html_string, self.df_basics

    def make_base_sequence_quality_data(self, plotname=str):
        """
        Takes data from the per base sequence quality module and turns into a list of
        dictionaries and a list of the means. This is passed to the super function to turn it
        into a boxplot
        :param plotname: string with the name of the plot
        :return: 0
        """
        boxplot_data_list = []
        meanplot_list = []
        x_ticks = []
        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t")
                for i, num in enumerate(line):  # looping through list of strings
                    if i == 0:  # putting each float in its corresponding variable
                        if num.find("-"): #checking for grouped bases
                            x_ticks.append(str(num)) #saving those so they can be used for x-tick
                            # labels
                            num = num.split("-")[0]  #only using the first number so it can be
                            # converted to int and used for plotting
                            label = num
                        else:
                            x_ticks.append(str(num))
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
                        boxplot_data_list.append(
                            {'label': label, 'mean': mean, 'med': median, 'q1': q1, 'q3': q3,
                             'whislo': whislo, 'whishi': whishi})
                        meanplot_list.append(mean)  #adding mean to separate list for line plot

        # when there are bases grouped (e.g. 14-19), use fewer x-tick labels so they don't overlap
        if x_ticks:
            xticks = np.arange(1, len(meanplot_list) + 1).tolist()
            # matching the number of ticks to the number of labels in the same interval
            base_num = [x for i, x in enumerate(x_ticks) if i > 9 and (i - 10) % 3 == 0 or i < 9]
            x_ticks = [x for x in xticks if x > 10 and x % 3 == 0 or x < 10]
            x_ticks = [x_ticks, base_num]
        else:  #turning empty list to None so x_labels stay None if x_ticks is unused
            x_ticks = None

        # using parent class to make boxplot from the processed data
        super().make_boxplot(boxplot_data_list, meanplot_list, x_labels=x_ticks,
                             plotname=plotname)
        return 0

    def make_per_tile(self, plotname=str):
        """
        Takes data from the per tile sequence quality module and turns into a list of
        dictionaries. This is passed to the super function turning that into a heatplot
        :param plotname: string with the name of the plot
        :return: 0
        """
        tile_list = []
        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t") #list of strings
                for i, num in enumerate(line):
                    if i == 0: #adding each number to the correct variable
                        num = int(num)
                        y = num
                    elif i == 1:
                        if num.find("-"):
                            num = num.split("-")[0] #using only the first int so it can be used
                            # for plotting
                            num = int(num)
                            x = num
                        else:
                            num = int(num)
                            x = num
                    elif i == 2:
                        num = float(num)
                        z = num
                tile_list.append({'x': x, 'y': y, 'z': z}) #saving each line as a dict inside a list

        # using parent class to make a heatplot from the processed data
        super().make_heatplot(tile_list, plotname)

        return 0

    def make_sequence_quality(self, plotname=str):
        """
        Takes the data from the per sequence quality scores module and adds the phred scores and
        their corresponding counts to seperate lists, which get passed to the super function to
        turn them into a lineplot.

        :param plotname: string with the name of the plot
        :return: 0
        """
        x_list = []
        y_list = []
        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t") #list of strings
                for i, num in enumerate(line): #adding each number to their corresponding list
                    if i == 0:
                        num = int(num)
                        x_list.append(num)
                    elif i == 1:
                        num = float(num)
                        y_list.append(num)

        # using parent class to plot the processed data
        super().make_lineplot(x_list, y_list, plot_name=plotname,
                              labels=["Average Quality per read"])

        return 0

    def make_base_sequence(self, plotname=str):
        """
        Takes the data from the per base sequence content module and turns those into seperate
        lists, which get passed to the super function to turn them into a lineplot.
        :param plotname: string with the name of the plot
        :return: 0
        """
        base_num = []
        G_base = []
        A_base = []
        T_base = []
        C_base = []
        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t") #list of strings
                for i, num in enumerate(line):
                    if i == 0:  #adding each number to their corresponding list
                        if num.find("-"): #checking for grouped bases
                            num = num.split("-")[0]
                            base_num.append(int(num))
                        else:
                            base_num.append(int(num))
                    elif i == 1:
                        G_base.append(float(num))
                    elif i == 2:
                        A_base.append(float(num))
                    elif i == 3:
                        T_base.append(float(num))
                    elif i == 4:
                        C_base.append(float(num))
        labels = ["%T", "%C", "%A", "%G"]
        #
        x_list = [i + 1 for i, num in enumerate(base_num)]
        x_ticks = [x for x in x_list if x>=10 and x%5 == 0 or x<10]
        base_num = [x for i, x in enumerate(base_num) if x > 10 and i % 5 == 0 or x < 10]
        # using parent class to plot the processed data
        super().make_lineplot(x_list, T_base, C_base, A_base, G_base, labels=labels,
                              x_labels=[x_ticks, base_num], plot_name=plotname)

        return 0

    def make_gc_content(self, plotname=str):
        """
        Takes the data from the per sequence GC content module and turns those into lists,
        which get passed to the super function to turn them into a lineplot.
        :param plotname: string with the name of the plot
        :return: 0
        """
        mean_gc_perc = []
        count = []

        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t") #list of strings
                for i, num in enumerate(line):
                    if i == 0:
                        mean_gc_perc.append(int(num))
                    elif i == 1:
                        count.append(float(num))

        # using parent class to plot the processed data
        super().make_lineplot(mean_gc_perc, count, plot_name=plotname,
                              labels=["GC count per read"])

        return 0

    def make_n_count(self, plotname=str):
        """
        Takes the data from the per base N content module and turns those into lists,
        which get passed to the super function to turn them into a lineplot.
        :param plotname: string with the name of the plot
        :return: 0
        """
        base = []
        n_count = []

        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t") #list of strings
                for i, num in enumerate(line):
                    if i == 0:
                        if num.find("-"):
                            num = num.split("-")[0]
                            base.append(int(num))
                        else:
                            base.append(int(num))

                    elif i == 1:
                        n_count.append(float(num))
        # using parent class to plot the processed data
        super().make_lineplot(base, n_count, plot_name=plotname, labels= ["%N"])

        return 0

    def make_sequence_length(self, plotname=str):
        """
        Takes the data from the sequence lenght distribution module and turns those into lists,
        which get passed to the super function to turn them into a line plot.
        :param plotname: string with the name of the plot
        :return: 0
        """
        length = []
        count = []

        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t") #list of strings
                for i, num in enumerate(line):
                    if i == 0:
                        if num.find("-"):
                            num = num.split("-")[0]
                            length.append(int(num))
                        else:
                            length.append(int(num))
                    elif i == 1:
                        count.append(float(num))
        #when all sequences are the same length add to the lists to be able to make a straight plot
        if len(length) < 2:
            length = [length[0] - 1, length[0], length[0] + 1]
            count = [0, count[0], 0]

        # using parent class to plot the processed data
        super().make_lineplot(length, count, plot_name=plotname, labels=["Sequence Length"])

        return 0

    def make_sequence_duplication(self, plotname=str):
        """
        Takes the data from the sequence duplication levels module and turns those into lists,
        which get passed to the super function to turn them into a line plot.
        :param plotname: string with the name of the plot
        :return: 0
        """

        duplication = []
        last_num = 0
        perc = []
        title = ""
        x_label = []

        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t")
                for i, num in enumerate(line):
                    if i == 0:
                        x_label.append(num)
                        if num.startswith(">"): #for the last large numbers eg '>5k'
                            duplication.append(last_num + 1)
                        else:
                            duplication.append(int(num))
                    elif i == 1:
                        perc.append(float(num))
                        last_num += 1 #keeping track of the numbers even for the non int/floats
            elif line.startswith("#Total Deduplicated Percentage"): #extra end result
                line = line.rstrip().split("\t")
                title = f"Percent of secs remaining if deduplicated {line[-1]}%"

        x_labels = [duplication, x_label]
        label = ["% Total sequences"]
        # using parent class to plot the processed data
        super().make_lineplot(duplication, perc, x_labels=x_labels, labels=label,
                              title=title, plot_name=plotname)

        return 0

    def make_overrepresented(self, plotname=str):
        """
        Takes the data from the overrepresented sequences module and turns those into a
        dictionary where the first row from the data is used as the keys. This is turned into a
        dataframe, which is passed to the super function to make a html table.

        :param plotname: string with the name of the plot
        :return: string of the html table
        """
        header_list = []
        entry = {}

        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t")
                for i, num in enumerate(line):
                    key = header_list[i]
                    if key not in entry.keys():  # checking if already in dictionary
                        entry[key] = [num]  # adding new key:value pair
                    else:
                        entry[key].append(num)  # extending already existing key:value pair
            elif line.startswith("#"): #saving header seperate
                line = line.lstrip("#").rstrip("\n").split("\t")
                header_list.extend(line)

        # using parent class to plot the processed data
        if len(entry) > 0:
            df_overrepresented = pd.DataFrame(entry)
            html_string = super().make_html_table(df_overrepresented)
        else: #when there are none
            html_string = "No overrepresented sequences"

        return html_string

    def make_adapter (self, plotname=str):
        """
        Takes the data from the adapter content module and turns those into lists,
        which get passed to the super function to turn them into a line plot.
        :param plotname: string with the name of the plot
        :return: 0
        """
        base_list = []
        illumina_universal_list = []
        illumina_small_3_list = []
        illumina_small_5_list = []
        nextera_transposase_list = []
        PolyA_list = []
        PolyG_list = []
        for line in self.rows_list:
            # skipping module title and column names
            if not line.startswith(">>") and not line.startswith("#"):
                line = line.rstrip().split("\t")
                for i, num in enumerate(line):
                    if i == 0:
                        if num.find("-"):
                            num = num.split("-")[0]
                            base_list.append(int(num))
                        else:
                            base_list.append(int(num))
                    elif i == 1:
                        illumina_universal_list.append(float(num))
                    elif i == 2:
                        illumina_small_3_list.append(float(num))
                    elif i == 3:
                        illumina_small_5_list.append(float(num))
                    elif i == 4:
                        nextera_transposase_list.append(float(num))
                    elif i == 5:
                        PolyA_list.append(float(num))
                    elif i == 6:
                        PolyG_list.append(float(num))

        labels = ["Illumina Universal Adapter", "Illumina Small RNA 3' Adapter",
                  "Illumina Small RNA 5' Adapter", "Nextera Transposase Sequence", "PolyA", "PolyG"]
        # using parent class to plot the processed data
        super().make_lineplot(base_list, illumina_universal_list, illumina_small_3_list,
                              illumina_small_5_list, nextera_transposase_list, PolyA_list,
                              PolyG_list, labels=labels, plot_name=plotname)

        return 0
