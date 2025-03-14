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

        entry = {}
        for line in openfile:
            if not line.startswith(">>"): #modules start and end with line starting with >>
                if counter == 1: #content inside first module
                    entry = make_basic_statistics(line, header_list, entry)

                elif counter == 3 and not line.startswith("#"): #content inside second module, ignoring header
                    make_base_sequence_quality_data(line, base_quality_list, meanplot_list)

                elif counter == 5 and not line.startswith("#"):
                    #
                #     make_per_tile(line)
                    pass
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

    df = pd.DataFrame(entry)
    make_table(df)
    make_boxplot(base_quality_list, meanplot_list)


    return 0

def make_basic_statistics(line, header_list, entry):
    """

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
        num = float(num)
        if linecounter == 0: #putting each float in its corresponding variable
            label = num
            linecounter += 1
        elif linecounter == 1:
            mean = num
            linecounter += 1
        elif linecounter == 2:
            median = num
            linecounter += 1
        elif linecounter == 3:
            q1 = num
            linecounter += 1
        elif linecounter == 4:
            q3 = num
            linecounter += 1
        elif linecounter == 5:
            whislo = num
            linecounter += 1
        elif linecounter == 6:
            whishi = num
            # adding dict with the base quality statistics to list
            base_quality_list.append({'label':label, 'mean':mean, 'med':median, 'q1':q1, 'q3':q3, 'whislo':whislo, 'whishi':whishi})
            linecounter = 0
            meanplot_list.append(mean) #adding mean to separate list for separate line plot

    return base_quality_list, meanplot_list

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
    plt.show()

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

    plt.show()



def main(args):
    """
    main function excuting the script
    :param args: file uploaded by user
    :return: 0
    """
    # file = args[1]
    file = "../static/fastqc_data.txt"
    read_data(file) #opening file and sending the right parts of the file to the needed functions


    return 0



if __name__ == "__main__":
    exitcode = main(sys.argv)
    sys.exit(exitcode)








