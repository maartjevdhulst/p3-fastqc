#!/usr/bin/env python3
"""

"""

__author__ = "Maartje van der Hulst"
__date__ = 2025.3
__version__ = 1.0

import sys
import subprocess
from subprocess import Popen
from Plotting_v2 import MakeTables

def run_fastqc(file):

    p1 = Popen(["run_fastqc.bat", file],
               cwd="C:/Users/maart/School/Practicum/fastqc_v0.12.1/FastQC/", shell=True)
    stdout, stderr = p1.communicate()

def unzip_results():
    subprocess.run("tar -xf ../static/test_fastqc.zip -C ../static/", shell=True)

def reading_datafile(file):
    current_module = []
    with open(file, "r") as open_file:
        for line in open_file:
            if line.startswith(">>END_MODULE"):
                module = current_module[0]
                if module.startswith(">>Basic Statistics"):
                    print('basic statistics gevonden')
                    print(module)
                    html_string = MakeTables(current_module)
                    print(html_string)
                #     plotting class die module(->soort plot) en inhoud(current_module) meekrijgt
                current_module = []
                break
            elif line.startswith(">>") and not line.startswith(">>END_MODULE"):
                current_module += [line]
            elif line.startswith("##"):
                continue
            elif not line.startswith(">>"):
                current_module.append(line)

    return 0


def main():
    # subprocess.run("cd ../fastqc_v0.12.1/FastQC/ | /run_fastqc.bat ../../Practicum_3/Example_Data/test.fastq", shell=True)
    # run_fastqc("../../p3-fastqc/website/static/test.fastq")
    # unzip_results()
    reading_datafile("../static/test_fastqc/fastqc_data.txt")


if __name__ == "__main__":
    EXITCODE = main()
    sys.exit(EXITCODE)
