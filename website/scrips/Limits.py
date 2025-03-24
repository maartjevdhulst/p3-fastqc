#!/usr/bin/env python3
"""
limits class to edit limits.txt of fastqc tool
use:
"""

__author__ = "Maartje van der Hulst"
__date__ = 2025.3
__version__ = 1.0

import sys
import re

class Limits:
    def __init__(self, limits, file):
        self.limits = limits
        self.file = file
        self.changes_dict = {}
        self.full_file = ""
        self.file_handler()

    def change_limits(self):
        for key, value in self.limits.items():
            if len(value) == 3:
                self.changes_dict[key] = value
            elif len(value) == 5:
                self.changes_dict[key] = value[0]
                key_lower = key+"_lower"
                self.changes_dict[key_lower] = ['on']
                self.changes_dict[key_lower].extend(value[1:3])
                key_median = key+"_median"
                self.changes_dict[key_median] = ['on']
                self.changes_dict[key_median].extend(value[3:])

        return self.changes_dict


    def file_handler(self):
        changes_dict = self.change_limits()

        with open(self.file, 'r+') as open_file:
            for line in open_file:
                if not line.startswith("#"):
                    line = line.strip('\n')
                    line = re.sub("\s+", "\t", line)
                    line = line.split('\t')
                    if len(line) < 2:
                        self.full_file += '\n'
                        continue
                    if line[0] in changes_dict.keys() and line[1] == 'ignore':
                        line[2]='0\n'
                    elif line[1] == 'ignore':
                        line[2]='1\n'
                    elif line[0] in changes_dict.keys() and line[1] == 'warn':
                        line[2]=changes_dict[line[0]][1] + '\n'
                    elif line[1] == 'warn':
                        line += '\n'
                    elif line[0] in changes_dict.keys() and line[1] == 'error':
                        line[2]=changes_dict[line[0]][2] + '\n'
                    elif line[1] == 'error':
                        line += '\n'
                    line = '\t\t'.join(line)
                    self.full_file += line
                else:
                    self.full_file += line
        self.make_outfile()
        return f'limits.txt changed'

    def make_outfile(self):
        with open(self.file, 'w') as outfile:
            outfile.write(self.full_file)
        return 0


# testing

# limits = {'quality_base': ['on', '11', '4', '26', '21'],
# 'sequence': ['10', '20'],
# 'gc_sequence': ['15', '30'],
# 'quality_sequence': ['27', '20'],
# 'tile': ['on', '6', '11'],
# 'sequence_length': ['1', '1'],
# 'adapter': ['6', '11']}
#
# new = Limits(limits, "../../../fastqc_v0.12.1/FastQC/Configuration/limits_kopie.txt")
# a = new.file_handler()
# print(new.change_limits())
# print(a)
