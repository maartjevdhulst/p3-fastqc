#!/usr/bin/env python3
"""
limits class to edit the limits.txt file of the fastqc tool in the Tools directory. By changing
this file you change how many of the modules from the tool get executed and which warning and
error limits they use.

This class gets imported in the app.py script of this project. To use this class in other projects
import the class like you would any other selfmade class.
"""

__author__ = "Maartje van der Hulst"
__date__ = 2025.3
__version__ = 2.0


import re

class Limits:
    """
    changes the limits.txt file of the fastqc tool when given the desired settings
    and the limits.txt file
    """
    def __init__(self, limits, file):
        """
        initializes global variables and executes file_handler function, which executes both
        change_limits and make_outfile function thus, if user gives file and limits the file
        will be changed after the class is instantiated.
        :param limits: dict with titles of the modules as keys and a list starting with 'on' for
        each module to be executed followed by their limits. If the module is to be switched off,
        the list will only contain the standard limits.
        :param file: string with (path to) file name
        """
        self.limits = limits
        self.file = file
        self.changes_dict = {}
        self.full_file = ""
        self.file_handler()

    def __repr__(self):
        """
        An unambiguous string representation of an object, primarily for developers and debugging.
        :return: string
        """
        return f"Limits({self.limits}, {self.file})"

    def change_limits(self):
        """
        loops through dict with settings given by user so only wanted modules are returned and
        the quality base module limits are split into lower and median limits
        :return: dict only containing the 'on' modules with their limits
        """
        for key, value in self.limits.items():
            # each module that the user switched on has 2 or 4 limits
            if len(value) == 3: #normal, add to new dict
                self.changes_dict[key] = value
            elif len(value) == 5: #more settings per module which need to be split
                self.changes_dict[key] = value[0] # unchanged module name + on added to dict to
                # be able to switch the module on
                key_lower = key+"_lower" #adding changed module name & corresponding limits
                self.changes_dict[key_lower] = ['on'] #making value length the same as the rest
                self.changes_dict[key_lower].extend(value[1:3])
                key_median = key+"_median"
                self.changes_dict[key_median] = ['on']
                self.changes_dict[key_median].extend(value[3:])

        return self.changes_dict

    def file_handler(self):
        """
        executes change_limits function
        loops through file, changes which modules are switched on and their changed limits,
        saves changes in string, uses that string to write the changes back to the file with the
        make_outfile function
        :return: string confirming full execution
        """
        # calling previous function to have usable dict with settings
        changes_dict = self.change_limits()

        # looping through file
        with open(self.file, 'r') as open_file:
            for line in open_file:
                if not line.startswith("#"): #skipping lines with instructions
                    line = line.strip('\n')
                    line = re.sub(r"\s+", "\t", line) #removing excessive whitespaces
                    line = line.split('\t')
                    if len(line) < 2: #empty lines
                        self.full_file += '\n'
                        continue
                    # switching modules on or off
                    if line[0] in changes_dict.keys() and line[1] == 'ignore':
                        line[2]='0\n' # == on
                    elif line[1] == 'ignore':
                        line[2]='1\n' # == off
                    # changing the warning limit
                    elif line[0] in changes_dict.keys() and line[1] == 'warn':
                        line[2]=changes_dict[line[0]][1] + '\n'
                    # adding removed new line back to unchanged lines
                    elif line[1] == 'warn':
                        line += '\n'
                    # changing the error limit
                    elif line[0] in changes_dict.keys() and line[1] == 'error':
                        line[2]=changes_dict[line[0]][2] + '\n'
                    # adding removed new line back to unchanged lines
                    elif line[1] == 'error':
                        line += '\n'
                    # turning list of strings back into a correctly spaced string
                    line = '\t\t'.join(line)
                    self.full_file += line
                else:
                    self.full_file += line
        # calling function to write all made changes to the file
        self.make_outfile()
        return 'limits.txt changed'

    def make_outfile(self):
        """
        writes changes back to the file
        :return: 0
        """
        with open(self.file, 'w') as outfile: #same as input file, 'w' mode to override current file
            outfile.write(self.full_file)
        return 0


# --------------------testing-------------
#
# limits = {'quality_base': ['on', '11', '4', '26', '21'],
# 'sequence': ['10', '20'],
# 'gc_sequence': ['15', '30'],
# 'quality_sequence': ['27', '20'],
# 'tile': ['on', '6', '11'],
# 'sequence_length': ['1', '1'],
# 'adapter': ['6', '11']}
# #
# new = Limits(limits, "../Tools/fastqc_v0.12.1/FastQC/Configuration/limits.txt")
#
# # a = new.file_handler()
# # print(new.change_limits())
# # print(a)
