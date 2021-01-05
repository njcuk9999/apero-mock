#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CODE DESCRIPTION HERE

Created on 2021-01-2021-01-05 13:53

@author: cook
"""
import logging
import os

# =============================================================================
# Define variables
# =============================================================================
# define runs per group
RUNS_PER_GROUP = 50
# define number of groups
NUM_GROUPS = 10
# output file name
RUN_FILE = 'apero-runs.txt'
# remove previous runs / log file
if os.path.exists('apero-log.txt'):
    os.remove('apero-log.txt')
if os.path.exists(RUN_FILE):
    os.remove(RUN_FILE)
# define logger
logger = logging.basicConfig(filename='apero-log.txt', level=logging.INFO,
                             format='%(asctime)s | %(levelname)s | %(message)s')


# =============================================================================
# Define functions
# =============================================================================
def main():

    # generate runs (just calls to recipe.py with group number and run number)
    runs = []
    group = []
    # loop around groups
    for group_num in range(NUM_GROUPS):
        # loop around runs
        for run_num in range(RUNS_PER_GROUP):
            # define parity
            if group_num % 2 == 0:
                parity = 1
            else:
                parity = 2
            # generate command
            command = 'recipe{0}.py {1} {2}'.format(parity, group_num, run_num)
            # log message
            msg = 'PROCESSING: Adding "{0}"'.format(command)
            print(msg)
            # adding command
            logging.info(msg)
            # add to runs
            runs.append(command)
            # append group number
            group.append(group_num)

    # define a counter for current group
    current_group = -1
    # log message
    msg = 'PROCESSING: Writing run file: {0}'.format(RUN_FILE)
    print(msg)
    # write runs to a file
    with open(RUN_FILE, 'w') as wfile:
        # loop around run files
        for it, run in enumerate(runs):
            # get this rows group number
            group_num = group[it]
            # see if current group has changed
            if current_group != group_num:
                # write a command
                wfile.write('\n# Group {0}\n'.format(group_num))
                # update current group
                current_group = int(group_num)
            # write line
            wfile.write(run + '\n')


# =============================================================================
# Start of code
# =============================================================================
if __name__ == "__main__":
    main()

# =============================================================================
# End of code
# =============================================================================
