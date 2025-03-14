#!/usr/bin/env python3
"""
main script plotting all plots for fastqc report
use: python .\website\scrips\edit_limits.py .\website\static\fastqc_data.txt
"""

__author__ = "Maartje van der Hulst"
__date__ = 2025.3
__version__ = 1.0


import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd
from dask.dataframe.methods import values
from matplotlib.colors import Normalize


def read_data(file):
    """
    read fastqc data file
    :param file:
    :return:
    """
    with open(file) as openfile:
        counter = 0
        linecounter = 0
        base_quality_list = []
        meanplot_list = []
        header_list = []
        tile_list = []
        entry = {}
        for line in openfile:
            if not line.startswith(">>"): #modules start and end with line starting with >>
                if counter == 1: #content inside first module
                    entry = make_basic_statistics(line, header_list, entry)

                elif counter == 3 and not line.startswith("#"): #content inside second module, ignoring header
                    make_base_sequence_quality_data(line, base_quality_list, meanplot_list)

                elif counter == 5 and not line.startswith("#"):
                    tile_list.append(make_per_tile(line))

                elif counter == 7 and not line.startswith("#"):
                #         make_sequence_quality
                    pass
                elif counter == 9 and not line.startswith("#"):
                # make_base_sequence
                    pass
                elif counter == 11 and not line.startswith("#"):
                # make_gc_content(line)
                    pass
                elif counter == 13 and not line.startswith("#"):
                # make_per_base_n(line)
                    pass
                elif counter == 15 and not line.startswith("#"):
                # make_sequence_length(line)
                    pass
                elif counter == 17 and not line.startswith("#"):
                # make_sequence_duplication(line)
                    pass
                elif counter == 19 and not line.startswith("#"):
                # make_overrepresented(line)
                    pass
                elif counter == 21 and not line.startswith("#"):
            #     make_adapter(line)
                    pass
            else:
                counter += 1

    # df_table = pd.DataFrame(entry)
    # make_table(df_table)
    # make_boxplot(base_quality_list, meanplot_list)
    tile_df = pd.DataFrame(tile_list)
    make_heatplot(tile_df)

    return 0

def make_basic_statistics(line, header_list, entry):
    """

    :param entry:
    :param line:
    :param header_list:
    :return: dictionary with basic statistics
    """


    if line.startswith("#"): #saving header seperate
        line = line.lstrip("#").rstrip("\n").split("\t")
        header_list.extend(line)
    else:
        line = line.rstrip().split("\t")
        for i in range(len(line)): #looping through list with the elements from the line
            key = str(header_list[i])
            if key not in entry.keys(): #checking if already in dictionary
                entry[key] = [line[i]] #adding new key:value pair
            else:
                entry[key].append(line[i]) #extending already existing key:value pair

    return entry

def make_base_sequence_quality_data(line, base_quality_list, meanplot_list):
    """

    :param meanplot_list:
    :param base_quality_list:
    :param line:
    :return:
    """
    linecounter = 0
    line = line.rstrip().split("\t")

    for num in line: #looping through list of strings

        if linecounter == 0: #putting each float in its corresponding variable
            label = num
            linecounter += 1
        elif linecounter == 1:
            num = float(num)
            mean = num
            linecounter += 1
        elif linecounter == 2:
            num = float(num)
            median = num
            linecounter += 1
        elif linecounter == 3:
            num = float(num)
            q1 = num
            linecounter += 1
        elif linecounter == 4:
            num = float(num)
            q3 = num
            linecounter += 1
        elif linecounter == 5:
            num = float(num)
            whislo = num
            linecounter += 1
        elif linecounter == 6:
            num = float(num)
            whishi = num
            # adding dict with the base quality statistics to list
            base_quality_list.append({'label':label, 'mean':mean, 'med':median, 'q1':q1, 'q3':q3, 'whislo':whislo, 'whishi':whishi})
            linecounter = 0
            meanplot_list.append(mean) #adding mean to separate list for separate line plot

    return base_quality_list, meanplot_list

def make_per_tile(line):
    """

    :param line:
    :return:
    """
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


    return {'x':x, 'y':y, 'z':z}

def make_sequence_quality(line):
    """

    :param line:
    :return:
    """
    pass

    return 0

def make_base_sequence(line):
    """

    :param line:
    :return:
    """
    pass

    return 0

def make_gc_content(line):
    """

    :param line:
    :return:
    """
    pass
    return 0

def make_per_base_n(line):
    """

    :param line:
    :return:
    """
    pass

    return 0

def make_sequence_length(line):
    """

    :param line:
    :return:
    """
    pass

    return 0

def make_sequence_duplication(line):
    """

    :param line:
    :return:
    """

    pass

    return 0

def make_overrepresented(line):
    """

    :param line:
    :return:
    """
    pass

    return 0

def make_adapter (line):
    """

    :param line:
    :return:
    """

    pass

    return 0

def make_kmer (line):
    """

    :param line:
    :return:
    """
    pass

    return 0


def make_boxplot(data, meanplot):
    """

    :param data:
    :param meanplot:
    :return:
    """
    fig, ax = plt.subplots() #making the figure and axis
    #only drawing the boxplots using the already calculated statistics from data file
    ax.bxp(bxpstats=data, showfliers=False,  showmeans = True, meanline = True, manage_ticks=False )
    xticks = np.arange(1, len(meanplot) + 1).tolist() #making line plot also start at 1 instead of 0

    ax.plot(xticks, meanplot) #creating line plot of mean overlapping the boxplots
    #  mooimaken en zorgen dat het plaatje naar een bruikbare plek gaat
    plt.savefig("../static/images/boxplot.png")
    plt.close()

def make_table(data):
    """

    :param data:
    :return:
    """

    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')


    ax.table(cellText=data, loc='center')

    fig.tight_layout()

    plt.savefig("../static/images/table.png")
    plt.close()

def make_heatplot(df_tile):
    """

    :param df_tile:
    :param data:
    :return:
    """
    # Y, X= np.meshgrid(df_tile['y'], df_tile['x'])
    # Z = np.array(df_tile['z'])
    # print(df_tile.loc[0])
    # Z = Z.reshape(len(X), len(Y))

    # Z = np.transpose(Z)
    # data = Z

    # plt.style.use('_mpl-gallery-nogrid')

    # Pivot the dataframe
    df_pivot = df_tile.pivot(index='x', columns='y', values='z')
    print(df_pivot)

    # ax = sns.heatmap(df_pivot, cmap="YlGnBu")
    # ax.set_title("Heatmap of Z values")
    #
    # plt.show()
    fig, ax = plt.subplots()
    #
    ax.imshow(df_pivot, cmap= "RdYlBu", vmin= -1, vmax= 1 )
    # plt.colorbar()
    ax.set_ylim(top=df_tile['y'].max(), bottom=df_tile['y'].min())
    ax.set_xlim(right=df_tile['x'].max(), left=df_tile['x'].min())
    fig.tight_layout()
    plt.show()
    # plt.savefig("../static/images/heatmap1.png")
    # plt.close()

def make_lineplot(data):
    """

    :param data:
    :return:
    """
    pass

    return 0

def main(args):
    """
    main function excuting the script
    :param args: file uploaded by user
    :return: 0
    """
    # file = args[1]
    file = "../static/fastqc_data_lang.txt"
    read_data(file) #opening file and sending the right parts of the file to the needed functions




if __name__ == "__main__":
    exitcode = main(sys.argv)
    sys.exit(exitcode)








