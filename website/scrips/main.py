#!/usr/bin/env python3
"""
should user be able to upload cwd to fastqc?!
cwd="C:/Users/maart/School/Practicum/fastqc_v0.12.1/FastQC/"
"""

__author__ = "Maartje van der Hulst"
__date__ = 2025.3
__version__ = 1.0

import sys
import subprocess
from subprocess import Popen
from Plotting_v2 import MakeTables, MakePlots

class FastQC:
    def __init__(self, file):
        self.file = file
        self.run_fastqc()
        self.unzip_results()

    def run_fastqc(self):

        p1 = Popen(["run_fastqc.bat", self.file],
                   cwd="C:/Users/maart/School/Practicum/fastqc_v0.12.1/FastQC/", shell=True)
        stdout, stderr = p1.communicate()

    def unzip_results(self):
        subprocess.run("tar -xf ../static/test_fastqc.zip -C ../static/", shell=True)


class ReadingDataTextFile:
    def __init__(self, file):
        self.file = file
        self.table, self.icons = self.reading_datafile()


    def reading_datafile(self):
        current_module = []
        icon_list = []
        with open(self.file, "r", encoding='UTF-8') as open_file:
            for line in open_file:
                if line.startswith(">>END_MODULE"):
                    module = current_module[0]
                    if module[-5:-1] == 'pass':
                        icon_list.append('pass;tick')
                    elif module[-5:-1] == 'warn':
                        icon_list.append('warning')
                    elif module[-5:-1] == 'fail':
                        icon_list.append('error')
                    if module.startswith(">>Basic Statistics"):
                        html_string = MakeTables(current_module)
                        # print(html_string.html_string)
                    #     plotting class die module(->soort plot) en inhoud(current_module) meekrijgt
                    elif module.startswith('>>Per base sequence quality'):
                        boxplot = MakePlots(current_module)
                        boxplot.make_boxplot('Per base sequence quality')
                        break
                    current_module = []

                elif line.startswith(">>") and not line.startswith(">>END_MODULE"):
                    current_module += [line]
                elif line.startswith("##"):
                    continue
                elif not line.startswith(">>"):
                    current_module.append(line)

        return html_string.html_string, icon_list


def main():
    # subprocess.run("cd ../fastqc_v0.12.1/FastQC/ | /run_fastqc.bat ../../Practicum_3/Example_Data/test.fastq", shell=True)
    # run_fastqc("../../p3-fastqc/website/static/test.fastq")
    # unzip_results()
    ReadingDataTextFile("../static/test_fastqc/fastqc_data.txt")


if __name__ == "__main__":
    EXITCODE = main()
    sys.exit(EXITCODE)
