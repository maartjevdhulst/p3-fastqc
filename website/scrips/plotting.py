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
import matplotlib as mpl
import table
from Tools.demo.spreadsheet import center
from pandas.plotting import table
from dask.dataframe.methods import values
import matplotlib.colors as colors


def read_data(file):
    """
    read fastqc data file
    :param file:
    :return:
    """
    with open(file) as openfile:
        counter = 0

        base_quality_list = []
        meanplot_list = []
        header_list = []
        tile_list = []
        entry = {}
        line_x_list = []
        line_y_list = []
        base_list = []
        G_list = []
        A_list = []
        T_list = []
        C_list = []
        mean_perc_gc_list = []
        count_list = []
        n_count_list = []
        length_list = []
        length_count_list = []
        duplication_list = []
        duplication_perc_list = []
        last_num = 0
        overrepresented = {}
        base2_list = []
        illumina_universal_list = []
        illumina_small_3_list = []
        illumina_small_5_list = []
        nextera_transposase_list = []
        PolyA_list = []
        PolyG_list = []
        kmer = {}
        for line in openfile:
            
            if not line.startswith(">>"): #modules start and end with line starting with >>
                if counter == 1: #content inside first module
                    entry = make_basic_statistics(line, header_list, entry)

                elif counter == 3 and not line.startswith("#"): #content inside second module, ignoring header
                    make_base_sequence_quality_data(line, base_quality_list, meanplot_list)

                elif counter == 5 and not line.startswith("#"):
                    tile_list.append(make_per_tile(line))

                elif counter == 7 and not line.startswith("#"):
                    x, y = make_sequence_quality(line)
                    line_x_list.append(x)
                    line_y_list.append(y)

                elif counter == 9 and not line.startswith("#"):
                    base, G, A, T, C = make_base_sequence(line)
                    base_list.append(base)
                    G_list.append(G)
                    A_list.append(A)
                    T_list.append(T)
                    C_list.append(C)

                elif counter == 11 and not line.startswith("#"):
                    mean_perc_gc, count = make_gc_content(line)
                    mean_perc_gc_list.append(mean_perc_gc)
                    count_list.append(count)

                elif counter == 13 and not line.startswith("#"):
                    n_count = make_n_count(line)
                    n_count_list.append(n_count)

                elif counter == 15 and not line.startswith("#"):
                    length, length_count = make_sequence_length(line)
                    length_list.append(length)
                    length_count_list.append(length_count)

                elif counter == 17 and not line.startswith("#"):
                    duplication, perc, last_num =  make_sequence_duplication(line, last_num)
                    duplication_list.append(duplication)
                    duplication_perc_list.append(perc)

                elif counter == 19:
                    overrepresented = make_overrepresented(line, header_list, overrepresented)

                elif counter == 21 and not line.startswith("#"):
                    base, illumina_universal, illumina_small_3, illumina_small_5, nextera_transposase, PolyA, PolyG = make_adapter(line)
                    base2_list.append(base)
                    illumina_universal_list.append(illumina_universal)
                    illumina_small_3_list.append(illumina_small_3)
                    illumina_small_5_list.append(illumina_small_5)
                    nextera_transposase_list.append(nextera_transposase)
                    PolyA_list.append(PolyA)
                    PolyG_list.append(PolyG)

                elif counter == 23:
                   kmer = make_kmer(line, header_list, kmer)
            else:
                counter += 1

    # df_table = pd.DataFrame(entry)
    # print(df_table)
    # make_table(df_table)
    # make_boxplot(base_quality_list, meanplot_list)
    # tile_df = pd.DataFrame(tile_list)
    # make_heatplot(tile_df)
    # make_lineplot(line_x_list, 'sequence_quality',line_y_list)
    # make_lineplot(base_list, 'base_sequence', G_list, A_list, T_list, C_list )
    # make_lineplot(mean_perc_gc_list, 'mean_percentage_gc', count_list)
    # make_lineplot(base_list, 'n_content',n_count_list)
    # make_lineplot(length_list, 'lenght_distribution', length_count_list)
    # make_lineplot(duplication_list, 'duplication_percentage', duplication_perc_list)
    # make_lineplot(base2_list, 'adapter', illumina_universal_list, illumina_small_3_list, illumina_small_5_list,
    #               nextera_transposase_list, PolyA_list, PolyG_list)
    # print(len(base2_list))
    df_kmer = pd.DataFrame(kmer)
    make_table(df_kmer)

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
        for i, num in enumerate(line): #looping through list with the elements from the line
            key = header_list[i]
            if key not in entry.keys(): #checking if already in dictionary
                entry[key] = [num] #adding new key:value pair
            else:
                entry[key].append(num) #extending already existing key:value pair

    return entry

