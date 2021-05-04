#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CODE DESCRIPTION HERE

Created on 2021-01-2021-01-05 13:53

@author: cook
"""
import logging
import numpy as np
import os
from typing import Any, Dict, List, Union

import recipe1
import recipe2

# =============================================================================
# Define variables
# =============================================================================
# define runs per group
RUNS_PER_GROUP = 50
# define number of groups
NUM_GROUPS = 10
# define whether this is a test run (just write to file don't run)
TEST_RUN = False
# Number of cores (when using multiprocessing)
NUM_CORES = 10
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
class Run:
    def __init__(self, recipename: str,
                 args: Union[List[Any], None] = None,
                 kwargs: Union[Dict[str, Any], None] = None):
        """
        This just stores the information for each run - for now it is
        either used to just write the "runstring" or to run the
        "recipe" .main function

        we use get_run_program at run time to get the correct module

        runstring is:
            recipename arg[0] arg[1] arg[2] --kwarg[0]=kwargs[kwarg[0]]

        :param recipename: str, the name of the recipe (for the run string)
        :param args: a list of positional arguments (can be None) passed to
                     recipe.main
        :param kwargs: a list of kwarg arguments passed to recipe.main
        """
        self.name = recipename
        if args is None:
            self.args = []
        else:
            self.args = list(args)
        if kwargs is None:
            self.kwargs = dict()
        else:
            self.kwargs = dict(kwargs)
        # get run string
        self.runstring = ''
        self.get_runstring()

    def get_runstring(self):
        self.runstring = '{0}'.format(self.name)
        for arg in self.args:
            self.runstring += ' {0}'.format(arg)
        for kwarg in self.kwargs:
            self.runstring += ' --{0}={1}'.format(kwarg, self.kwargs[kwarg])

    def get_run_program(self):
        if self.name == 'recipe1.py':
            return recipe1
        if self.name == 'recipe2.py':
            return recipe2


def linear_process(run_object):
    """
    Wrapper around run object

    :param run_object: Run instance
    :return:
    """
    # get run module
    rmod = run_object.get_run_program()
    # run main with args and kwargs
    return rmod.main(*run_object.args, **run_object.kwargs)


# =============================================================================
# Start of code
# =============================================================================
if __name__ == "__main__":
    # generate runs (just calls to recipe.py with group number and run number)
    runs = []
    groups = []
    # loop around groups
    for group_num in range(NUM_GROUPS):
        # loop around runs
        for run_num in range(RUNS_PER_GROUP):
            # define parity
            if group_num % 2 == 0:
                parity = 1
                rmod = recipe1
            else:
                parity = 2
                rmod = recipe2
            # generate command
            recipename = 'recipe{0}.py'.format(parity)
            run = Run(recipename, args=[group_num, run_num])
            # log message
            msg = 'PROCESSING: Adding "{0}"'.format(run.runstring)
            print(msg)
            # adding command
            logging.info(msg)
            # add to runs
            runs.append(run)
            # append group number
            groups.append(group_num)
    # define a counter for current group
    current_group = -1
    # -------------------------------------------------------------------------
    if TEST_RUN:
        # log message
        msg = 'PROCESSING: Writing run file: {0}'.format(RUN_FILE)
        print(msg)
        # write runs to a file
        with open(RUN_FILE, 'w') as wfile:
            # loop around run files
            for it, run in enumerate(runs):
                # get this rows group number
                group_num = groups[it]
                # see if current group has changed
                if current_group != group_num:
                    # write a command
                    wfile.write('\n# Group {0}\n'.format(group_num))
                    # update current group
                    current_group = int(group_num)
                # write line
                wfile.write(run.runstring + '\n')
    # -------------------------------------------------------------------------
    # Else we run with multiprocessing
    # TODO: this is what we need to replace - this works well on one machine
    #       but how do we get this to work on a cluster with nodes?
    else:
        # deal with Pool specific imports
        from multiprocessing import get_context
        from multiprocessing import set_start_method
        try:
            set_start_method("spawn")
        except RuntimeError:
            pass
        # get unique groups
        ugroups = np.unique(groups)
        # make groups and runs numpy arrays
        groups, runs = np.array(groups), np.array(runs)
        # storage for returned outputs
        return_dict = dict()
        # loop around groups
        for ugroup in ugroups:
            # get list for return
            return_dict[ugroup] = []
            # get all runs in group
            mask = groups == ugroup
            # arguments to pool must be a list of arguments
            poolargs = []
            for run in runs[mask]:
                poolargs.append([run])
            # send the runs for this mask to the pool
            with get_context('spawn').Pool(NUM_CORES, maxtasksperchild=1) as pool:
                # get parallel process
                results = pool.starmap(linear_process, poolargs)
            # get results
            for row in range(len(results)):
                return_dict[ugroup].append(results[row])

        # print the results after
        print('Results of multiprocess:')
        for ugroup in return_dict:
            print('Group {0}'.format(ugroup))
            for row in range(len(return_dict[ugroup])):
                margs = [row, return_dict[ugroup][row]]
                print('\t\tResult {0}: {1}'.format(*margs))


# =============================================================================
# End of code
# =============================================================================
