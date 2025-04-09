#!/usr/bin/env python3
"""
main script for running the tool and reading the made data file from the tool. Imports the
plotting class to make plots from the data file.

The classes FastQC and ReadingDataTextFile get imported in the app.py script of this project. To
use this class in other projects import the classes like you would any other selfmade class.

"""

__author__ = "Maartje van der Hulst"
__date__ = 2025.3
__version__ = 2.0

import sys #uncomment for testing
import subprocess
from plotting import PrepPlotData #remove . for testing



class FastQC:
    """
    class to run the fastqc tool on the uploaded fastq file and unzip the results so the data.txt
    file is accessible to process and plot
    """
    def __init__(self, file):
        """
        initialize the uploaded file variable and executes the run_fastqc and unzip_results
        functions
        :param file: string containing the name of the uploaded fastq file
        """
        # running both functions when calling the class with the given file
        self.file = file
        self.run_fastqc()
        self.unzip_results()

    def __repr__(self):
        """
        An unambiguous string representation of an object, primarily for developers and debugging.
        :return: string
        """
        return f"FastQC({self.file})"

    def run_fastqc(self):
        """
        using subprocess to run the fastqc tool via the terminal on the uploaded fastq file
        :return: stdout
        """
        # running the bat fastqc file with the given file
        process_1 = subprocess.run(["run_fastqc.bat", f"../../../uploads/{self.file}"],
                                   cwd="tools/fastqc_v0.12.1/FastQC/", shell=True,
                                   capture_output=True)
        return process_1.stdout

    def unzip_results(self):
        """
        using subprocess to unzip the results of the fastqc tool
        :return: stdout
        """
        # unpacking zip created by fastqc so data file is available for processing
        process_2 = subprocess.run(f"tar -xf uploads/{self.file[:-6]}_fastqc.zip", shell=True,
                                   capture_output=True)
        return process_2.stdout


class ReadingDataTextFile:
    """
    class that reads the data from the text file made by the fastqc tool. It uses the
    imported plotting classes to make plots from the data file.
    """
    def __init__(self, file):
        """
        initialize the data text file variable and executes the reading_datafile function saving
        the return values as global variables making them available in the app.py script of
        this project.
        :param file: string containing the path and name of the data text file
        """
        self.file = file
        self.results = {}
        self.dataframe = self.reading_datafile()

    def __repr__(self):
        """
        An unambiguous string representation of an object, primarily for developers and debugging.
        :return: string
        """
        return f"ReadingDataTextFile({self.file})"

    def reading_datafile(self):
        """
        looping through data file saving per module, when the full module is collected the icon
        is saved,  and the data is plotted using the imported plotting classes.
        :return: string of html table of the basic statistics of the data, list with the module
        icons, dataframe of the basic statistics of the data, string of html table of the
        overrepresented module, string of html table of the kmer module
        """
        current_module = []
        icon_list = []

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
                        basic_df = basic_string.df_basics
                        # saving name, icon, number, stream of result in dict
                        self.results["Basic Statistics"] = {'icon': icon_list[-1],
                                                            'num':len(icon_list),
                                                            'type': 'string',
                                                            'result':html_string}
                    elif module.startswith('>>Per base sequence quality'):
                        boxplot = PrepPlotData(current_module)
                        stream = boxplot.make_base_sequence_quality_data(
                            'Quality scores across all bases', basic_df)
                        # saving name, icon, number, stream of result in dict
                        self.results["Per base sequence quality"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'stream',
                                                            'result': stream}
                    elif module.startswith('>>Per tile sequence quality'):
                        heatmap = PrepPlotData(current_module)
                        stream = heatmap.make_per_tile('Quality per tile')
                        # saving name, icon, number, stream of result in dict
                        self.results["Per tile sequence quality"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'stream',
                                                            'result': stream}
                    elif module.startswith(">>Per sequence quality scores"):
                        lineplot = PrepPlotData(current_module)
                        stream = lineplot.make_sequence_quality("Quality score distribution over "
                                                                "all sequences")
                        # saving name, icon, number, stream of result in dict
                        self.results["Per sequence quality scores"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'stream',
                                                            'result': stream}
                    elif module.startswith(">>Per base sequence content"):
                        lineplot = PrepPlotData(current_module)
                        stream = lineplot.make_base_sequence("Sequence content across all bases")
                        # saving name, icon, number, stream of result in dict
                        self.results["Per base sequence content"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'stream',
                                                            'result': stream}
                    elif module.startswith(">>Per sequence GC content"):
                        lineplot = PrepPlotData(current_module)
                        stream = lineplot.make_gc_content("GC distribution over all sequences")
                        # saving name, icon, number, stream of result in dict
                        self.results["Per sequence GC content"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'stream',
                                                            'result': stream}
                    elif module.startswith(">>Per base N content"):
                        lineplot = PrepPlotData(current_module)
                        stream = lineplot.make_n_count("N content across all bases")
                        # saving name, icon, number, stream of result in dict
                        self.results["Per base N content"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'stream',
                                                            'result': stream}
                    elif module.startswith(">>Sequence Length Distribution"):
                        lineplot = PrepPlotData(current_module)
                        stream = lineplot.make_sequence_length("Distribution of sequence lengths "
                                                               "over all sequences")
                        # saving name, icon, number, stream of result in dict
                        self.results["Sequence Length Distribution"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'stream',
                                                            'result': stream}
                    elif module.startswith(">>Sequence Duplication Levels"):
                        lineplot = PrepPlotData(current_module)
                        stream = lineplot.make_sequence_duplication("Sequence_Duplication_Levels")
                        # saving name, icon, number, stream of result in dict
                        self.results["Sequence Duplication Levels"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'stream',
                                                            'result': stream}
                    elif module.startswith(">>Overrepresented sequences"):
                        overrepresented = PrepPlotData(current_module)
                        overrepresented_html = overrepresented.make_overrepresented()
                        # saving name, icon, number, stream of result in dict
                        self.results["Overrepresented sequences"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'string',
                                                            'result': overrepresented_html}
                    elif module.startswith(">>Adapter Content"):
                        lineplot = PrepPlotData(current_module)
                        stream = lineplot.make_adapter("% Adapter")
                        # saving name, icon, number, stream of result in dict
                        self.results["Adapter Content"] = {'icon': icon_list[-1],
                                                            'num': len(icon_list),
                                                            'type': 'stream',
                                                            'result': stream}
                    elif module.startswith(">>Kmer Content"):
                        kmer = PrepPlotData(current_module)
                        kmer_html = kmer.make_kmer()
                        if kmer_html:
                            # saving name, icon, number, stream of result in dict
                            self.results["Kmer Content"] = {'icon': icon_list[-1],
                                                                'num': len(icon_list),
                                                                'type': 'string',
                                                                'result': kmer_html}
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


        return basic_string.df_basics



# ----------testing---------------

def main():
    # subprocess.run("cd ../fastqc_v0.12.1/FastQC/ |
    # /run_fastqc.bat ../../Practicum_3/Example_Data/test.fastq", shell=True)
    # FastQC("ERR550643_1.fastq")
    # unzip_results()

    ReadingDataTextFile("../static/fastqc_data.txt")


if __name__ == "__main__":
    EXITCODE = main()
    sys.exit(EXITCODE)