def make_base_sequence_quality_data(line, base_quality_list, meanplot_list):
    """

    :param meanplot_list:
    :param base_quality_list:
    :param line:
    :return:
    """
    i= 0
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
            base_quality_list.append({'label':label, 'mean':mean, 'med':median, 'q1':q1, 'q3':q3, 'whislo':whislo, 'whishi':whishi})
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
    Extracts phred scores and their corresponding count from line and returns those seperately

    :param line: one line from uploaded file
    :return: x variable holding 1 float number, y variable holding 1 float number
    """
    line = line.rstrip().split("\t")
    for i, num in enumerate(line):
        num = float(num)
        if i == 0:
            x = num
        elif i == 1:
            y = num

    return x, y

def make_base_sequence(line):
    """

    :param line:G	A	T	C
    :return:
    """
    line = line.rstrip().split("\t")
    for i, num in enumerate(line):
        if i == 0:
            if num.find("-"):
                num = num.split("-")[0]
                base = float(num)
            else:
                base = float(num)
        elif i == 1:
            G = float(num)
        elif i == 2:
            A = float(num)
        elif i == 3:
            T = float(num)
        elif i == 4:
            C = float(num)

    return base, G, A, T, C

def make_gc_content(line):
    """

    :param line:
    :return:
    """
    line = line.rstrip().split("\t")
    for i, num in enumerate(line):
        if i == 0:
            mean_perc_gc = float(num)
        elif i == 1:
            count = float(num)

    
    return  mean_perc_gc, count

def make_n_count(line):
    """

    :param line:
    :return:
    """
    line = line.rstrip().split("\t")
    for i, num in enumerate(line):
        if i == 0:
            continue
        elif i == 1:
            n_count = float(num)

    return n_count

def make_sequence_length(line):
    """

    :param line:
    :return:
    """
    line = line.rstrip().split("\t")
    for i, num in enumerate(line):
        if i == 0:
            if num.find("-"):
                num = num.split("-")[0]
                length = float(num)
            else:
                length = float(num)
        elif i == 1:
            count = float(num)

    return length, count

def make_sequence_duplication(line, last_num):
    """

    :param line:
    :return:
    """

    line = line.rstrip().split("\t")

    for i, num in enumerate(line):
        if i == 0:
            if num.startswith(">"):
                duplication = last_num + 1
            else:
                duplication = float(num)
        elif i == 1:
            perc = float(num)
            last_num = duplication

    return duplication, perc, last_num

def make_overrepresented(line, header_list, entry):
    """

    :type entry: object
    :param header_list:
    :param line:
    :return:
    """

    if line.startswith("#"): #saving header seperate
        line = line.lstrip("#").rstrip("\n").split("\t")
        header_list.extend(line)
    else:
        line = line.rstrip().split("\t")
        for i, num in enumerate(line): #looping through list with the elements from the line
            key = header_list[i]
            if key not in entry.keys(): #checking if already in dictionary
                entry[key] = [num] #adding new key:value pair
            else:
                entry[key].append(num) #extending already existing key:value pair

    return entry

def make_adapter (line):
    """

    :param line:
    :return:
    """
    line = line.rstrip().split("\t")
    for i, num in enumerate(line):
        if i == 0:
            if num.find("-"):
                num = num.split("-")[0]
                base = float(num)
            else:
                base = float(num)
        elif i == 1:
            illumina_universal = float(num)
        elif i == 2:
            illumina_small_3 = float(num)
        elif i == 3:
            illumina_small_5 = float(num)
        elif i == 4:
            nextera_transposase = float(num)
        elif i == 5:
            PolyA = float(num)
        elif i == 6:
            PolyG = float(num)

    return base, illumina_universal, illumina_small_3, illumina_small_5, nextera_transposase, PolyA, PolyG

def make_kmer (line, header_list, entry):
    """

    :param entry:
    :param header_list:
    :param line:
    :return:
    """
    if line.startswith("#"):  # saving header seperate
        line = line.lstrip("#").rstrip("\n").split("\t")
        header_list.extend(line)
    else:
        line = line.rstrip().split("\t")
        for i, num in enumerate(line):  # looping through list with the elements from the line
            key = header_list[i]
            if key not in entry.keys():  # checking if already in dictionary
                entry[key] = [num]  # adding new key:value pair
            else:
                entry[key].append(num)  # extending already existing key:value pair

    return entry



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
    fig.set_figheight(22, forward=True)


    # table = ax.table(cellText=data, cellLoc='left', loc=center
    table = pd.plotting.table(ax, data, loc='center')
    table.auto_set_column_width(col=list(range(len(data.columns))))



    # ax.set_ylim(0, len(data.index))
    # plt.show()
    plt.savefig("../static/images/table_overrepresented.png")
    plt.close()

def make_heatplot(df_tile):
    """

    :param df_tile:
    :param data:
    :return:
    """



    # Pivot the dataframe
    df_pivot = df_tile.pivot(index='y', columns='x', values='z')



    fig, ax = plt.subplots()
    #
    h = ax.matshow(df_pivot, cmap=mpl.colormaps['jet'], origin='lower')
    plt.colorbar(h, ax=ax)
    # ax.set_ylim(top=df_tile['y'].max(), bottom=df_tile['y'].min())
    # ax.set_xlim(right=df_tile['x'].max(), left=df_tile['x'].min())
    fig.tight_layout()
    # plt.show()
    plt.savefig("../static/images/heatmap1.png")
    plt.close()

def make_lineplot(x_list, plot_name=str, *y_list):
    """

    :param plot_name:
    :param x_list:
    :param data:
    :return:
    """
    fig, ax = plt.subplots()
    ax.set_prop_cycle(color=['purple', 'blue', 'green', 'yellow', 'teal', 'pink'],
                      )

    for y in y_list:
        ax.plot(x_list, y)


    plt.savefig(f"../static/images/lineplot_{plot_name}.png")
    plt.close()

    return 0

def main(args):
    """
    main function excuting the script
    :param args: file uploaded by user
    :return: 0
    """
    # file = args[1]
    file = "../static/fastqc_data_lang.txt"
    file2 = "../static/fastqc_data.txt"
    read_data(file) #opening file and sending the right parts of the file to the needed functions




if __name__ == "__main__":
    exitcode = main(sys.argv)
    sys.exit(exitcode)








