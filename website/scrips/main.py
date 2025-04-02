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
from .Plotting_v2 import PrepPlotData



class FastQC:
    def __init__(self, file):
        # running both functions when calling the class with the given file
        self.file = file
        self.run_fastqc()
        self.unzip_results()

    def run_fastqc(self):
        # running the bat fastqc file with the given file
        p1 = subprocess.run(["run_fastqc.bat", f"../../../uploads/{self.file}"],
                   cwd="Tools/fastqc_v0.12.1/FastQC/", shell=True)
        # stdout, stderr = p1.communicate()

    def unzip_results(self):
        # unpacking zip created by fastqc so data file is available for processing
        subprocess.run(f"tar -xf uploads/{self.file[:-6]}_fastqc.zip" , shell=True)


class ReadingDataTextFile:
    def __init__(self, file):
        """

        :param file:
        """
        self.file = file
        self.table, self.icons, self.dataframe, self.overrepresented, self.kmer = self.reading_datafile()


    def reading_datafile(self):
        """

        :return:
        """
        current_module = []
        icon_list = []
        kmer_html = None
        with open(self.file, "r", encoding='UTF-8') as open_file:
            for line in open_file: #looping through data file
                if line.startswith(">>END_MODULE"): #saving each module till end and resetting
                    # adding module status to icon list so correct icon can be used for each module
                    module = current_module[0]
                    if module[-5:-1] == 'pass':
                        icon_list.append('tick')
                    elif module[-5:-1] == 'warn':
                        icon_list.append('warning')
                    elif module[-5:-1] == 'fail':
                        icon_list.append('error')
                    # sending each module to its corresponding dataprep and plotting functions
                    if module.startswith(">>Basic Statistics"):
                        basic_string = PrepPlotData(current_module)
                        html_string = basic_string.make_basics_dataframe()
                        # plotting class die module(->soort plot) en inhoud(current_module) meekrijgt
                    elif module.startswith('>>Per base sequence quality'):
                        boxplot = PrepPlotData(current_module)
                        boxplot.make_base_sequence_quality_data('Per_base_sequence_quality')
                    elif module.startswith('>>Per tile sequence quality'):
                        heatmap = PrepPlotData(current_module)
                        heatmap.make_per_tile('Per_base_sequence_quality')
                    elif module.startswith(">>Per sequence quality scores"):
                        lineplot = PrepPlotData(current_module)
                        lineplot.make_sequence_quality("Per_sequence_quality_scores")
                    elif module.startswith(">>Per base sequence content"):
                        lineplot = PrepPlotData(current_module)
                        lineplot.make_base_sequence("Per_base_sequence_content")
                    elif module.startswith(">>Per sequence GC content"):
                        lineplot = PrepPlotData(current_module)
                        lineplot.make_gc_content("Per_sequence_GC_content")
                    elif module.startswith(">>Per base N content"):
                        lineplot = PrepPlotData(current_module)
                        lineplot.make_n_count("Per_base_N_content")
                    elif module.startswith(">>Sequence Length Distribution"):
                        lineplot = PrepPlotData(current_module)
                        lineplot.make_sequence_length("Sequence_Length_Distribution")
                    elif module.startswith(">>Sequence Duplication Levels"):
                        lineplot = PrepPlotData(current_module)
                        lineplot.make_sequence_duplication("Sequence_Duplication_Levels")
                    elif module.startswith(">>Overrepresented sequences"):
                        overrepresented = PrepPlotData(current_module)
                        overrepresented_html = overrepresented.make_overrepresented("Overrepresented_sequences")
                    elif module.startswith(">>Adapter Content"):
                        lineplot = PrepPlotData(current_module)
                        lineplot.make_adapter("Adapter_Content")
                    elif module.startswith(">>Kmer Content"):
                        kmer = PrepPlotData(current_module)
                        kmer_html = kmer.make_overrepresented("Kmer_Content")
                    current_module = [] #resetting after >>END_MODULE line
                # adding module name to current module list
                elif line.startswith(">>") and not line.startswith(">>END_MODULE"):
                    current_module += [line]
                # skipping file header
                elif line.startswith("##"):
                    continue
                # adding the module data to the current module list
                elif not line.startswith(">>"):
                    current_module.append(line)

        # if kmer_html == None:
        return html_string[0], icon_list, basic_string.df_basics, overrepresented_html, kmer_html
        # else:
        #     return html_string[0], icon_list, basic_string.df_basics, overrepresented_html, kmer_html


# ----------testing---------------

# def main():
#     # subprocess.run("cd ../fastqc_v0.12.1/FastQC/ | /run_fastqc.bat ../../Practicum_3/Example_Data/test.fastq", shell=True)
#     FastQC("ERR550643_1.fastq")
#     # unzip_results()
#
#     # ReadingDataTextFile("../static/fastqc_data_lang.txt")
#
#
# if __name__ == "__main__":
#     EXITCODE = main()
#     sys.exit(EXITCODE)
